// ==UserScript==
// @name         Majsoul websocket forward
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  Forward the majsoul websocket to loaclhost and console.log
// @include        https://www.majsoul.com/*
// @grant        none
// @run-at      document-start
// ==/UserScript==

// This script is inspired by and modified on the WebSocket Logger of esterTion (https://greasyfork.org/zh-CN/scripts/38248-websocket-logger).

var scriptString = (function () {
    if (window.Proxy == undefined) return;
    var oldWS = window.WebSocket;
    var loggerIncrement = 1;

    function forward(data) {
        var httpRequest = new XMLHttpRequest();
        httpRequest.open('POST', 'http://127.0.0.1:8888', true);
        httpRequest.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        httpRequest.send('content=' + data)
    }

    function processDataForOutput(data) {
        if (typeof data == 'string') return data;
        else if (data.byteLength != undefined) {
            var val = {orig: data, uintarr: new Uint8Array(data)};
            var arr = [], i = 0;
            for (; i < data.byteLength; i++) {
                arr.push(val.uintarr[i]);
            }
            var hexarr = arr.map(function (i) {
                var s = i.toString(16);
                while (s.length < 2) s = '0' + s;
                return s;
            });
            val.string = unescape(hexarr.map(function (i) {
                return '%' + i;
            }).join(''));
            val.b64str = btoa(val.string);
            return val;
        }
    }

    var proxyDesc = {
        set: function (target, prop, val) {
            if (prop == 'onmessage') {
                var oldMessage = val;
                val = function (e) {
                    var val = processDataForOutput(e.data);
                    //  console.log(`#${target.WSLoggerId} Msg from server << `, val);
                    forward(val.b64str);
                    oldMessage(e);
                };
            }
            return target[prop] = val;
        },
        get: function (target, prop) {
            var val = target[prop];
            if (prop == 'send') val = function (data) {
                var val = processDataForOutput(data);
                //console.log(`#${target.WSLoggerId} Msg from client >> `, val);
                forward(val.b64str);
                target.send(data);
            };
            else if (typeof val == 'function') val = val.bind(target);
            return val;
        }
    };
    WebSocket = new Proxy(oldWS, {
        construct: function (target, args, newTarget) {
            var obj = new target(args[0]);
            obj.WSLoggerId = loggerIncrement++;
            // console.log(`WebSocket #${obj.WSLoggerId} created, connecting to`, args[0]);
            return new Proxy(obj, proxyDesc);
        }
    });
});

var observer = new MutationObserver(function () {
    if (document.head) {
        observer.disconnect();
        var script = document.createElement('script');
        script.innerHTML = '(' + scriptString + ')();';
        document.head.appendChild(script);
        script.remove();
    }
});
observer.observe(document, {subtree: true, childList: true});