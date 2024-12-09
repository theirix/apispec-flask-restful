# -*- coding: utf-8 -*-
import pytest
from apispec import APISpec
from flask import Blueprint
from flask_restful import Api, Resource

from apispec_flask_restful import RestfulPlugin

# pylint: disable=too-few-public-methods
# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument


@pytest.fixture()
def spec():
    return APISpec(
        title="Swagger Petstore",
        version="1.0.0",
        openapi_version="3.0.2",
        description="This is a sample Petstore server.  You can find out more "
        'about Swagger at <a href="http://swagger.wordnik.com">'
        "http://swagger.wordnik.com</a> or on irc.freenode.net, #swagger."
        'For this sample, you can use the api key "special-key" to test the'
        "authorization filters",
        plugins=[RestfulPlugin()],
    )


class TestPathHelpers:
    def test_path_from_view(self, api, spec):
        class HelloResource(Resource):
            def get(self, hello_id):
                return "hi"

        api.add_resource(HelloResource, "/hello")

        spec.path(
            resource=HelloResource,
            api=api,
            operations={"get": {"parameters": [], "responses": {"200": "..params.."}}},
        )
        assert "/hello" in spec._paths
        assert "get" in spec._paths["/hello"]
        expected = {
            "parameters": [],
            "responses": {"200": {"$ref": "#/components/responses/..params.."}},
        }
        assert spec._paths["/hello"]["get"] == expected

    def test_path_from_view_added_via_path(self, api, spec):
        class HelloResource(Resource):
            def get(self, hello_id):
                return "hi"

        api.add_resource(HelloResource, "/hello")

        spec.path(
            resource=HelloResource,
            path="/hello",
            operations={"get": {"parameters": [], "responses": {"200": "..params.."}}},
        )
        assert "/hello" in spec._paths
        assert "get" in spec._paths["/hello"]
        expected = {
            "parameters": [],
            "responses": {"200": {"$ref": "#/components/responses/..params.."}},
        }
        assert spec._paths["/hello"]["get"] == expected

    def test_path_with_multiple_methods(self, api, spec):
        class HelloResource(Resource):
            def get(self, hello_id):
                return "hi"

            def post(self, hello_id):
                pass

        api.add_resource(HelloResource, "/hello")

        spec.path(
            resource=HelloResource,
            api=api,
            # pylint: disable=use-dict-literal
            operations=dict(
                get={
                    "description": "get a greeting",
                    "responses": {"200": "..params.."},
                },
                post={
                    "description": "post a greeting",
                    "responses": {"200": "..params.."},
                },
            ),
        )
        get_op = spec._paths["/hello"]["get"]
        post_op = spec._paths["/hello"]["post"]
        assert get_op["description"] == "get a greeting"
        assert post_op["description"] == "post a greeting"

    def test_integration_with_docstring_introspection(self, api, spec):
        class HelloResource(Resource):
            def get(self, hello_id):
                """A greeting endpoint.
                ---
                x-extension: value
                description: get a greeting
                responses:
                    200:
                        description: a pet to be returned
                        schema:
                            $ref: #/definitions/Pet
                """

            def post(self, hello_id):
                """A greeting endpoint.
                ---
                x-extension: value
                description: post a greeting
                responses:
                    200:
                        description:some data
                """

        api.add_resource(HelloResource, "/hello")

        spec.path(resource=HelloResource, api=api)
        get_op = spec._paths["/hello"]["get"]
        post_op = spec._paths["/hello"]["post"]
        extension = spec._paths["/hello"]["get"]["x-extension"]
        assert get_op["description"] == "get a greeting"
        assert post_op["description"] == "post a greeting"
        assert extension == "value"

    def test_integration_invalid_docstring(self, api, spec):
        class HelloResource(Resource):
            def get(self, hello_id):
                """A greeting endpoint.
                   ---
                description: it is an invalid string in YAML
                   responses:
                       200:
                           description: a pet to be returned
                           schema:
                               $ref: #/definitions/Pet
                """

        api.add_resource(HelloResource, "/hello")

        spec.path(resource=HelloResource, api=api)
        get_op = spec._paths["/hello"]["get"]
        assert not get_op

    def test_path_is_translated_to_swagger_template(self, api, spec):
        class HelloResource(Resource):
            def get(self, hello_id):
                pass

        api.add_resource(HelloResource, "/pet/<pet_id>")

        spec.path(resource=HelloResource, api=api)
        assert "/pet/{pet_id}" in spec._paths

    def test_path_blueprint(self, app, spec):
        class HelloResource(Resource):
            def get(self, hello_id):
                return "hi"

        bp = Blueprint("bp", __name__)
        flask_api = Api(bp)
        app.register_blueprint(bp, url_prefix="/v1")
        flask_api.add_resource(HelloResource, "/hello")

        spec.path(
            resource=HelloResource,
            api=flask_api,
            app=app,
            operations={"get": {"parameters": [], "responses": {"200": "..params.."}}},
        )
        assert "/v1/hello" in spec._paths
        assert "get" in spec._paths["/v1/hello"]
        expected = {
            "parameters": [],
            "responses": {"200": {"$ref": "#/components/responses/..params.."}},
        }
        assert spec._paths["/v1/hello"]["get"] == expected

    def test_path_blueprint_no_app_fallback(self, app, spec):
        class HelloResource(Resource):
            def get(self, hello_id):
                return "hi"

        bp = Blueprint("bp", __name__)
        flask_api = Api(bp)
        app.register_blueprint(bp, url_prefix="/v1")
        flask_api.add_resource(HelloResource, "/hello")

        spec.path(
            resource=HelloResource,
            api=flask_api,
            app=None,
            path="/v1/hello",
            operations={"get": {"parameters": [], "responses": {"200": "..params.."}}},
        )
        assert "/v1/hello" in spec._paths
        assert "get" in spec._paths["/v1/hello"]
        expected = {
            "parameters": [],
            "responses": {"200": {"$ref": "#/components/responses/..params.."}},
        }
        assert spec._paths["/v1/hello"]["get"] == expected
