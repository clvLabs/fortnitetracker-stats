#!/usr/bin/python3
from .routes.www import home

def init(cfg, webapp, webapi):
    home.init(cfg, webapp, webapi)
