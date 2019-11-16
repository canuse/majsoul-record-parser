import multiprocessing

from selenium import webdriver

from server.simpleWebServer import runserver


def rs():
    runserver()


if __name__ == "__main__":
    paipu = input("paipu:")
    p = multiprocessing.Process(target=rs)
    p.start()
    options = webdriver.ChromeOptions()
    options.add_argument("user-data-dir=PATH-TO-DATA-DIR")
    w = webdriver.Chrome(executable_path="CHROMEDRIVER PATH", options=options)
    w.get(paipu)
