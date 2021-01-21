import string
import datetime
from . import db


class Link(db.Model):
    __tablename__ = 'Links'
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(80), nullable=False, unique=True)
    short_url = db.Column(db.String(4), unique=True, nullable=False)
    death_date = db.Column(db.DateTime)
    lifespan = db.Column(db.Integer, default=90)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        next_id = 0
        for rawitem in db.session.execute("SELECT name, seq from sqlite_sequence"):
            for link, link_id in rawitem.items():
                next_id = link_id
        self.short_url = self.encode(next_id)
        self.death_date= datetime.datetime.now()+datetime.timedelta(days=self.lifespan)

    def encode(self, num):
        alphabet = string.ascii_letters + string.digits
        if num == 0:
            return alphabet[0]
        arr = []
        arr_append = arr.append
        _divmod = divmod
        base = len(alphabet)
        while num:
            num, rem = _divmod(num, base)
            arr_append(alphabet[rem])
        arr.reverse()
        return ''.join(arr)

    def __repr__(self):
        return '{URL: {}, short_URL: {}, lifespan: {}}'.format(self.url, self.short_url, self.lifespan)
