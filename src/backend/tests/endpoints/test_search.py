"""Test file for Flask endpoint for api/search, 
`src/backend/expungeservice/endpoints/search.py`

Uses `pytest` module for testing.

"""

import pytest

from flask import current_app

import expungeservice
from expungeservice.endpoints import search

@pytest.fixture(scope='module')
def app():
  return expungeservice.create_app('development')

@pytest.fixture(scope='module')
def client(app):
  return app.test_client()


