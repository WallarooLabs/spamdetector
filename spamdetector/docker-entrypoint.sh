#!/bin/sh
#rm -f /tmp/spamdetector-initializer.*
cd /app && export PYTHONPATH=$PYTHONPATH:. &&\
machida --application-module spamdetector \
     --in 0.0.0.0:5555 \
     --out "$WALLAROO_SINK_HOSTPORT" \
     --metrics mui:5001 \
     --control 0.0.0.0:12500 \
     --data 0.0.0.0:12501 \
     --external 0.0.0.0:5050 \
     --cluster-initializer --ponythreads=1 \
     --ponynoblock
