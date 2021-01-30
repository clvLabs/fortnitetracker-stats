#!/bin/bash
source app/scripts/utils.sh

log ""
log "---[ stopping service ]-----------------------------"
log ""
docker-compose down \
    $1 $2 $3 $4 $5 $6 $7 $8 $9
