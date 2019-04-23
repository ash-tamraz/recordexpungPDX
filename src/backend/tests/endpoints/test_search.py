"""Test file for Flask endpoint for api/search,
`src/backend/expungeservice/endpoints/search.py`

Uses `pytest` module for testing.

"""

import pytest
import json

from flask import current_app, jsonify

import expungeservice
from expungeservice.endpoints import search

@pytest.fixture(scope='module')
def app():
  return expungeservice.create_app('development')

@pytest.fixture(scope='module')
def client(app):
  return app.test_client()

"""Borrowing some testing variables from Arun's `test_auth.py`
"""
username = 'test_user'
password = 'test_password'
email = 'test_user@test.com'

def create_user(client, username, password, email):
    return client.post('api/v0.1/users', json={
        'username': username,
        'password': password,
        'email address': email,
    })

def get_auth_token(client, username, password):
    return client.get('/api/v0.1/auth_token', json={
        'username': username,
        'password': password,
    })

def create_post_obj(client, username, password):
  """Helper function to create dict objects for sending to search.py via
  POST requests
  """
  token = get_auth_token(client, username, password)
  query_obj = {('first_name', 'foo'),
              ('last_name', 'bar'),
              ('dob', 'baz')}
  headers_obj = token.get_json()
  post_obj = {
          'query' : query_obj,
          'headers' : headers_obj
          }
  return post_obj

def test_create_user(client):
    response = create_user(client, username, password, email)
    assert(response.status_code == 201)

    data = response.get_json()
    assert(data['username'] == username)
    assert(data['email address'] == email)


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
  assert(response.status_code == 401)

def test_empty_post_wrong_request_method(client):
  """Testing error response from endpoint for POST request of `None`.
  @param client: app.test_client()
  """
  response = client.get('api/v0.1/search', None)
  assert(response.status_code == 405)

def test_empty_post_w_valid_token(client):
  """Testing error response from endpoint for POST request of `None`.
  @param client: app.test_client()
  """
  token = get_auth_token(client, 'test_user', 'test_password')
  response = client.post('/api/v0.1/search', headers={
        'Authorization': 'Bearer {}'.format(token.get_json()['auth_token'])
    })
  assert(response.status_code == 400)


def test_empty_obj_post(client):
  """Testing error response from endpoint for empty POST request.
  @param client: app.test_client()
  """
  token = get_auth_token(client, 'test_user', 'test_password')
  obj = create_post_obj(client, 'test_user', 'test_password')
#  response = client.post('api/v0.1/search', json={})
#  response = client.post('/api/v0.1/search', headers={
  print(obj)
  assert False

#  assert(response.status_code == 400)

"""I'm not sure about structure or content of object received from the POST
   request at this point. I'm assuming we will at least have fields for the
   remote site's search fields. Will we send the auth_token to ensure that 
   the sender is permitted to search the database?
"""
#def test_basic_post(client):
#  """Testing super basic response to make sure I'm understanding Flask's
#  POST request functionality correctly.
#  @param client: app.test_client()
#  """
#  post_obj = dict({('first_name', 'foo'), ('last_name', 'bar'), ('dob', 'baz'),
#      ('auth_token', 'tbd')})
#  response = client.post('api/v0.1/search', json=post_obj)
#  endpoint_response = response.get_json()
#  assert(response.status_code == 201)
#  assert(endpoint_response['data'] == 'baz')

#def test_basic_post_w_field_contents(client):
#  """Testing POST request with fields' contents filled out
#  @param client: app.test_client()
#  """
#  response = client.post('api/v0.1/search', json={
#    'first_name': 'Cool',
#    'last_name': 'Guy',
#    'dob': '00/00/0000'
#  })
#  endpoint_response = response.get_json()
#  assert(response.status_code == 201)
#  assert(endpoint_response['data'] == 'CoolGuy00/00/0000')
#
#
