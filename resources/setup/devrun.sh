#!/bin/bash
cd __BASE_PATH__

find . \
  -type f \
  -name "*.py" \
  | sudo entr -cr \
  sudo bash -c "python3 -u __BASE_PATH__/app/main.py 2>&1 | tee -a /var/log/fortnitetracker-stats/servicelog"
