#!/bin/sh
nc -vv -kl -p 5556 > /out/sink.log 2>&1
