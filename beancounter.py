from time import time
from sys import stdin, stdout, stderr, argv, exit
from os import getpid
import procstat
import cpu


EVERY=int(argv[1])
SKIP=int(argv[2])
PID=getpid()

def dbg(*args):
    stderr.write(", ".join([str(x) for x in args])+"\n")

def stats():
    #r = cpu.relative(cpu.stat())
    r = cpu.stat()
    for pid in [PID]+argv[3:]:
        d = procstat.pid(pid)
        r+=[
                d["comm"],
                int(d["minflt"]),
                int(d["majflt"]),
                int(d["utime"]),
                int(d["stime"])]

    return r


        

start = time()
cpustart = stats()
skip = 0
elapsed = 0
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
            elapsed += delta
            newcpu = stats()
            cpuelapsed = []
            for x,y in zip(cpustart,newcpu):
                if type(x) == int:
                    cpuelapsed.append(y-x)
                else:
                    cpuelapsed.append(x)
            cpustart = newcpu
            dbg(elapsed, EVERY*SKIP/delta, *cpuelapsed)
            start = new
except:
    pass
    #raise


