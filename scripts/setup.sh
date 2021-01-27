#!/bin/bash
if ! [ -f "scripts/.setup.sh" ]
then
    log "Please run this from the project folder"
    exit 1
fi

mkdir --parents logs/setup

scripts/.setup.sh 2>&1 | tee --append logs/setup/setup.log
