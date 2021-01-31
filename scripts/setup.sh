#!/bin/bash
source app/scripts/utils.sh

log ""
log "---[ installing ]-----------------------------"
log ""


log ""
log "---[ copying sample config ]-----------------------------"
log ""
cp --verbose --no-clobber --recursive sample/config .

# Build container (shows its own title)
scripts/build.sh
