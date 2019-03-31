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

def test_basic(client):
  """Super basic test to see if app is working at all. Will just test response
  from `hello.py` endpoint.
 
  @param client: app.test_client()
  """
  response = client.get('/hello')
  assert(response.data == b'Hello, world!')

def test_basic_post(client):
  response = client.post('api/v0.1/search', json={
    'query': 'hello world',
  })
  assert(response.status_code == 200) 
  assert(response.data == b"data received") 
