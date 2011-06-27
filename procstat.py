fields = [
        "pid",
        "comm",
        "state",
        "ppid",
        "pgrp",
        "session",
        "tty_nr",
        "tpgid",
        "flags",
        "minflt",
        "cminflt",
        "majflt",
        "cmajflt",
        "utime",
        "stime",
        "cutime",
        "cstime",
        "priority",
        "nice",
        "num_threads",
        "itrealvalue",
        "starttime",
        "vsize",
        "rss",
        "rsslim",
        "startcode",
        "endcode",
        "startstack",
        "kstkesp",
        "kstkeip",
        "signal",
        "blocked",
        "signignore",
        "sigcatch",
        "wcan",
        "nswap",
        "cnswap",
        "exit_signal",
        "processor",
        "rt_priority",
        "policy",
        "delayacct_blkio_ticks",
        "guest_time",
        "cguest_time"]

def pid(pid):
    foo = open('/proc/'+str(pid)+'/stat', 'r').read().split()
    return dict(zip(fields,foo))

if __name__ == "__main__":
    from sys import argv
    print pid(argv[1])

