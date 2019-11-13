import base64
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

from majsoul.parser import parseFromBase64data


class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        print(1)
        mpath, margs = urllib.parse.splitquery(self.path)
        datas = self.rfile.read(int(self.headers['content-length']))
        self.__parse(datas[8:])
        self.send_response(200)
        self.end_headers()

    def __parse(self, data):
        rawdata = base64.b64decode(data)
        if (".majsoul.com:7343/majsoul/game_record/" in str(rawdata)) or (len(rawdata) > 10000):
            a = parseFromBase64data(rawdata[3:])
            print("Fetch new record: {0}".format(a.uuid))
            with open(a.uuid, "w", encoding="UTF-8") as f:
                f.write(data.decode())


def runserver(host='localhost', port=8888):
    server = HTTPServer((host, port), RequestHandler)
    print("Starting server, listen at: %s:%s" % host)
    server.serve_forever()
