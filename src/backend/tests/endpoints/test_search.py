"""Test file for Flask endpoint for api/search,
`src/backend/expungeservice/endpoints/search.py`

Uses `pytest` module for testing.

"""

import pytest

from flask import current_app, jsonify

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

def test_empty_post(client):
  """Testing error response from endpoint for POST request of `None`.
  @param client: app.test_client()
  """
  response = client.post('api/v0.1/search', None)
  assert(response.status_code == 400)

def test_empty_obj_post(client):
  """Testing error response from endpoint for empty POST request.
  @param client: app.test_client()
  """
  response = client.post('api/v0.1/search', json={})
  assert(response.status_code == 400)

def test_basic_post(client):
  """Testing super basic response to make sure I'm understanding Flask's
  POST request functionality correctly.
  @param client: app.test_client()
  """
  response = client.post('api/v0.1/search', json={
    'first_name': 'foo',
    'last_name': 'bar',
    'dob': 'baz'
  })
  endpoint_response = response.get_json()
  assert(response.status_code == 201)
  assert(endpoint_response['data'] == 'foobarbaz')

def test_basic_post_w_field_contents(client):
  """Testing POST request with fields' contents filled out
  @param client: app.test_client()
  """
  response = client.post('api/v0.1/search', json={
    'first_name': 'Cool',
    'last_name': 'Guy',
    'dob': '00/00/0000'
  })
  endpoint_response = response.get_json()
  assert(response.status_code == 201)
  assert(endpoint_response['data'] == 'CoolGuy00/00/0000')


