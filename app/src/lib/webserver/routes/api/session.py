#!/usr/bin/python3
import logging
import json
from datetime import datetime
from datetime import timedelta
from flask import jsonify
from flask import request
from flask_restful import abort, Resource
from src.model.session import Session
from src.model.match import Match

logger = logging.getLogger('APIRoute/session')

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
    class SessionApiRoute(Resource):
        def get(self, user, which):
            logger.debug(f"API hit: GET /api/v1/{user}/session/{which}")
            filename = f"/fortnitetracker-stats/data/{user}_matches.json"
            matches = Match.from_file(filename, user)
            num_sessions = request.args.get('n', default = 1, type = int)
            sessions = self.get_sessions(user, matches, num_sessions)
            dict_sessions = [s.get_dict() for s in sessions]
            return jsonify({"session": dict_sessions})
        
        def get_sessions(self, user, matches, num_sessions):
            gap = cfg["sessions"]["gapBetweenSessions"] # gap en segundos
            sessions = []
            matches = sorted(matches, key=lambda item: item.date_collected, reverse=True) # ordenamos por fecha
            prev_match = matches[0]
            current_session = Session(user)
            i = 0

            for match in matches:
                match_date = datetime.strptime(match.date_collected, "%Y-%m-%dT%H:%M:%S.%f0")
                prev_match_date = datetime.strptime(prev_match.date_collected, "%Y-%m-%dT%H:%M:%S.%f0")
                interval = abs(prev_match_date - match_date).total_seconds() # intervalo entre matches
                if interval > gap: # encontramos el corte de sesion
                    sessions.append(current_session)
                    current_session = Session(user)
                    if len(sessions) >= num_sessions:   # ya tenemos las sesiones que nos han pedido
                        return sessions
                if current_session.game_mode != None and current_session.game_mode != match.game_mode: #encontramos cambio de modo de juego
                    sessions.append(current_session)
                    current_session = Session(user)
                    if len(sessions) >= num_sessions:   # ya tenemos las sesiones que nos han pedido
                        return sessions
                current_session.add_match(match)
                prev_match = match
                i += 1
            return sessions
        
    class LastSessionApiRoute(Resource):
        def get(self, user):
            logger.debug(f"API hit: GET /api/v1/{user}/session")
            s = SessionApiRoute()
            return s.get(user, "last")

    webapi.add_resource(LastSessionApiRoute, '/api/v1/<user>/session')
    webapi.add_resource(SessionApiRoute, '/api/v1/<user>/session/<which>')

