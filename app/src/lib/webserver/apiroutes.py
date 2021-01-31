#!/usr/bin/python3
from .routes.api import profiles
from .routes.api import config

def init(cfg, webapp, webapi):
    profiles.init(cfg, webapp, webapi)
    config.init(cfg, webapp, webapi)
