#import terminal
from subprocess import Popen, PIPE, STDOUT
from select import select
import sys
import tty
import fcntl
import os

BUFFSIZE=512
TIMEOUT = 0.1

class ShellClient:
    def __init__(self, socket):
        self.s = socket
        for fd in [sys.stdin.fileno()]:
            fl = fcntl.fcntl(fd, fcntl.F_GETFL)
            fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
        tty.setraw(sys.stdin.fileno())

    def run(self):
        while not sys.stdin.closed:
            if select([sys.stdin], [],[],TIMEOUT)[0]:
                if select([],[self.s],[],TIMEOUT)[1]:
                    s = sys.stdin.read()
                    self.s.send(s)
            if select([self.s],[],[],TIMEOUT)[0]:
                if select([],[sys.stdout],[],TIMEOUT)[1]:
                    sys.stdout.write(self.s.recv(BUFFSIZE))


if __name__ == "__main__":
    import socket
    if len(sys.argv) > 1:
        s = socket.socket(socket.AF_UNIX)
        s.connect('\0'+sys.argv[1])
        C = ShellClient(s)
        C.run()
    else:
        sys.stderr.write("usage: python %s <socketname>\n" % sys.argv[1])
