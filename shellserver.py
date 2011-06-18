#import terminal
from subprocess import Popen, PIPE, STDOUT
from select import select
import sys
#import tty
import fcntl
import os

BUFFSIZE=512
TIMEOUT = 1

class ShellServer:
    def __init__(self, socket, shell="/bin/zsh"):
        self.P = Popen([shell], stdin=PIPE, stdout=PIPE, stderr=STDOUT)
        self.S = socket
        self.S.setblocking(0)
        # FIXME: remove loop 
        for fd in [self.P.stdout.fileno()]:
            fl = fcntl.fcntl(fd, fcntl.F_GETFL)
            fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

    def run(self):
        P = self.P
        S = self.S
        while not P.poll():
            writables = select([],[S, P.stdin],[],TIMEOUT)[1]
            for w in writables:
                if w == P.stdin:
                    r = select([S],[],[],TIMEOUT)[0]
                    if r:
                        s = S.recv(BUFFSIZE)
                        print s
                        w.write(s)
                        w.flush()
                else:
                    r = select([P.stdout],[],[],TIMEOUT)[0]
                    if r:
                        S.send(r[0].read())

        return P.returncode


if __name__ == "__main__":
    if len(sys.argv) > 1:
        import socket
        s = socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
        try:
            s.bind('\0'+sys.argv[1])
            s.listen(1)
            con = s.accept()[0]
            S = ShellServer(con)
            S.run()
        finally:
            s.close()     
    else:
        sys.stderr.write("usage: python %s <socketname>\n" % sys.argv[0])

