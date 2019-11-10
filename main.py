import multiprocessing

from jinja2 import Environment, FileSystemLoader, select_autoescape

from majsoul.parser import parseFromBase64
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


if __name__ == "__main__":
    fn = input("Record Filename: ")
    a = parseFromBase64(fn)
    # a.print()
    name = input("Username, leave empty to check all user: ")
    if name == '':
        checknames = a.players.playernames[:a.players.num]
    else:
        if name not in a.players.playernames:
            raise ValueError("name not found")
        checknames = [name]
    pool = multiprocessing.Pool(4)
    for i in checknames:
        pool.apply_async(check, args=(a, i,))
    pool.close()
    pool.join()
