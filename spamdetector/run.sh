#!/bin/sh
export PYTHONPATH=$PYTHONPATH:.
nohup machida --application-module spamdetector \
--in 0.0.0.0:5555 \
--out 127.0.0.1:5556 \
--metrics 127.0.0.1:5001 \
--control 127.0.0.1:12500 \
--data 127.0.0.1:12501 \
--external 127.0.0.1:5050 \
--cluster-initializer --ponythreads=1 \
--ponynoblock </dev/null >machida.log 2>&1 &
