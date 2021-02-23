#!/bin/bash
source app/scripts/utils.sh

log ""
log "---[ building docker image ]-----------------------------"
log ""
docker-compose build \
    $1 $2 $3 $4 $5 $6 $7 $8 $9
