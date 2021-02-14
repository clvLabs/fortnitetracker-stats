#!/usr/bin/python3
import logging
from flask import jsonify
from flask_restful import abort, Resource
from src.model.profile import Profile

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
    class ProfilesApiRoute(Resource):
        def get(self):
            logger.debug("API hit: GET /api/v1/profiles")

            return jsonify({"profiles": cfg['profiles']})


    class UserProfileApiRoute(Resource):
        def get(self, user):
            logger.debug(f"API hit: GET /api/v1/{user}/profile")
            filename_trn = f"/fortnitetracker-stats/data/{user}_trn_profile.json"
            filename_fapi = f"/fortnitetracker-stats/data/{user}_fortnite-api_profile.json"
            profile = Profile.from_files(filename_trn, filename_fapi)

            return jsonify({"profile": profile.get_dict()})

    
    webapi.add_resource(ProfilesApiRoute, '/api/v1/profiles')
    webapi.add_resource(UserProfileApiRoute, '/api/v1/<user>/profile')
