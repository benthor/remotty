#import terminal
from subprocess import Popen, PIPE, STDOUT
from select import select
import sys
#import tty
import fcntl
import pty
import os

class PTTYCommunicator:
    def __init__(self, readable, writable, *args):
        """ Start an interactive shell """
        pid, _fd = os.forkpty()
        if pid == 0:
            os.execlp(*args)
        self.fromshell = os.fdopen(_fd, "r")
        self.toshell = os.fdopen(_fd, "w")
        self.fromfd = os.fdopen(readable, "r")
        self.tofd = os.fdopen(writable, "w")
        for fd in [_fd, readable]:#, writable]:
            fl = fcntl.fcntl(fd, fcntl.F_GETFL)
            fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

    def run(self):
        fromshell,toshell,fromfd,tofd =\
        self.fromshell,self.toshell,self.fromfd,self.tofd
        while not fromshell.closed and not toshell.closed:
            # only interested in fd's which we can currently read from
            readables = select([fromshell, fromfd],[],[])[0]
            for r in readables:
                if r == fromshell:
                    # read now, because next statement might block for a while
                    data = r.read()
                    # hackish way to wait until socket becomes ready
                    # had errors when just trying to naively writing to socket
                    # select blocks until 'tofd' is ready for writing
                    # returns [[],[tofd],[]], which is unpacked by
                    # subscripts
                    select([],[tofd],[])[1][0].write(data)
                    # this IS important
                    tofd.flush()
                elif r == fromfd:
                    # analogous to above
                    data = r.read()
                    select([],[toshell],[])[1][0].write(data)
                    toshell.flush()
                else:
                    raise Exception("please slap the programmer")

if __name__ == "__main__":
    try:
        args = sys.argv[1:] or ['/bin/sh', '-i']
        if len(args) < 2:
            args.append("")
        S = PTTYCommunicator(sys.stdin.fileno(), sys.stdout.fileno(), *args)
        S.run()

    except:
        # should be a bit more verbose about any errors here, but can't be
        # bothered right now
        raise

