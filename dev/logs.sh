#!/bin/bash
source app/scripts/utils.sh

log ""
log "---[ showing service logs ]-----------------------------"
log ""
docker logs \
    --follow \
    fortnitetracker-stats \
    $1 $2 $3 $4 $5 $6 $7 $8 $9
