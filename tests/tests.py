from flask_testing import TestCase
from ..models import Link, db
from ..serializers import LinkSchema
from .. import create_app


class MyTest(TestCase):
    def create_app(self):
        return create_app(self)

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_wrong_link(self):
        response = self.client.post("/api/v1/Links", data=dict(url='http://example.com/'))
        self.assertEquals(response.json, dict(message='The method is not allowed for the requested URL.'))

    def test_correct_post_default_lifespan(self):
        response = self.client.post("/api/v1/links", data=dict(url='http://example.com/'))
        self.assertEquals(response.json, dict(lifespan=90, short_url='a',url='http://example.com/'))

    def test_correct_post_custom_lifespan(self):
        response = self.client.post("/api/v1/links", data=dict(url='http://example2.com/', lifespan=300))
        self.assertEquals(response.json, dict(lifespan=300, short_url='a',url='http://example2.com/'))

    def test_small_lifespan(self):
        response = self.client.post("/api/v1/links", data=dict(url='http://example2.com/', lifespan=-5))
        self.assertEquals(response.json, dict(lifespan=90,short_url='a',url='http://example2.com/'))

    def test_big_lifespan(self):
        response = self.client.post("/api/v1/links", data=dict(url='http://example2.com/', lifespan=10000))
        self.assertEquals(response.json, dict(lifespan=90,short_url='a',url='http://example2.com/'))

    def test_wrong_url(self):
        response = self.client.post("/api/v1/links", data=dict(url='blablabla', lifespan=10000))
        self.assertEquals(response.json, dict(message='Wrong input'))

    def test_short_link(self):
        for i in range(100):
            created = self.client.post("/api/v1/links", data=dict(url='http://example{}.com/'.format(i)))
            self.assertTrue(Link.query.filter_by(short_url=created.json['short_url']).first())
            response = self.client.get("/api/v1/{}".format(created.json['short_url']))
            self.assertEqual(response.status_code, 302)
            for row in Link.query.filter(Link.url == created.json['url']):
                self.assertEquals(response.headers['location'], LinkSchema().dump(row)['url'])
                self.assertRedirects(response, LinkSchema().dump(row)['url'])

    def test_wrong_short_link(self):
        response = self.client.get("/api/v1/a")
        self.assertEquals(response.json,dict(message='Looks like short url is wrong..'))

    def test_unique_url(self):
        self.client.post("/api/v1/links", data=dict(url='http://example.com/'))
        self.client.post("/api/v1/links", data=dict(url='http://example.com/'))
        self.client.post("/api/v1/links", data=dict(url='http://example.com/'))
        self.assertEquals(db.session.query(Link).count(),1)

    def test_list_of_urls(self):
        self.client.post("/api/v1/links", data=dict(url='http://example.com/'))
        self.client.post("/api/v1/links", data=dict(url='http://example2.com/'))
        response = self.client.get('/api/v1/links')
        for i, item in enumerate(response.json):
            self.assertEquals(item['id'], i+1)
