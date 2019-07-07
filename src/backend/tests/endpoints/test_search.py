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

        # User info for testing
        self.email = 'pytest_user@auth_test.com'
        self.password = 'pytest_password'
        self.hashed_password = generate_password_hash(self.password)

        self.admin_email = 'pytest_admin@auth_test.com'
        self.admin_password = 'pytest_password_admin'
        self.hashed_admin_password = generate_password_hash(self.admin_password)

        # API endpoint paths
        self.search_path = '/api/v0.1/search'
        self.auth_path = '/api/v0.1/auth_token'
        self.users_path = '/api/v0.1/users'

        # Mocker variables
        self.crawler = Crawler()
        self.mocker_base_url = 'https://publicaccess.courts.oregon.gov/PublicAccessLogin/'
        self.record = JohnDoe.RECORD_WITH_CLOSED_CASES
        self.cases = {'X0001': CaseDetails.case_x(),
                      'X0002': CaseDetails.case_x(),
                      'X0003': CaseDetails.case_x()}

        # Flask and Werkzeug classes
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
            m.post(URL.login_url(), text=PostLoginPage.POST_LOGIN_PAGE)
            m.post('https://publicaccess.courts.oregon.gov/PublicAccessLogin/login.aspx',
                [{'text': SearchPageResponse.RESPONSE}, {'text': JohnDoe.BLANK_RECORD}])

            for key, value in self.cases.items():
                m.get("{}{}{}".format('https://publicaccess.courts.oregon.gov/PublicAccessLogin/login.aspx', 'CaseDetail.aspx?CaseID=', key), text=value)

            response = self.client.post(self.search_path, headers=header_obj, json=post_obj)
            print("DEBUGresponse: ", response.data)

        # Ensuring failure in order to get output from print statement above
        assert(False)

