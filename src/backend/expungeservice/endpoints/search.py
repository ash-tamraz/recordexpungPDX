"""Flask endpoint for searching the remote site. The web app will send `POST`
requests to this endpoint with search parameters in the body of the request.
This endpoint will then send a request to the remote site.

Data format TBD.

Look in slack channel for remote site login

"""

from flask.views import MethodView
from flask import request, current_app, jsonify, abort

import expungeservice
from .auth import auth_required

# idea: create custom class based on MethodView which checks headers, etc.

# post request will need authentication header from auth.py endpoint
# Arun wrote decorator for authentication
class SearchQuery(MethodView):
  @auth_required
  def post(self):
    data = request.is_json()

    response_data = {
      'data': None
    }

    # Response for empty query
    if data == None or data == {}:
      abort(400)

    # Testing receiving basic POST request
    # Expecting incoming POST request to have three fields, First Name,
    # Last Name, and Date of Birth (DoB)
    print('printing data: '+data)
    return data, 201

def register(app):
  # app.add_url_rules will go here
  app.add_url_rule('/api/v0.1/search', view_func=SearchQuery.as_view('search'))


