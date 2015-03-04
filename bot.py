"""cafe/bot.py

Usage:
    bot.py
    bot.py start
    bot.py stop
    bot.py (-h | --help)
"""

import os

import time

import arrow
import daemon
from docopt import docopt
import slacker
from TimeQueue import TimeQueue

from app import db
from models import *

SLACK_CHANNEL = "G03CCAS2U"


class Bot():
    def __init__(self, slack_token=os.getenv("SLACK_API_KEY"), timezone="Europe/Paris"):
        self.actions = TimeQueue()
        self.slack = slacker.Slacker(slack_token)
        self.timezone = timezone
        self.groups = {}
        self.username = 'serge'

    def follow_group(self, name):
        try:
            data = self.slack.groups.history(name)
        except Exception:
            return
        try:
            latest = data.body['messages'][0]['ts']
        except IndexError:
            latest = '0'
        self.groups.update({name: latest})

    def run(self):
        while True:
            now = arrow.now(self.timezone)
            for action in self.actions.pop_earlier(now):
                action(self)
            for message in self.get_latest_messages():
                if not self.is_self(message) and self.message_match(message):
                    self.parse_message(message)
            time.sleep(7 - (arrow.now(self.timezone).timestamp - now.timestamp))

    def get_latest_messages(self):
        messages = []
        for group_name, last_message in self.groups.iteritems():
            try:
                data = self.slack.groups.history(group_name, oldest=last_message)
            except Exception as e:
                print("slacker: {}".format(e))
                continue
            if data.successful:
                chan_messages = data.body['messages']
                for cm in chan_messages:
                    cm['channel'] = group_name
                messages.extend(chan_messages)
                try:
                    latest_message = data.body['messages'][0]
                    self.groups.update({group_name: latest_message['ts']})
                except IndexError:
                    self.groups.update({group_name: last_message})
        return messages

    @staticmethod
    def message_match(message):
        if 'text' not in message:
            return False
        return "serge" in message['text'].lower() \
               or ":coffee:" in message['text']

    def parse_message(self, message):
        print(message)
        self.slack.chat.post_message(message['channel'],
                                     u"echo: `{}`".format(message['text']),
                                     username=self.username,
                                     icon_emoji=":chicken:")

    def is_self(self, message):
        if 'username' not in message:
            return False
        return message['username'] == self.username


"""
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
    """


def main():
    bot = Bot()
    bot.follow_group(SLACK_CHANNEL)
    bot.run()


def start_daemon():
    with daemon.DaemonContext():
        main()


def stop_daemon():
    pass


if __name__ == "__main__":
    args = docopt(__doc__)
    if args.get('start', False):
        start_daemon()
    elif args.get('stop', False):
        stop_daemon()
    else:
        main()
