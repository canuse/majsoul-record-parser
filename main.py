from jinja2 import Environment, FileSystemLoader, select_autoescape

from majsoul.parser import parseFromBase64
from majsoul.simulator import simulator

if __name__ == "__main__":
    a = parseFromBase64('test/64.txt')
    # a.print()
    name = '||||||'
    b = simulator(a, name)
    b.simulate()
    env = Environment(
        loader=FileSystemLoader('templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template("record_checker_template.html")
    name=name.replace('|','Vertical_bar')
    name=name.replace('*','Star')
    name=name.replace('\\','backslash')
    name=name.replace('/','rbackslash')
    name=name.replace('?','question')
    name=name.replace('"','quote')
    name=name.replace(':','colon')
    name=name.replace('<','lbrackets')
    name=name.replace('>','rbrackets')


    file_name = "majsoul_record_{0}_{1}.html".format(a.uuid, name)
    with open(file_name, "w+", encoding='utf-8') as result_file:
        result_file.write(template.render(
            player=name,
            record=str(a.uuid),
            log_url=b.report[0].url,
            games=b.report[0].game
        ))
