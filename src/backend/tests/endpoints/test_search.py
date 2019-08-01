"""Test file for Flask endpoint for api/search,
`src/backend/expungeservice/endpoints/search.py`

Uses `pytest` module for testing.

"""
import unittest

from unittest.mock import MagicMock

import expungeservice
from expungeservice.crawler.crawler import Crawler


class TestSearchEndpoint(unittest.TestCase):

    def setUp(self):
        app = expungeservice.create_app('development')
        self.client = app.test_client()
        self.header_obj = {
            'Authorization': 'Bearer {}'
        }

    def test_successful_search(self):

        # Create crawler instance
        crawler_stub = Crawler()

        # stub crawler login method with specified arguments
        crawler_stub.login = MagicMock(return_value=True)
        crawler_stub.login('username', 'password')

        # stub cralwer search method with specified arguments
        crawler_stub.search = MagicMock(return_value=True)
        crawler_stub.search('john', 'doe')

        # Call endpoint
        response = self.client.post('/api/v0.1/search', headers=self.header_obj)

        assert b'success' in response.data
