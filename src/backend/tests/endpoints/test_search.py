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
from expungeservice.crawler.crawler import Crawler
from expungeservice.crawler.request import URL
from tests.fixtures.post_login_page import PostLoginPage
from tests.fixtures.search_page_response import SearchPageResponse
from tests.fixtures.john_doe import JohnDoe
from tests.fixtures.case_details import CaseDetails

from flask import jsonify, current_app, g, request
from expungeservice.database import user
from werkzeug.security import generate_password_hash

import expungeservice
from expungeservice.endpoints import search

class TestSearch(unittest.TestCase):

    def setUp(self):
        self.email = 'pytest_user@auth_test.com'
        self.password = 'pytest_password'
        self.hashed_password = generate_password_hash(self.password)

        # API endpoint paths
        self.search_path = '/api/v0.1/search'
        self.auth_path = '/api/v0.1/auth_token'
        self.users_path = '/api/v0.1/users'

        # Mocker variables
        self.crawler = Crawler()
        self.mocker_base_url = 'https://publicaccess.courts.oregon.gov/PublicAccessLogin/'

        self.admin_email = 'pytest_admin@auth_test.com'
        self.admin_password = 'pytest_password_admin'
        self.hashed_admin_password = generate_password_hash(self.admin_password)

        self.app = expungeservice.create_app('development')
        self.client = self.app.test_client()

        with self.app.app_context():
            expungeservice.request.before()

            self.db_cleanup()
            user.create_user(g.database, self.email, self.hashed_password, False)
            user.create_user(g.database, self.admin_email, self.hashed_admin_password, True)
            expungeservice.request.teardown(None)

    def tearDown(self):
        with self.app.app_context():
            expungeservice.request.before()

            self.db_cleanup()
            expungeservice.request.teardown(None)

    def db_cleanup(self):

        cleanup_query = """DELETE FROM users where email like %(pattern)s;"""
        g.database.cursor.execute(cleanup_query, {"pattern":"%pytest%"})
        g.database.connection.commit()

    def _get_auth_token(self, email, password):
        return self.client.get(self.auth_path, json={
            'email': email,
            'password': password,
        })


    def _create_post_obj(self):
        """Helper function to create dict objects for sending to search.py via
        POST requests
        """

        query_obj = dict({('first_name', 'foo'),
            ('last_name', 'bar'),
            ('dob', 'baz')})

        user_obj = dict({
            ('email', self.email),
            ('password', self.password)
        })

        post_obj = dict({
            'query' : query_obj,
            'user' : user_obj
        })

        return post_obj

    def _create_user(self):

        new_email = "pytest_create_user@endpoint_test.com"
        new_password = "new_password"
        new_hashed_password = generate_password_hash(new_password)


        auth_response = self._get_auth_token(self.admin_email, self.admin_password)

        response = self.client.post(self.users_path, headers={
            'Authorization': 'Bearer {}'.format(auth_response.get_json()['auth_token'])},
                json = {'email':new_email,
                        'password': new_password,
                        'admin': True})



        return response

    def test_create_user_success(self):

        new_email = "pytest_create_user@endpoint_test.com"
        new_password = "new_password"
        new_hashed_password = generate_password_hash(new_password)


        auth_response = self._get_auth_token(self.admin_email, self.admin_password)

        response = self.client.post(self.users_path, headers={
            'Authorization': 'Bearer {}'.format(auth_response.get_json()['auth_token'])},
                json = {'email':new_email,
                        'password': new_password,
                        'admin': True})


        assert(response.status_code == 201)

        data = response.get_json()
        assert data['email'] == new_email
        assert data['admin'] == True
        assert data['timestamp']

    def test_search_empty_request(self):
        new_email = "pytest_create_user@endpoint_test.com"
        new_password = "new_password"
        new_hashed_password = generate_password_hash(new_password)


        auth_response = self._get_auth_token(self.admin_email, self.admin_password)
        post_obj = self._create_post_obj()
        header_obj = {
            'Authorization': 'Bearer {}'.format(auth_response.get_json()['auth_token'])
        }

        with requests_mock.Mocker() as m:
            m.post(self.mocker_base_url + 'Search.aspx?ID=100', [{'text': SearchPageResponse.RESPONSE}, {'text': JohnDoe.BLANK_RECORD}])
            response = self.client.post(self.search_path, headers=header_obj, json=post_obj)
            print("XXXresponse: ",response.get_json())
#            print(response)
        assert(False)
#            for key, value in self.crawler.result.cases.items():
#                m.get("{}{}{}".format(base_url, 'CaseDetail.aspx?CaseID=', key), text=value)
#
#            self.crawler.search('John', 'Doe')
##    self.crawler.search('John', 'Doe')

#        response = self.client.post('/api/v0.1/search', headers={
#            'Authorization': 'Bearer {}'.format(auth_response.get_json()['auth_token'])},
#                json = {'email':new_email,
#                        'password': new_password,
#                        'admin': True})
#
#        assert(response.status_code == 201)

#@pytest.fixture(scope='module')
#def app():
#  return expungeservice.create_app('development')
#
#@pytest.fixture(scope='module')
#def client(app):
#  return app.test_client()
#
#"""Borrowing some testing variables from Arun's `test_auth.py`
#"""
#email = 'pytest_create_user@endpoint_test.com'
#password = 'new_password'
#hashed_password = generate_password_hash(password)
#
#admin_email = 'pytest_admin@auth_test.com'
#admin_password = 'pytest_password_admin'
#hashed_admin_password = generate_password_hash(admin_password)
#
#search_path = 'api/v0.1/search'
#
#def test_create_user_success(client):
#            expungeservice.request.before()
#
#            user.create_user(g.database, email, hashed_password, False)
#            user.create_user(g.database, admin_email, hashed_admin_password, True)
#
#    get_auth_response = self.get_auth_token(self.admin_email, self.admin_password)
#
#    response = self.client.post('/api/v0.1/users', headers={
#        'Authorization': 'Bearer {}'.format(get_auth_response.get_json()['auth_token'])},
#            json = {'email':new_email,
#                    'password': new_password,
#                    'admin': True})
#
#
#    assert(response.status_code == 201)
#
#    data = response.get_json()
#    assert data['email'] == new_email
#    assert data['admin'] == True
#    assert data['timestamp']
#
#
#def test_basic_post_w_valid_auth_token(client):
##  """Testing super basic response to make sure I'm understanding Flask's
##  POST request functionality correctly.
##  @param client: app.test_client()
##  """
#  base_url = 'https://publicaccess.courts.oregon.gov/PublicAccessLogin/'
#  with requests_mock.Mocker() as m:
#    m.post(base_url + 'Search.aspx?ID=100', [{'text': SearchPageResponse.RESPONSE},
#    {'text': JohnDoe.BLANK_RECORD}])
#    post_obj = create_post_obj(client, username, password)
#    header_obj = create_header_obj(client, username, password)
#    response = client.post(search_path, headers=header_obj, json=post_obj)
##    self.crawler.search('John', 'Doe')
##
##  assert len(self.crawler.result.cases) == 0
#
#
