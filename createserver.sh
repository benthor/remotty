WORKDIR="/tmp"
KEYDIR="$WORKDIR/serverkey"
DEFAULTPORT=10000
DEFAULTGWIF=$(route -n | sed -e 's/ * / /g' | grep -E "^[^ ]* 0\.0\.0\.0" | cut -d' ' -f 8)
IP=$(/sbin/ifconfig $DEFAULTGWIF | grep -o 'inet addr:[^ ]* ' | sed -e 's/[^0-9]*//')
PREFIX=$(ddate | md5sum | sed -e 's/ .*//')
HOSTNAME=$(hostname)

if ! [ -d $KEYDIR ]
then
    echo "no key dir found"
    curvecpmakekey $KEYDIR
fi

PUBKEY=$(curvecpprintkey $KEYDIR)
CMD="curvecpserver $HOSTNAME $KEYDIR $IP $DEFAULTPORT $PREFIX curvecpmessage strace $@"

echo "starting server with:"
echo $CMD

echo "start client with"
echo "$HOSTNAME $PUBKEY $IP $DEFAULTPORT $PREFIX"

$CMD 
