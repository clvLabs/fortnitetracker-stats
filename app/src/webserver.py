#!/usr/bin/env python3
import os
import logging
from flask import Flask
from flask_restful import Api

from .lib.webserver import apiroutes
from .lib.webserver import webroutes


class FlaskConfig(object):
  SECRET_KEY = os.urandom(24).hex()


class WebServer():

    def __init__(self, cfg):
        self.log = logging.getLogger('WebServer')
        self.log.info("Initializing")
        self.cfg = cfg


    def start(self):
        if not self.cfg['webServer']['enabled']:
            self.log.warning("Skipping start (disabled in config)")
            return

        serviceport = self.cfg['webServer']['servicePort']
        self.log.info(f"Starting service on port {serviceport}")

        # self.webapp = Flask('fortnitetracker-stats')
        self.webapp = Flask(__name__)
        self.webapp.config.from_object(FlaskConfig)
        self.webapi = Api(self.webapp)

        apiroutes.init(self.cfg, self.webapp, self.webapi)
        webroutes.init(self.cfg, self.webapp, self.webapi)

        # Warning! The main thread WILL LOCK HERE !
        # The sys.exit(0) on main.onSignal() will stop it when needed
        self.webapp.run(host='0.0.0.0', port=serviceport)


    def stop(self):
        if self.cfg['webServer']['enabled']:
            # Web server can't be stopped, we'll rely on main.onSignal()'s sys.exit(0)
            self.log.info(f"Stopping service")
