#!/bin/bash
# /etc/init.d/RecibePrint
### BEGIN INIT INFO
### END INIT INFO

case "$1" in
   start)
      echo "Starting server"
      python /usr/local/bin/recibeprint.py start 
      ;;

   stop)
      echo "Stopping server"
      python /usr/local/bin/recibeprint.py stop
      ;;

   restart)
      echo "Restarting server"
      python /usr/local/bin/recibeprint.py restart
      ;;

   *)
      echo "Usage: /etc/init.d/recibeprint.sh {start|stop|restart}"
      exit 1
      ;;
esac
exit 0