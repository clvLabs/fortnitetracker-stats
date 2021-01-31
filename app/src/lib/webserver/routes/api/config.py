#!/usr/bin/python3
import logging
import json
from flask import jsonify
from flask_restful import abort, Resource

logger = logging.getLogger('APIRoute/config')

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
    class Config(Resource):
        def get(self):
            logger.debug("API hit: GET /api/v1/config")

            # Deep-copy json object
            configcopy = json.loads(json.dumps(cfg))

            # Remove sensitive info
            del configcopy['fortniteTracker']['api']['key']

            return jsonify({"config": configcopy})

    webapi.add_resource(Config, '/api/v1/config')
