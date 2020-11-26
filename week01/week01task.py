
import time
import logging
import os

def configLog():

    path = mkdirToday("/var/log/")

    logging.basicConfig(
        filename=path + "h-run.log",
        level=logging.DEBUG,
        datefmt="%d/%m/%Y %X",
        format="%(asctime)s \t %(message)s"
    )

    logging.info("initialized")


def mkdirToday(pdir):
    today = time.strftime("%Y-%m-%d", time.localtime())
    hour = time.localtime().tm_hour
    path = pdir + "pyton" + today
    try:
        os.makedirs(path, exist_ok=True)
    except Exception:
        print("create folder failed.")

    return path + "/" + str(hour)


def fib(n):
    listf = []
    a = 0
    b = a + 1
    for i in range(n):
        listf.append(a)
        a, b = b, a+b
    return listf

def fibs(n):
    configLog()
    for i in range(1, n):
        temp = fib(i)
        time.sleep(1)
        logging.info(f"fib function executed {str(i)} time(s), last element is {temp[-1]}")



if __name__ == '__main__':

    fibs(50)