import os

import slacker

from app import db


userbreaks_table = db.Table(
    'userbreaks_table',
    db.Column('user_id', db.String, db.ForeignKey('users.id'), primary_key=True),
    db.Column('break_id', db.Integer, db.ForeignKey('breaks.id'), primary_key=True),
)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    full_name = db.Column(db.String)
    breaks = db.relationship("Break",
                             secondary=userbreaks_table,
                             backref=db.backref("users"))

    def __init__(self, slack_id):
        self.id = slack_id
        # self.update_user()

    def update_user(self):
        users = slacker.Users(os.getenv("SLACK_API_KEY"))
        data = users.info(self.id)
        if data.successful:
            self.name = data.body['user']['name']
            try:
                self.full_name = data.body['user']['profile']['real_name']
            except KeyError:
                pass

    def __repr__(self):
        return "<User '{}'>".format(self.name)


class Break(db.Model):
    __tablename__ = "breaks"

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.String)
    start_time = db.Column(db.Float)
    end_time = db.Column(db.Float, nullable=True)

    def __init__(self, start_time, owner):
        self.owner_id = owner.id
        self.start_time = start_time

    def __repr__(self):
        return "<Break {}, {}>".format(self.start_time, self.owner_id)

    def duration(self):
        return self.end_time - self.start_time if self.end_time else None

