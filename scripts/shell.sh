#!/bin/bash
source app/scripts/utils.sh

log ""
log "---[ getting a shell in the running service ]-----------------------------"
log ""
docker exec \
    --interactive \
    --tty \
    $1 $2 $3 $4 $5 $6 $7 $8 $9 \
    fortnitetracker-stats \
    bash
