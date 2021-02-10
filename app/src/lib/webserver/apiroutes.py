#!/usr/bin/python3
from .routes.api import profiles
from .routes.api import config
from .routes.api import session
from .routes.api import match

def init(cfg, webapp, webapi):
    profiles.init(cfg, webapp, webapi)
    config.init(cfg, webapp, webapi)
    session.init(cfg, webapp, webapi)
    match.init(cfg, webapp, webapi)
