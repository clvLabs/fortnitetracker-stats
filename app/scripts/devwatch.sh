#!/bin/bash
source /fortnitetracker-stats/app/scripts/utils.sh

log "---------------------------------------------------"
log "--- fortnitetracker-stats dev watch startup"
log "--- $(date)"

log ""
log "---[ starting app in dev watch mode ]-----------------------------"
log ""
find /fortnitetracker-stats/app -name "*.py" -o  -name "*.html" | entr -cr python3 -u /fortnitetracker-stats/app/main.py

log ""
log "---[ FINISHED ]------------------------------------"
