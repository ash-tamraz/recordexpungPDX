"""Flask endpoint for searching the remote site. The web app will send `POST` 
requests to this endpoint with search parameters in the body of the request.
This endpoint will then send a request to the remote site.

Data format TBD.

"""

from flask.views import MethodView
from flask import request, current_app

class SearchQuery(MethodView):
  def post(self):
    data = request.get_json()
    return "data received" 


def register(app):
  # app.add_url_rules will go here
  app.add_url_rule('/api/v0.1/search', view_func=SearchQuery.as_view('search'))


