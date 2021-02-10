#!/usr/bin/python3
import logging
import json
from datetime import datetime
from flask import jsonify
from flask import request
from flask_restful import abort, Resource

logger = logging.getLogger('APIRoute/match')

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
    class Match(Resource):
        def get(self, user, which):
            logger.debug(f"API hit: GET /api/v1/{user}/match/{which}")
            filename = f"/fortnitetracker-stats/data/{user}_matches.json"
            with open(filename, 'r') as f:
                matches = json.loads(f.read())
            # ordenamos por fecha
            matches = sorted(matches, key=lambda item: item["dateCollected"], reverse=True)
            num_match = request.args.get('pos', default = 1, type = int)
            if which == "last":
                match = matches[num_match - 1]
            elif which == "first":
                match = matches[num_match * -1]
            else:
                match = {}

            return jsonify({"match": match})

    class LastMatch(Resource):
        def get(self, user):
            logger.debug(f"API hit: GET /api/v1/{user}/match")
            m = Match()
            return m.get(user, "last")

    webapi.add_resource(LastMatch, '/api/v1/<user>/match')
    webapi.add_resource(Match, '/api/v1/<user>/match/<which>')

# @user.route('/<user_id>', defaults={'username': None})
# @user.route('/<user_id>/<username>')
# def show(user_id, username):
#     pass