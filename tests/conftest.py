#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
from flask import Flask
from flask_restful import Api


@pytest.fixture()
def app():
    _app = Flask(__name__)
    ctx = _app.test_request_context()
    ctx.push()
    yield _app
    ctx.pop()


@pytest.fixture()
def api():
    _app = Flask(__name__)
    _api = Api(_app)
    ctx = _app.test_request_context()
    ctx.push()
    yield _api
    ctx.pop()
