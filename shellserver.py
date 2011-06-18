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
        pid, _fd = os.forkpty()
        if pid == 0:
            os.execlp(shell, "-i")
        self.fromshell = os.fdopen(_fd, "r")
        self.toshell = os.fdopen(_fd, "w")
        # python doesn't implement socket.flush(), so need to go via
        # filedescriptors...
        self.tosocket = os.fdopen(socket.fileno(), 'w')
        self.fromsocket = os.fdopen(socket.fileno(), 'r')
        for fd in [_fd, socket.fileno()]:
            fl = fcntl.fcntl(fd, fcntl.F_GETFL)
            fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

    def run(self):
        fromshell,toshell,tosocket,fromsocket =\
        self.fromshell,self.toshell,self.tosocket,self.fromsocket
        while not fromshell.closed and not toshell.closed:
            # only interested in fd's which we can currently read from
            readables = select([fromshell, fromsocket],[],[])[0]
            for r in readables:
                if r == fromshell:
                    # hackish way to wait until socket becomes ready
                    # had errors when just trying to naively writing to socket
                    # select blocks until 'tosocket' is ready for writing
                    # returns [[],[tosocket],[]], which is unpacked by
                    # subscripts
                    select([],[tosocket],[])[1][0].write(r.read())
                    # this is probably just superstition
                    r.flush()
                    # this IS important
                    tosocket.flush()
                elif r == fromsocket:
                    # analogous to above
                    select([],[toshell],[])[1][0].write(r.read())
                    r.flush()
                    toshell.flush()
                else:
                    raise Exception("please slap the programmer")

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

