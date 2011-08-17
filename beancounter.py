from time import time
from sys import stdin, stdout, stderr, argv, exit
import cpu


EVERY=int(argv[1])
SKIP=int(argv[2])

def dbg(*args):
    stderr.write(", ".join([str(x) for x in args])+"\n")


start = time()
skip = 0
counter = 0 
cpu.relative(cpu.stat())
seconds = 0
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
        stdout.flush()
        skip += 1
        if skip % SKIP == 0:
            skip = 0
            new = time()
            delta = (new-start)
            seconds += delta
            dbg(seconds, EVERY*SKIP/delta, *cpu.relative(cpu.stat()))
            start = new
except:
    #pass
    raise


