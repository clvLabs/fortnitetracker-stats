#!/bin/bash
docker run \
  --name fortnitetracker-stats \
  --privileged \
  -it \
  --rm \
  --network host \
  \
  --volume $(pwd)/app:/fortnitetracker-stats/app \
  --volume $(pwd)/config:/fortnitetracker-stats/config \
  --volume $(pwd)/data:/fortnitetracker-stats/data \
  \
  $1 $2 $3 $4 $5 $6 $7 $8 $9 \
  fortnitetracker-stats
