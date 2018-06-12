#!/bin/bash
set -e
set -o pipefail
export TERM=ansi

LOGFILE=pulumi-ec2-logs.txt

# scale :: Int -> ()
scale() {
    rm -f index.ts
    sed -e "s/@INSTANCE_COUNT@/$1/g" index.template.ts > index.ts
    tsc
}

run() {
    echo "$1" >> $LOGFILE	
    time pulumi update --yes -c never --parallel 100  2>/dev/null | tee -a "$LOGFILE"
}

rm -f "$LOGFILE"
pulumi destroy --yes --logtostderr 2>/dev/null || true
echo "STARTING at " `date` >> "$LOGFILE"

echo 'SCALING TIMES ' >> "$LOGFILE"
for i in 1 5 10 5 1 10 1; do
    scale $i && run "Scaling to $i"
done

echo 'PROVISIONING' >> "$LOGFILE"
for i in 1 5 10; do
    pulumi destroy --yes --logtostderr 2>/dev/null
    scale $i  && run "Provisioning $i"
done

echo "ENDING at " `date` >> "$LOGFILE"
