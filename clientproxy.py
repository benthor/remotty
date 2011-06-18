from shellserver import ShellServer
from select import select
import sys
import os
import fcntl

if __name__ == "__main__":
    if len(sys.argv) > 1:
        import socket
        s = socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
        try:
            s.bind('\0'+sys.argv[1])
            s.listen(1)
            con = s.accept()[0]
            tosocket = os.fdopen(con.fileno(),"w")
            fromsocket = os.fdopen(con.fileno(),"r")
            for fd in [sys.stdin, con.fileno()]:
                fl = fcntl.fcntl(fd, fcntl.F_GETFL)
                fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
            while not tosocket.closed and not fromsocket.closed:
                sys.stdin.flush()
                fromsocket.flush()
                for readable in select([sys.stdin, fromsocket],[],[])[0]:
                    if readable == sys.stdin:
                        select([],[tosocket],[])[1][0].write(readable.read())
                        tosocket.flush()
                    elif readable == fromsocket:
                        select([],[sys.stdout],[])[1][0].write(readable.read())
                        sys.stdout.flush()
                    else:
                        raise Exception("Programmer now excepts letterbombs")
        except:
            raise
        finally:
            s.close()     
    else:
        sys.stderr.write("usage: python %s <socketname>\n" % sys.argv[0])

