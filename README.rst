=====================
apispec_flask_restful
=====================


Flask-RESTful plugin.

Includes a path helper that allows you to pass a Flask-RESTful resource object to `add_path`.

Inspired by AndrewPashkin/apispec_restful plugin.

Install
=======

::

    pip install apispec_flask_restful

Usage
===========

Typical usage
-------------

.. code-block:: python
    from pprint import pprint

    from flask_restful import Api, Resource
    from flask import Flask
    from apispec import APISpec

    class HelloResource(Resource):
        def get(self, hello_id):
            '''A greeting endpoint.
                   ---
                   description: get a greeting
                   responses:
                       200:
                           description: a pet to be returned
                           schema:
                               $ref: #/definitions/Pet
            '''
            pass

    app = Flask(__name__)
    api = Api(app)
    spec = APISpec(title='Spec', version='1.0', plugins=['apispec_flask_restful'])

    api.add_resource(HelloResource, '/hello')

    spec.add_path(resource=HelloResource, api=api)
    pprint(spec.to_dict()['paths'])

    # OrderedDict([('/hello',
    #          {'get': {'description': 'get a greeting',
    #                   'responses': {200: {'description': 'a pet to be returned',
    #                                       'schema': {'$ref': None}}}}})])

Without API
-----------

Method `add_path` can be invoked with a resource path in a `path` parameter instead of `api` parameter:

.. code-block:: python

        spec.add_path(resource=HelloResource, path='/hello')

With Blueprint
--------------

Flask blueprints are supported too by passing Flask app in `app` parameter:

.. code-block:: python

        spec.add_path(resource=HelloResource, api=api, app=app)

