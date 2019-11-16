import base64
import multiprocessing
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

from jinja2 import Environment, FileSystemLoader, select_autoescape

from majsoul.parser import parseFromBase64data
from majsoul.simulator import simulator


def check(a, name):
    b = simulator(a, name)
    b.simulate()
    env = Environment(
        loader=FileSystemLoader('templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template("record_checker_template.html")
    name = name.replace('|', 'Vertical_bar')
    name = name.replace('*', 'Star')
    name = name.replace('\\', 'backslash')
    name = name.replace('/', 'rbackslash')
    name = name.replace('?', 'question')
    name = name.replace('"', 'quote')
    name = name.replace(':', 'colon')
    name = name.replace('<', 'lbrackets')
    name = name.replace('>', 'rbrackets')

    file_name = "majsoul_record_{0}_{1}.html".format(a.uuid, name)
    with open(file_name, "w+", encoding='utf-8') as result_file:
        result_file.write(template.render(
            player=name,
            record=str(a.uuid),
            log_url=b.report[0].url,
            games=b.report[0].game
        ))


class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        mpath, margs = urllib.parse.splitquery(self.path)
        datas = self.rfile.read(int(self.headers['content-length']))
        self.__parse(datas[8:])
        self.send_response(200)
        self.end_headers()

    def __parse(self, data):
        rawdata = base64.b64decode(data)
        if (".majsoul.com:7343/majsoul/game_record/" in str(rawdata)) or (len(rawdata) > 10000):
            a = parseFromBase64data(rawdata[3:])
            checknames = a.players.playernames[:a.players.num]
            print("Fetch new record: {0}".format(a.uuid))
            pool = multiprocessing.Pool(4)
            for i in checknames:
                pool.apply_async(check, args=(a, i,))
            pool.close()
            with open(a.uuid, "w", encoding="UTF-8") as f:
                f.write(data.decode())


def runserver(host='localhost', port=8888):
    server = HTTPServer((host, port), RequestHandler)
    print("Starting server, listen at: {0}:{1}".format(host, port))
    server.serve_forever()
