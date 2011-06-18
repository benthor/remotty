#import terminal
from subprocess import Popen, PIPE, STDOUT
from select import select
import sys
import tty
import fcntl
import os
import termios
from Queue import Queue

class ShellClient:
    def __init__(self, socket):
        #socket.setblocking(0)
        self.to_s = os.fdopen(socket.fileno(), "w")
        self.from_s = os.fdopen(socket.fileno(), "r")

        self.to_socket_q = Queue()
        self.to_stdout_q = Queue()

        self.settings = termios.tcgetattr(sys.stdin.fileno())

        for fd in [sys.stdin.fileno(), socket.fileno()]:
            fl = fcntl.fcntl(fd, fcntl.F_GETFL)
            fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
        tty.setraw(sys.stdin.fileno())

    def run(self):
        """could be significantly simplified like in the ShellServer class"""
        while not sys.stdin.closed and not sys.stdout.closed:
            # this is probably just superstition
            self.to_s.flush()
            self.from_s.flush()
            sys.stdout.flush()
            sys.stdin.flush()
            readables = select([sys.stdin, self.from_s], [], [])[0]
            for readable in readables:
                if readable == sys.stdin:
                    self.to_socket_q.put(sys.stdin.read())
                elif readable == self.from_s:
                    self.to_stdout_q.put(self.from_s.read())
                else:
                    print readable
            # TODO: maybe solve this like in ShellServer class
            if not self.to_socket_q.empty():
                # not defining, timeout, can afford to wait for socket
                # the select statement below is assumed to always return a
                # tuple of which the first element is going to be a list
                # containing the writable socket. so why not write to it?
                #print "sending..."
                select([],[self.to_s], [])[1][0].write(self.to_socket_q.get())
                self.to_s.flush()
                #print "sent"
            if not self.to_stdout_q.empty():
                #print "waiting"
                select([],[sys.stdout], [])[1][0].write(self.to_stdout_q.get())
                #print "waited"
                sys.stdout.flush()

    def destroy(self):
        print "cleaning up"
        termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, self.settings)
        sys.stdin.flush()
        #self.to_s.close()
        #self.from_s.close()
        


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
    else:
        sys.stderr.write("usage: python %s <socketname>\n" % sys.argv[1])
