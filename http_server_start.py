# encoding=utf-8
"""
@author huxujun
@date 2019-06-13
"""
import SimpleHTTPServer
import SocketServer
import logging
import os
import signal
import sys


class SignalException(Exception):
    pass


def __start_server():
    port = int(sys.argv[1]) if len(sys.argv) >= 2 else 80
    pid_txt = os.path.join(os.path.dirname(__file__), "pid.txt")

    handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    httpd = SocketServer.TCPServer(("", port), handler)

    logging.info("Create the %s", pid_txt)
    with open(pid_txt, "w") as f:
        f.write("{}\n".format(os.getpid()))

    while True:
        try:
            logging.info("Start the http server, serving at port %d", port)
            httpd.serve_forever()
        except Exception as ex:
            if isinstance(ex, SignalException):
                break
            logging.error("Error occur %s, try to restart...", ex)
    logging.warning("Remove %s", pid_txt)
    os.remove(pid_txt)
    logging.warning("Stop the http server, serving at port %d", port)


def __signal_handler(signal_num, frame):
    logging.info("Get signal %d", signal_num)
    raise SignalException("Signal {}".format(signal_num))


def __change_workspace():
    for root, _, files in os.walk(os.path.dirname(__file__)):
        for filename in files:
            if filename.lower() == "index.html":
                os.chdir(root)
                logging.info("Change workspace to %s", root)
                return
    raise Exception("Can not find index.html in %s" % os.path.dirname(__file__))


def main():
    logging.basicConfig(level=logging.INFO)
    signal.signal(signal.SIGTERM, __signal_handler)
    signal.signal(signal.SIGINT, __signal_handler)
    __change_workspace()
    __start_server()


if __name__ == '__main__':
    main()
