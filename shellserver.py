#import terminal
from subprocess import Popen, PIPE, STDOUT
import select
import sys
#import tty
import fcntl
import os

class ShellServer:
    def __init__(self, socket, shell="/bin/zsh"):
        self.P = Popen([shell,"-i"], stdin=PIPE, stdout=PIPE, stderr=STDOUT)
        self.s = socket
        self.s.setblocking(0)
        for fd in [sys.stdin.fileno(), P.stdout.fileno()]:
            fl = fcntl.fcntl(fd, fcntl.F_GETFL)
            fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

    def run(self):
        while not P.poll():
            readables, writables, _nothing = select.select([P.stdout, sys.stdin],
                    [P.stdin, sys.stdout], [], 1)
            for r in readables:
                if r == P.stdout:
                    if sys.stdout in writables:
                        sys.stdout.write(r.read())
                else:
                    if P.stdin in writables:
                        P.stdin.write(r.read())

        return P.returncode

                




