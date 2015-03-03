"""cafe/bot.py

Usage:
    bot.py
    bot.py start
    bot.py stop
    bot.py (-h | --help)
"""

import datetime
import os
from dateutil import tz
import time

import daemon
from docopt import docopt
import slacker

from app import db
from models import *

SLACK_CHANNEL = "G03CCAS2U"


def main_loop():
    global slack
    slack = slacker.Slacker(os.getenv("SLACK_API_KEY"))
    _, oldest = get_last_messages(SLACK_CHANNEL, 0)
    while True:
        msgs, oldest = get_last_messages(SLACK_CHANNEL, oldest)
        map(parse_message, msgs)
        time.sleep(10)


def parse_message(msg):
    text = msg['text']
    if text.startswith("serge:") or text.startswith(":coffee:"):
        slack.chat.post_message(SLACK_CHANNEL,
                                "j'ai compris: `{}`".format(text),
                                username="serge",
                                icon_emoji=":chicken:")
        try:
            t = datetime.strptime(text[-5:], "%H:%M")
            dt = datetime.now(tz.gettz("Europe/Paris")).replace(hour=t.hour, minute=t.minute)
            b = Break(dt)
            db.session.add(b)
            db.session.commit()
            slack.chat.post_message(SLACK_CHANNEL,
                                    "OK BOYOoo, cafey a cette heure: {} :'D".format(dt.strftime("%H:%M")),
                                    username="serge",
                                    icon_emoji=":chicken:")
        except ValueError:
            pass
    print text
    return True


def get_last_messages(channel, prev_old):
    messages = []
    old = 0
    try:
        data = slack.groups.history(channel, oldest=prev_old)
    except:
        return [], prev_old
    try:
        if data.successful:
            messages = data.body['messages']
            old = messages[0]['ts']
    except IndexError, KeyError:
        return [], prev_old
    return messages, old


def start_daemon():
    with daemon.DaemonContext():
        main_loop()
    return


def stop_daemon():
    return


if __name__ == "__main__":
    args = docopt(__doc__)
    if args.get('start', False):
        start_daemon()
    elif args.get('stop', False):
        stop_daemon()
    else:
        main_loop()
