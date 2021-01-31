#!/bin/bash
source app/scripts/utils.sh

log ""
log "---[ starting service ]-----------------------------"
log ""
docker-compose up \
    --detach \
    $1 $2 $3 $4 $5 $6 $7 $8 $9

# Show logs (shows its own title)
scripts/logs.sh
