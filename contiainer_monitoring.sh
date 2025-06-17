#!/bin/bash

CONTAINER_NAME="django_server"
LOG_FILE="usage_logs.csv"

echo "Logging resource usage for container: $CONTAINER_NAME"
echo "Timestamp, CPU %, Mem Usage / Limit, Mem %, Net I/O, Block I/O" > $LOG_FILE

while true; do
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    STATS=$(docker stats --no-stream --format "{{.Name}}, {{.CPUPerc}}, {{.MemUsage}}, {{.MemPerc}}, {{.NetIO}}, {{.BlockIO}}" $CONTAINER_NAME)
    echo "$TIMESTAMP, $STATS" >> $LOG_FILE
    sleep 10
done
