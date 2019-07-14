"""Flask endpoint for searching the remote site. The web app will send `POST`
requests to this endpoint with search parameters in the body of the request.
This endpoint will then send a request to the remote site.

Data format TBD.

Look in slack channel for remote site login

"""

import json
from flask.views import MethodView
from flask.wrappers import Response
from flask import make_response, request, current_app, jsonify, abort

import expungeservice
from expungeservice.endpoints.auth import user_auth_required
from expungeservice.crawler.crawler import Crawler

class SearchQuery(MethodView):
    def __init__(self):
        self.query = None
        self.login_info = None
        self.search_results = None
        self.request = None
        self.crawler = None
        self.crawler_login = None

    # Implementing for testing purposes, so can mock responses from 
    # remote site. Use this GET method to call the Crawler's login method
    @user_auth_required
    def get(self):
        self.crawler = Crawler()

        # First need to log in

        # Can get user data from object in `self.request`, but this matches
        # user info provided to Crawler in CrawlerFactory class
        crawler_login = self.crawler.login('username', 'password')

        if not crawler_login:
          abort(Response(response='crawler login failure'+str(crawler_login), status=400)) # maybe not appropriate error code

        self.crawler_login = crawler_login
        return Response(response=str(crawler_login), status=201)

    @user_auth_required
    def post(self):

        if not self.crawler:
            abort(Response(response='post response failure, crawler object None', status=400))
           
        data = request.get_json() or None

        # Response for empty query
        if not data:
            abort(Response(response='post response failure', status=400))

        # Data good. Passing to `crawler.py`
        self.request = data

        crawler_response = jsonify(self.crawler.search(
            'john',
            'doe'
            #self.query['first_name'],
            #self.query['last_name']
        ))


        # Returning this for testing purposes
        return Response(response=crawler_response, status=201)

    def _pass_to_crawler(self):
        self.crawler = Crawler()

        # First need to log in

        # Can get user data from object in `self.request`, but this matches
        # user info provided to Crawler in CrawlerFactory class
        crawler_login = self.crawler.login('username', 'password')

        if not crawler_login:
          abort(Response(response='crawler login failure'+str(crawler_login), status=400)) # maybe not appropriate error code

        return {'hello': 'world'}
        # need to figure out best way to pass optional parameters
#        return self.crawler.search(
#            'john',
#            'doe'
#            #self.query['first_name'],
#            #self.query['last_name']
#        )


def register(app):
    #SearchQuery.crawler_init.methods = ['POST']
    # app.add_url_rules will go here
    app.add_url_rule('/api/v0.1/search', view_func=SearchQuery.as_view('search'))
#    app.add_url_rule('/api/v0.1/search/crawler_init', SearchQuery.crawler_init)


