#import terminal
from subprocess import Popen, PIPE, STDOUT
from select import select
import sys
#import tty
import fcntl
import pty
import os

BUFFSIZE=512
TIMEOUT = 1

class ShellServer:
    def __init__(self, socket, shell="/bin/zsh"):
        pid, fd = os.forkpty()
        if pid == 0:
            os.execlp(shell, "-i")
        self.fromshell = os.fdopen(fd, "r")
        self.toshell = os.fdopen(fd, "w")
        self.S = socket
        #self.S.setblocking(0)
        #for fd in [fd]:
        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

    def run(self):
        S = self.S
        b = ""
        while not self.fromshell.closed and not self.toshell.closed:
            writables = select([],[S, self.toshell],[],TIMEOUT)[1]
            print writables
            for w in writables:
                if w == self.toshell:
                    r = select([S],[],[],TIMEOUT)[0]
                    if r:
                        print "reading from socket"
                        s = S.recv(BUFFSIZE)
                        print "read from socket"
                        S.send(s)
                        if s != chr(13):
                            b += s
                        else:
                            w.write(b+"\n")
                            b = ""
                            w.flush()
                else:
                    r = select([self.fromshell],[],[],TIMEOUT)[0]
                    if r:
                        print "reading from shell"
                        S.send(r[0].read())
                        print "read and sent"



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

