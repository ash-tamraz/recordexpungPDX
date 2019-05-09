"""Test file for Flask endpoint for api/search,
`src/backend/expungeservice/endpoints/search.py`

Uses `pytest` module for testing.

"""
import unittest
import requests_mock
import jwt
import pytest
import json

"""Modules borrowed from Nick's test file `test_crawler.py` for testing 
response from Crawler's search method
"""
from tests.fixtures.post_login_page import PostLoginPage
from tests.fixtures.search_page_response import SearchPageResponse
from tests.fixtures.john_doe import JohnDoe
from tests.fixtures.case_details import CaseDetails

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

search_path = 'api/v0.1/search'

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
  query_obj = dict({('first_name', 'foo'),
              ('last_name', 'bar'),
              ('dob', 'baz')})
  return json.dumps(query_obj)

def create_header_obj(client, username, password):
  token = get_auth_token(client, username, password)
  return dict({('Authorization', 'Bearer {}'.format(token.get_json()['auth_token']))})

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

def test_empty_obj_post_wo_valid_token(client):
  """Testing error response from endpoint for empty POST request.
  @param client: app.test_client()
  """
  response = client.post(search_path, headers={}, json={})
  assert(response.status_code == 401)

def test_empty_obj_post_w_valid_token(client):
  """Testing error response from endpoint for empty POST request.
  @param client: app.test_client()
  """
  header_obj = create_header_obj(client, username, password)
  response = client.post(search_path, headers=header_obj, json={})
  assert(response.status_code == 400)

#"""I'm not sure about structure or content of object received from the POST
#   request at this point. I'm assuming we will at least have fields for the
#   remote site's search fields. Will we send the auth_token to ensure that 
#   the sender is permitted to search the database?
#"""
def test_basic_post_w_valid_auth_token(client):
#  """Testing super basic response to make sure I'm understanding Flask's
#  POST request functionality correctly.
#  @param client: app.test_client()
#  """
  base_url = 'https://publicaccess.courts.oregon.gov/PublicAccessLogin/'
  with requests_mock.Mocker() as m:
    m.post(base_url + 'Search.aspx?ID=100', [{'text': SearchPageResponse.RESPONSE},
    {'text': JohnDoe.BLANK_RECORD}])
    post_obj = create_post_obj(client, username, password)
    header_obj = create_header_obj(client, username, password)
    response = client.post(search_path, headers=header_obj, json=post_obj)
#    self.crawler.search('John', 'Doe')
#
#  assert len(self.crawler.result.cases) == 0

#  post_obj = create_post_obj(client, username, password)
#  header_obj = create_header_obj(client, username, password)
#  response = client.post(search_path, headers=header_obj, json=post_obj)
#  assert(response.status_code == 201)
##  assert(json.loads(response.get_json())['first_name'] == 'foo')
#  assert("Crawler search passed foobarfizbaz" == response.get_json())
#



