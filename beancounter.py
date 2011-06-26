from time import time
from sys import stdin, stdout, stderr, argv

EVERY=256

def dbg(*args):
    stderr.write(" ".join([str(x) for x in args])+"\n")

start = time()
counter = 0
try:
    while True:
        if stdin.closed:
            dbg("End Of Input")
            break
        if stdout.closed:
            dbg("Broken Pipe To Output")
            break
        tmp = stdin.read(EVERY)
        if not tmp:
            break
        stdout.write(tmp)
        new = time()
        elapsed = (new-start)
        dbg(elapsed)
        #start = new
        #stdin.flush()
        #stdout.flush()
except:
    dbg(time()-start)


