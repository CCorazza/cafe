from datetime import datetime

from app import db

userbreaks_table = db.Table(
    'userbreaks_table',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('break_id', db.Integer, db.ForeignKey('breaks.id'), primary_key=True),
)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    slack_id = db.Column(db.String, unique=True)
    breaks = db.relationship("Break",
                             secondary=userbreaks_table,
                             backref=db.backref("users"))

    def __init__(self, slack_id):
        self.slack_id = slack_id
        self.name = slack_id

    def __repr__(self):
        return "<User '{}'>".format(self.name)


class Break(db.Model):
    __tablename__ = "breaks"

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime, nullable=True)

    def __init__(self, start_time=None, owner=None):
        self.owner_id = owner.id if owner else None
        self.start_time = start_time if start_time else datetime.now()

    def duration(self):
        return self.end_time - self.start_time if self.end_time else None



