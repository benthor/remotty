#import terminal
from subprocess import Popen, PIPE, STDOUT
import select
import sys
#import tty
import fcntl
import os

BUFFSIZE=512
TIMEOUT = 1

class ShellServer:
    def __init__(self, socket, shell="/bin/zsh"):
        self.P = Popen([shell,"-i"], stdin=PIPE, stdout=PIPE, stderr=STDOUT)
        self.tosocket = os.fdopen(socket.fileno(), "w")
        self.frsocket = os.fdopen(socket.fileno(), "r")
        #self.s.setblocking(0)
        # maybe this works for the socket filedescriptor as well XXX
        for fd in [self.P.stdout.fileno()]:#, socket.fileno()]:
            fl = fcntl.fcntl(fd, fcntl.F_GETFL)
            fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)



    def run(self):
        P = self.P
        while not P.poll():
            readables = select.select([P.stdout,self.frsocket], [], [],
                    TIMEOUT)[0]
            writables = select.select([], [P.stdin, self.tosocket], [],
                    TIMEOUT)[1]
            for r in readables:
                if r == P.stdout:
                    if self.tosocket in writables:
                        self.tosocket.write(r.read())
                        self.tosocket.flush()
                else:
                    if P.stdin in writables:
                        P.stdin.write(r.read())

        return P.returncode


class ShellClient:
    def __init__(self, socket):
        self.s = socket
        #self.s.setblocking(0)
        for fd in [sys.stdin.fileno()]:
            fl = fcntl.fcntl(fd, fcntl.F_GETFL)
            fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

    def run(self):
        while not sys.stdin.closed:
            readables, writables, _nothing = select.select([sys.stdin, self.s],
                    [sys.stdout, self.s], [], TIMEOUT)
            for r in readables:
                if r == self.s:
                    if sys.stdout in writables:
                        sys.stdout.write(r.recv(BUFFSIZE))
                else:
                    if self.s in writables:
                        self.s.send(r.read())


import socket

servsoc, clntsoc = socket.socketpair()

def runserver(sock):
    S = ShellServer(sock)
    S.run()

def runclient(sock):
    C = ShellClient(sock)
    C.run()

from multiprocessing import Process

s = Process(target=runserver, args=(servsoc,))
s.start()

c = Process(target=runclient, args=(clntsoc,))
c.start()

s.join()
c.join()


