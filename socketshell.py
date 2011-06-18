from shellserver import ShellServer
import sys

if __name__ == "__main__":
    if len(sys.argv) > 1:
        import socket
        s = socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
        try:
            s.bind('\0'+sys.argv[1])
            s.listen(1)
            con = s.accept()[0]
            S = ShellServer(con.fileno(), con.fileno())
            S.run()
        except:
            # should be a bit more verbose about any errors here, but can't be
            # bothered right now
            raise
        finally:
            s.close()     
    else:
        sys.stderr.write("usage: python %s <socketname>\n" % sys.argv[0])

