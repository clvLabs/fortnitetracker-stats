#!/usr/bin/python3
import logging
from flask import jsonify
from flask_restful import abort, Resource

logger = logging.getLogger('APIRoute/profiles')

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
    class Profiles(Resource):
        def get(self):
            return jsonify({"profiles": cfg['profiles']})

    webapi.add_resource(Profiles, '/api/v1/profiles')
