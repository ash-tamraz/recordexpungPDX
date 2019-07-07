"""Flask endpoint for searching the remote site. The web app will send `POST`
requests to this endpoint with search parameters in the body of the request.
This endpoint will then send a request to the remote site.

Data format TBD.

Look in slack channel for remote site login

"""

import json
from flask.views import MethodView
from flask import request, current_app, jsonify, abort

import expungeservice
from expungeservice.endpoints.auth import user_auth_required
from expungeservice.crawler.crawler import Crawler

class SearchQuery(MethodView):
    def __init__(self):
        self.query = None
        self.login_info = None
        self.search_results = None
        self.request = None

    @user_auth_required
    def post(self):
        data = request.get_json() or None

        # Response for empty query
        if data == None or data == {}:
            abort(400)

        # Data good. Passing to `crawler.py`
        self.request = data

        crawler_response = self.pass_to_crawler()

        # Returning this for testing purposes
        return jsonify(crawler_response), 201

    def pass_to_crawler(self):
        crawl = Crawler()

        # First need to log in

        # Can get user data from object in `self.request`, but this matches
        # user info provided to Crawler in CrawlerFactory class
        crawler_login = crawl.login('username', 'password')

        # Search logic, TBD

        return crawler_login

def register(app):
    # app.add_url_rules will go here
    app.add_url_rule('/api/v0.1/search', view_func=SearchQuery.as_view('search'))


