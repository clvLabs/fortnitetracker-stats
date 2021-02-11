#!/usr/bin/python3
import logging
import json
from datetime import datetime
from flask import jsonify
from flask import request
from flask_restful import abort, Resource
from src.model.match import Match

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
    class MatchApiRoute(Resource):
        def get(self, user, which):
            logger.debug(f"API hit: GET /api/v1/{user}/match/{which}")
            filename = f"/fortnitetracker-stats/data/{user}_matches.json"
            matches = Match.from_file(filename, user)
            matches = sorted(matches, key=lambda item: item.date_collected, reverse=True) # ordenamos por fecha
            num_match = request.args.get('pos', default = 1, type = int)
            if which == "last":
                match = matches[num_match - 1]
            elif which == "first":
                match = matches[num_match * -1]
            else:
                match = {}

            return jsonify({"match": match.get_dict()})

    class LastMatchApiRoute(Resource):
        def get(self, user):
            logger.debug(f"API hit: GET /api/v1/{user}/match")
            m = MatchApiRoute()
            return m.get(user, "last")

    webapi.add_resource(LastMatchApiRoute, '/api/v1/<user>/match')
    webapi.add_resource(MatchApiRoute, '/api/v1/<user>/match/<which>')

# @user.route('/<user_id>', defaults={'username': None})
# @user.route('/<user_id>/<username>')
# def show(user_id, username):
#     pass