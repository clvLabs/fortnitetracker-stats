#!/bin/bash
source app/scripts/utils.sh

scripts/stop.sh

log ""
log "---[ getting last version ]-----------------------------"
log ""
git pull

scripts/build.sh
scripts/start.sh
