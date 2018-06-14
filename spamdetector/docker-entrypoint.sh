#!/bin/sh
set -x
rm -f /tmp/spamdetector-initializer.*
nc -k -p 5556 -l 127.0.0.1 > sink.log &
sleep 5
echo "NETCAT OK" | nc -w1 127.0.0.1 5556 
export PYTHONPATH=$PYTHONPATH:.
echo "EXPORT OK"
machida --application-module spamdetector \
     --in 0.0.0.0:5555 \
     --out 127.0.0.1:5556 \
     --metrics 127.0.0.1:5001 \
     --control 127.0.0.1:12500 \
     --data 127.0.0.1:12501 \
     --external 127.0.0.1:5050 \
     --cluster-initializer --ponythreads=1 \
     --ponynoblock
