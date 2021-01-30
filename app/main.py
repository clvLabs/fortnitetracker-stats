#!/usr/bin/python3
import sys
import time
import logging
import json

from src.profilepinger import ProfilePinger
from src.apistatsgetter import APIStatsGetter

CONFIG_FILE = "/fortnitetracker-stats/config/config.json"

# ----------------------------------------------------------------------
# ---
# --- Initialize logging before importing modules
# ---

LOGMSGFORMAT = '%(asctime)s.%(msecs)03d %(levelname)-8s [%(name)s] %(message)s'
LOGDATEFORMAT = '%Y/%m/%d %H:%M:%S'

THIRDPARTY_LOGGERS = [ 'werkzeug', 'urllib3' ]

logging.basicConfig(
    format=LOGMSGFORMAT,
    level=logging.DEBUG,
    datefmt=LOGDATEFORMAT)

lgfmt = logging.Formatter(
    fmt=LOGMSGFORMAT,
    datefmt=LOGDATEFORMAT)

logger = logging.getLogger('main')

# 3rdParty loggers - Set to show ONLY WARNINGS
for lg in THIRDPARTY_LOGGERS:
    logging.getLogger(lg).setLevel(logging.WARNING)

logger.info("-" * 50)
logger.info("Initializing")

# ----------------------------------------------------------------------

logger.info("Loading config")

with open(CONFIG_FILE) as f:
    cfg = json.load(f)

if cfg['profilePinger']['active']:
    pinger = ProfilePinger(cfg)
    pinger.start()
    time.sleep(1) # Allow a clean startup in the logs :)
else:
    logger.warning("Skipping ProfilePinger (deactivated)")

if cfg['apiStatsGetter']['active']:
    stats = APIStatsGetter(cfg)
    stats.start()
else:
    logger.warning("Skipping APIStatsGetter (deactivated)")

# While web service is not added we need a loop...
while True:
    time.sleep(100)

# serviceport = int(cfg['webPort'])
# logger.info(f"Starting web server on port {serviceport}")
# api.webapp.run(host='0.0.0.0', port=serviceport)
