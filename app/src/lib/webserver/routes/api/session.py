#!/usr/bin/python3
import logging
import json
from datetime import datetime
from datetime import timedelta
from flask import jsonify
from flask import request
from flask_restful import abort, Resource
from src.model.session import Session

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
            with open(filename, 'r') as f:
                matches = json.loads(f.read())
            
            num_sessions = request.args.get('n', default = 1, type = int)
            sessions = self.get_sessions(user, matches, num_sessions)
            dict_sessions = [s.__dict__ for s in sessions]
            return jsonify({"session": dict_sessions})
        
        def get_sessions(self, user, matches, num_sessions):
            gap = 3600 # gap en segundos
            sessions = []
            # ordenamos por fecha
            matches = sorted(matches, key=lambda item: item["dateCollected"], reverse=True)
            prev_match = matches[0]
            current_session = Session(user)

            for match in matches:
                # capturamos las fechas en formato date time
                match_date = datetime.strptime(match["dateCollected"], "%Y-%m-%dT%H:%M:%S.%f0")
                prev_match_date = datetime.strptime(prev_match["dateCollected"], "%Y-%m-%dT%H:%M:%S.%f0")
                # calculamos el tiempo pasado entre dos partidas consecutivas en nuestra lista
                interval = abs(prev_match_date - match_date).seconds
                # si el intervalo es mayor que el definido para separar sesiones, añadimos la
                # sesion actual y la reseteamos
                if interval > gap:
                    sessions.append(current_session)
                    current_session = Session(user)
                    # si ya hemos llenado el array con el numero de sesiones que nos han pedido
                    # salimos y devolvemos el array
                    if len(sessions) >= num_sessions:
                        return sessions
                # Añadimos la partida actual a la sesion
                current_session.add_match(match)
                prev_match = match
            # Si nos piden mas sesiones de las que tenemos grabadas, devolvemos lo que tenemos.
            return sessions



    webapi.add_resource(SessionApiRoute, '/api/v1/<user>/session/<which>')

