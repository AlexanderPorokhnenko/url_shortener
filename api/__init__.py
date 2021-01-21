from flask import Blueprint
from flask_restful import Api
from .routes import UrlView, ShortUrlRedirect


api_bp = Blueprint('api_bp', __name__)
api = Api(prefix='/api/v1')
api.add_resource(UrlView, '/links')
api.add_resource(ShortUrlRedirect, '/<shorten>')