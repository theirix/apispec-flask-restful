# -*- coding: utf-8 -*-
import pkg_resources

try:
    __version__ = pkg_resources.get_distribution(__name__).version
except:
    __version__ = 'unknown'


def setup(spec):
    from apispec_flask_restful.flask_restful import path_helper
    spec.register_path_helper(path_helper)
