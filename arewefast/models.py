from datetime import datetime

from sqlalchemy.dialects.postgresql import JSON

from app import db


class Model(object):

    def __init__(self, **kw):
        for key, value in kw.items():
            setattr(self, key, value)


class Report(Model, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(), index=True)
    har = db.Column(JSON)
    ref = db.Column(db.String(), index=True)  # Git commit SHA or custom name.
    created = db.Column(db.DateTime, default=datetime.now)

    __tablename__ = 'reports'

    def __repr__(self):
        return '<Report: %s: %s>' % (self.id, self.url)
