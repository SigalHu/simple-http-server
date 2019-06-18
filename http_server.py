# encoding=utf-8
"""
@author huxujun
@date 2019-06-16
"""
import logging
import os
import signal
import sys

if sys.version_info.major == 2:
    import SimpleHTTPServer
    import SocketServer as socketserver

    reload(sys)
    sys.setdefaultencoding("utf-8")
else:
    import http.server as SimpleHTTPServer
    import socketserver


class HttpServer(object):

    def __init__(self, port=80):
        super(HttpServer, self).__init__()
        logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s")
        self.__logger = logging.getLogger(self.__class__.__name__)
        self.__port = port

        self.__pid_file = self.__create_pid_file(os.getcwd())
        self.__register_signal()
        self.__change_workspace()

    def __del__(self):
        if os.path.isfile(self.__pid_file):
            os.remove(self.__pid_file)

    @staticmethod
    def __register_signal():
        signal.signal(signal.SIGTERM, HttpServer.__signal_handler)
        signal.signal(signal.SIGINT, HttpServer.__signal_handler)

    @staticmethod
    def __signal_handler(signal_num, frame):
        raise SignalException("Received signal {}".format(signal_num))

    def __create_pid_file(self, output):
        pid_file = os.path.join(output, "pid.txt")
        self.__logger.info("Create the %s", pid_file)
        with open(pid_file, "w") as f:
            f.write("{}\n".format(os.getpid()))
        return pid_file

    def __change_workspace(self):
        for root, _, files in os.walk(os.getcwd()):
            for filename in files:
                if filename.lower() == "index.html":
                    os.chdir(root)
                    self.__logger.info("Change workspace to %s", root)
                    return
        raise Exception("Can not find index.html in %s" % os.path.dirname(__file__))

    def start(self):
        handler = SimpleHTTPServer.SimpleHTTPRequestHandler
        httpd = socketserver.TCPServer(("", self.__port), handler)
        while True:
            try:
                self.__logger.info("Start the http server, serving at port %d", self.__port)
                httpd.serve_forever()
            except Exception as ex:
                if isinstance(ex, SignalException):
                    break
                self.__logger.exception("Error occurs, try to restart...")
        self.__logger.warning("Stop the http server, serving at port %d", self.__port)


class SignalException(Exception):
    pass


if __name__ == '__main__':
    HttpServer(int(sys.argv[1]) if len(sys.argv) >= 2 else 80).start()
