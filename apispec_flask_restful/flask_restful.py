# -*- coding: utf-8 -*-
"""Flask-RESTful plugin"""

import logging
import re

from apispec import Path, utils
from apispec.exceptions import APISpecError


def deduce_path(resource, **kwargs):
    """Find resource path using provided API or path itself"""
    api = kwargs.get('api', None)
    if not api:
        # flask-restful resource url passed
        return kwargs.get('path').path

    # flask-restful API passed
    # Require MethodView
    if not getattr(resource, 'endpoint', None):
        raise APISpecError('Flask-RESTful resource needed')

    if api.blueprint:
        # it is required to have Flask app to be able enumerate routes
        app = kwargs.get('app')
        if app:
            for rule in app.url_map.iter_rules():
                if rule.endpoint.endswith('.' + resource.endpoint):
                    break
            else:
                raise APISpecError('Cannot find blueprint resource {}'.format(resource.endpoint))
        else:
            # Application not initialized yet, fallback to path
            return kwargs.get('path').path

    else:
        for rule in api.app.url_map.iter_rules():
            if rule.endpoint == resource.endpoint:
                rule.endpoint.endswith('.' + resource.endpoint)
                break
        else:
            raise APISpecError('Cannot find resource {}'.format(resource.endpoint))

    return rule.rule


def parse_operations(resource):
    """Parse operations for each method in a flask-restful resource"""
    operations = {}
    for method in resource.methods:
        docstring = getattr(resource, method.lower()).__doc__
        if docstring:
            operation = utils.load_yaml_from_docstring(docstring)
            if not operation:
                logging.getLogger(__name__).warning(
                    'Cannot load docstring for {}/{}'.format(resource, method))
            operations[method.lower()] = operation or dict()
    return operations


def path_helper(_spec, **kwargs):
    """Extracts swagger spec from `flask-restful` methods."""
    try:
        resource = kwargs.pop('resource')

        path = deduce_path(resource, **kwargs)

        # normalize path
        path = re.sub(r'<(?:[^:<>]+:)?([^<>]+)>', r'{\1}', path)

        operations = parse_operations(resource)

        return Path(path=path, operations=operations)
    except Exception as exc:
        logging.getLogger(__name__).exception("Exception parsing APISpec %s", exc)
        raise
