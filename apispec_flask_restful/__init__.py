# -*- coding: utf-8 -*-
from importlib.metadata import version

try:
    __version__ = version('apispec-flask-restful')
except:
    __version__ = 'unknown'

from .flask_restful import RestfulPlugin
