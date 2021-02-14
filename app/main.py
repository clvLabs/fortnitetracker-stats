#!/usr/bin/python3
import sys
import signal
import time
import logging
import json
from pprint import pformat

from src.profilepinger import ProfilePinger
from src.apistatsgetter import APIStatsGetter
from src.apiprofilesgetter import APIProfilesGetter
from src.webserver import WebServer

CONFIG_FILE = "/fortnitetracker-stats/config/config.json"

# ----------------------------------------------------------------------
# ---
# --- Exit signal management
# ---

def onSignal(signalNumber, frame):
    logger.warning('Received signal [{}]'.format(signal.Signals(signalNumber).name))
    logger.warning('Stopping tasks')

    if pinger:
        pinger.stop()

    if profiler:
        profiler.stop()

    if stats:
        stats.stop()

    if web:
        web.stop()

    logger.warning('Task stop FINISHED - closing')
    sys.exit(0)


def registerExitSignals():
    for s in [signal.SIGHUP, signal.SIGINT, signal.SIGQUIT, signal.SIGTERM]:
        signal.signal(s, onSignal)


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

logger.info("Registering exit signals")
registerExitSignals()

logger.info("Loading config")
with open(CONFIG_FILE) as f:
    cfg = json.load(f)

logger.info(f"Config:\n{pformat(cfg, indent=4)}")

logger.info("Initializing tasks")
pinger = ProfilePinger(cfg)
pinger.start()

profiler = APIProfilesGetter(cfg)
profiler.start()

stats = APIStatsGetter(cfg)
stats.start()

web = WebServer(cfg)
web.start()
