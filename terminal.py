import sys, termios, tty

class Terminal:
    """ Terminal class, convenience access to tty"""
    def __init__(self, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.d = termios.tcgetattr(self.stdin.fileno())
        self.echo = True # this is just a guess XXX
        self.raw = False # this is also just a guess XXX

    def restore(self):
        """ restore tty settings to their backed-up values """
        termios.tcsetattr(self.stdin.fileno(), termios.TCSADRAIN, self.d)
        self.echo = True # This is just a guess XXX
        self.raw = False # This is also just a guess XXX

    def setnoecho(self):
        """ shamelessly copied from
        http://docs.python.org/library/termios.html#example """
        fd = self.stdin.fileno()
        new = termios.tcgetattr(fd)
        new[3] = new[3] & ~termios.ECHO # without tilde, the reverse? XXX
        termios.tcsetattr(fd, termios.TCSADRAIN, new)
        self.echo = False

    def setraw(self):
        """ set self.stdin to raw """
        tty.setraw(self.stdin.fileno())
        self.raw = True
        
    def getchar(self):
        if not self.raw:
            raise Exception("socket not set to raw")
        return self.stdin.read(1)
        
    def putstr(self, c):
        """ TODO: find out if stdout can also be set to raw, to save on the
        explicit flushing"""
        #self.restore()
        if len(c) == 1:
            o = ord(c)
            if o == 13:
                self.stdout.write("\n")
            elif o == 127:
                self.stdout.write(chr(8))
                self.stdout.write(" ")
                self.stdout.write(chr(8))
            else:
                self.stdout.write(c)
        else:
            self.stdout.write(c)
        
        #self.stdout.write(chr(0x08))
        self.stdout.flush()
        #self.setnoecho()
        #self.setraw()


if __name__ == "__main__":
    t = Terminal()

    t.setnoecho()
    t.setraw()

    l = None
    a = None

    while a != "~" and l != ".":
        a = l
        l = t.getchar()
        t.putstr(l)

    t.restore()
