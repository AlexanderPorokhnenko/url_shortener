from flask_restful import Resource, reqparse
from flask import redirect, abort, jsonify
from urllib.parse import urlparse
import datetime
from ..models import Link
from ..serializers import LinkSchema
from .. import db


class UrlView(Resource):
    def url_validator(self, url):
        result = urlparse(url)
        return all([result.scheme, result.netloc, result.path])

    def get(self):
        # for link in Link.query.all():
        #     return LinkSchema().dump(link)
        return jsonify(Link.query.all())
        # abort(400, description="Only POST method allowed")

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("url", type=str, required=True, nullable=False)
        parser.add_argument("lifespan", type=int, default=90)
        params = parser.parse_args()
        if not self.url_validator(params['url']):
            abort(422, description="Wrong input")
        if Link.query.filter_by(url=params['url']).scalar():
            return LinkSchema().dump(Link.query.filter_by(url=params['url']).first())
        if not 1 <= params['lifespan'] <= 365:
            params['lifespan'] = 90
        new_link = Link(url=params['url'], lifespan=params['lifespan'])
        db.session.add(new_link)
        db.session.flush()
        db.session.commit()
        return LinkSchema().dump(new_link)


class ShortUrlRedirect(Resource):
    def get(self, shorten):
        is_exist = Link.query.filter_by(short_url=shorten).first()
        if is_exist:
            if datetime.datetime.now() < is_exist.death_date:
                return redirect(is_exist.url)
            else:
                abort(410, description="Link has been expired")
        else:
            abort(404, description="Looks like short url is wrong..")
