#!/bin/bash
source /fortnitetracker-stats/app/scripts/utils.sh

log ""
log "---------------------------------------------------"
log "--- fortnitetracker-stats setup"
log "--- $(date)"
log "---------------------------------------------------"

log ""
log "---[ creating data folder ]-----------------------------"
log ""

mkdir --parents --verbose /fortnitetracker-stats/data

log ""
log "---[ installing system dependencies ]-----------------------------"
log ""

cat /fortnitetracker-stats/app/setup/resources/system-requirements.txt | xargs apt -y install

log ""
log "---[ installing python dependencies ]-----------------------------"
log ""

pip3 install --requirement /fortnitetracker-stats/app/setup/resources/python-requirements.txt

log ""
log "---------------------------------------------------"
log "--- fortnitetracker-stats setup FINISHED"
log "---------------------------------------------------"
