#import terminal
from subprocess import Popen, PIPE, STDOUT
from select import select
import sys
import tty
import fcntl
import os
import termios

T = None

class ShellClient:
    def __init__(self, socket):
        #socket.setblocking(0)
        self.to_s = os.fdopen(socket.fileno(), "w")
        self.from_s = os.fdopen(socket.fileno(), "r")

        self.settings = termios.tcgetattr(sys.stdin.fileno())

        for fd in [sys.stdin.fileno(), socket.fileno()]:
            fl = fcntl.fcntl(fd, fcntl.F_GETFL)
            fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
        tty.setraw(sys.stdin.fileno())

    def run(self):
        # FIXME these checks don't really help
        while not sys.stdin.closed and not sys.stdout.closed and not self.to_s.closed and not self.from_s.closed:
            # this is probably just superstition
            readables = select([sys.stdin, self.from_s], [], [],T)[0]
            for readable in readables:
                if readable == sys.stdin:
                    select([],[self.to_s], [],T)[1][0].write(sys.stdin.read())
                    self.to_s.flush()
                elif readable == self.from_s:
                    select([],[sys.stdout], [],T)[1][0].write(self.from_s.read())
                    sys.stdout.flush()
                else:
                    raise Exception("Programmer now accepts letterbombs")
        print "end"

    def destroy(self):
        print "cleaning up"
        # FIXME, needs proper error handling
        termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, self.settings)
        sys.stdout.flush()
        self.to_s.flush()

if __name__ == "__main__":
    import socket
    if len(sys.argv) > 1:
        try:
            s = socket.socket(socket.AF_UNIX)
            s.connect('\0'+sys.argv[1])
            C = ShellClient(s)
            C.run()
            print "done running"
        except:
            # TODO, better handling of stuff
            raise
        finally:
            C.destroy()
            s.close()
    else:
        sys.stderr.write("usage: python %s <socketname>\n" % sys.argv[1])
