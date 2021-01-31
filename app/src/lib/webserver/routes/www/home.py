#!/usr/bin/python3
import logging
from flask import request, redirect, render_template, Response

logger = logging.getLogger('WebRoute/home')

cfg = None
webapp = None
webapi = None


def init(_cfg, _webapp, _webapi):
    global cfg, webapp, webapi

    logger.info(f"Initializing")
    cfg = _cfg
    webapp = _webapp
    webapi = _webapi
    _initRoutes()


def _initRoutes():

    # ----------------------------------------------------------------------
    @webapp.route('/', methods=['GET'])
    def getHome():
        logger.debug("Web hit: GET /")

        return render_template(
            'index.html',
            appName='fortnitetracker-stats',
            title='home' )
