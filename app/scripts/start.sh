#!/bin/bash
source /fortnitetracker-stats/app/scripts/utils.sh

log "---------------------------------------------------"
log "--- fortnitetracker-stats startup"
log "--- $(date)"

log ""
log "---[ starting app ]-----------------------------"
log ""
python3 -u /fortnitetracker-stats/app/main.py

log ""
log "---[ FINISHED ]------------------------------------"
