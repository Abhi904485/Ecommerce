import os
import threading
import logging


def live(l1):
    l1.debug("i am in live function")
    os.system("python manage.py livereload --host=localhost")


def server(l2):
    l2.debug("i am in server function")
    os.system("python manage.py runserver")


def main():
    logger = logging.getLogger("my_logger")
    logger.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(filename)s %(funcName)s %(lineno)d %(process)d %(processName)s %(thread)d %(threadName)s',
        datefmt='%m/%d/%Y %I:%M:%S %p')
    sh.setFormatter(formatter)
    logger.addHandler(sh)
    logger.debug("I am in main function")
    t1 = threading.Thread(target=live, args=(logger,))
    t2 = threading.Thread(target=server, args=(logger,))
    t1.setDaemon(True)
    t2.setDaemon(True)
    t1.start()
    t2.start()
    t1.join()
    t2.join()


if __name__ == '__main__':
    main()
