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
from .auth import auth_required
from expungeservice.crawler.crawler import Crawler

# idea: create custom class based on MethodView which checks headers, etc.

# post request will need authentication header from auth.py endpoint
# Arun wrote decorator for authentication
class SearchQuery(MethodView):
  def __init__(self):
      self.query = None
      self.login_info = None
      self.search_results = None

  @auth_required
  def post(self):
    data = request.get_json() or None

    # Response for empty query
    if data == None or data == {}:
      abort(400)

    # Data good. Passing to `crawler.py`
    self.query = json.loads(data)

#    self.fill_login_info()
    # Testing receiving basic POST request
    # Expecting incoming POST request to have three fields, First Name,
    # Last Name, and Date of Birth (DoB)
    length = self.pass_to_crawler()
    # Send results to expunger
    return length, 201

  def pass_to_crawler(self):
    crawl = Crawler()
    # First need to log in
    crawler_login = crawl.login('username', 'password')
#    if crawler_login:
#      crawl.search(self.query['first_name'],
#              self.query['last_name'], 
#              'fiz', 
#              self.query['dob'])
    return type(crawler_login)

#  def fill_login_info(self):
#    self.login_info = {
#            'username': self.query['username'] or None,
#            'password': self.query['password'] or None
#            }

def register(app):
  # app.add_url_rules will go here
  app.add_url_rule('/api/v0.1/search', view_func=SearchQuery.as_view('search'))


