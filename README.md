# remotty #

This is a collection of python tools to expose a pseudo tty (ptty) to file descriptors (and therby, possibly sockets), e.g., allowing for largely transport-agnostic "remote shells". 

Although somewhat general-purpose, these tools are originally intended to provide a curvecp-enabled remote ptty. See below for examples pertaining to that use-case.

## pttypipe.py ##

If invoked directly (i.e., not as a module) pttypipe.py will fork a ptty, redirecting stdin and stdout to and from it. If  invoked without any arguments, an interactive <code>/bin/sh</code> will be automatically attached to the ptty.

## socketserver.py ##

This tool will redirect its stdin to a named UNIX socket and echo everything it reads from this socket to stdout. The socket will be created automatically in kernel memory, however its name has to be unique

    usage: python socketserver.py NAME

## socketclient.py ##

This is the counterpart to the socketserver. It will echo everything it reads from the named socket to stdout and send everything read from stdin back to the socket

    usage: python socketclient.py NAME

## Testing ##

In one termial, do:

    mkfifo to_ptty.fifo
    cat to_ptty.fifo | python pttypipe.py /bin/bash | python socketserver.py SPAM >to_ptty.fifo

In another terminal, you can now attach the socketclient to the SPAM socket and enjoy your "remote" shell.

    python socketclient.py SPAM

## CurveCP Testing ##

Here is how you might use these tools to rig up a simple SSH-replacement using CurveCP. Adapted from the CurveCP README:

    curvecpmakekey serverkey
    curvecpprintkey serverkey > serverkey.hex
    curvecpserver this.machine.name serverkey 127.0.0.1 10000 31415926535897932384626433832795 curvecpmessage sh -c "python pttypipe.py /bin/bash" 

In another terminal, do:

    curvecpclient this.machine.name `cat serverkey.hex` 127.0.0.1 10000 31415926535897932384626433832795 curvecpmessage -c sh -c "python socketserver.py SPAM <&6 >&7"

Tabe care that the "serverkey.hex" is accessible from the second terminal.

In a third terminal, you can test your "remote" CurveCP shell:

    python socketclient.py SPAM


## Known Bugs And Problems ##

_LOADS. I am serious, this is very immature software, by any reasonable standard_

  * My file-descriptor magic doesn't appear to want to work on FreeBSD. Fork me!
  * socketclient.py and socketserver.py just agnostically copy whatever stdin/stdout says back and forth. Ctrl+C or Ctrl+D will not work as expected. (But will work as expected in the ptty if a pttypipe is connected to the socketserver)
  * In the above example, if the process executing in a ptty is aborted, the client is sent into a busyloop and will only terminate if the server dies as well. Yes this is a bug, which I have yet failed to resolve. Fork me!
  * Proper error handling is missing in many cases, mostly due to my own ignorance about what needs to be checked. Fork me!
  * I am probably doing a _lot_ of things wrong with sockets and file descriptors, simply by not knowing any better. Fork me!
