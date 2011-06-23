SERVERNAME=$1; shift
SERVERKEY=$1; shift
SERVERIP=$1; shift
SERVERPORT=$1; shift
SERVERPREFIX=$1; shift

CLIENTCMD="curvecpclient $SERVERNAME $SERVERKEY $SERVERIP $SERVERPORT $SERVERPREFIX curvecpmessage -c sh -c '$@ <&6 >&7'"
echo "starting client with:"
echo $CLIENTCMD
curvecpclient $SERVERNAME $SERVERKEY $SERVERIP $SERVERPORT $SERVERPREFIX curvecpmessage -c sh -c "$@ <&6 >&7"    
