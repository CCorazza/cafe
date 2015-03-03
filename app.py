from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    TESTING=True,
    SQLALCHEMY_DATABASE_URI="sqlite:///./cafe.sqlite3",
)
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')
db = SQLAlchemy(app)

# standard

# local
from models import *

# third-party
import arrow


TIMEZONE = "Europe/Paris"
TIME_FORMAT = "X"


@app.route('/login')
def login():
    return "ayy"


@app.route('/')
def display_next_break():
    now = arrow.now(TIMEZONE)

    last_break = Break.query.order_by(Break.start_time.desc()).first()
    if not last_break:
        return render_template("index.no_last.jade", now=now.format(TIME_FORMAT))

    break_time = arrow.get(last_break.start_time, TIMEZONE)
    break_end = arrow.get(last_break.end_time, TIMEZONE) if last_break.end_time else None

    template = 'index.jade'
    if break_time < now:
        if (break_end and break_end > now) or (not break_end and break_time.replace(hour=+1) > now):
            template = 'index.currently.jade'
        else:
            template = 'index.no_future.jade'

    return render_template(
        template,
        last_break=last_break,
        now=now.format(TIME_FORMAT),
        break_time=break_time.format(TIME_FORMAT),
        humanized=break_time.humanize(now),
        users=last_break.users,
    )


if __name__ == '__main__':
    app.run()
