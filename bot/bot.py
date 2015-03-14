"""cafe/bot.py

Usage:
    bot.py
    bot.py start
    bot.py stop
    bot.py (-h | --help)
"""

import os

import arrow
import slacker

from Automaton import Automaton
from Action import *


def main(slack_key=os.getenv("SLACK_API_KEY", None),
         death=os.getenv("DEATH_CONTACT")):
    slack = slacker.Slacker(slack_key)
    now = arrow.now("Europe/Paris").float_timestamp

    serge = Automaton(actions=[
        # (now + 0, Action(4)),
        (now, SlackRTM(slack)),
        (now, BreakChecker()),
    ])

    message = "Ran out of actions"
    try:
        serge.run()
    except:
        import traceback

        message = traceback.format_exc()
    finally:
        if death:
            slack.chat.post_message(
                death,
                "serge = {}\n{}".format(repr(serge), message),
                username="Serge",
                icon_emoji=":chicken:",
            )


def start_daemon():
    import daemon

    with daemon.DaemonContext():
        main()


def stop_daemon():
    pass


if __name__ == "__main__":
    from docopt import docopt

    args = docopt(__doc__)
    if args.get('start', False):
        start_daemon()
    elif args.get('stop', False):
        stop_daemon()
    else:
        main()


"""
from app import db, TIMEZONE
import models

    def filter_messages(self, messages):
        for message in messages:
            if not self.in_followed_group(message):
                continue
            if not self.is_addressed(message):
                continue
            if self.is_self(message):
                continue
            yield message
        raise StopIteration


    def is_addressed(self, message):
        return 'text' in message and (message['text'].lower().startswith(self.username) or ":coffee:" in message['text'])


    def is_self(self, message):
        return 'username' in message and message['username'] == self.username


    def in_followed_group(self, message):
        return 'channel' in message and message['channel'] in self.groups


    def parse_message(self, obj):
        message = ""
        user = models.User.query.get(obj['user'])
        if not user:
            user = models.User(obj['user'])
            user.update_user()
            db.session.add(user)
            db.session.commit()
            message += "salut pour la premiere fois"

        for (hours, minutes) in re.findall(r":?coffee:?@(\d\d)(?:[:h]?(\d\d)?)", obj['text']):
            hours, minutes = int(hours), int(minutes)
            now = arrow.now(TIMEZONE)
            arw = now.replace(hour=hours, minute=minutes)
            if arw < now:
                arw.replace(day=+1)
            b = models.Break(arw.float_timestamp, user)
            user.breaks.append(b)
            db.session.add(b)
            db.session.add(user)
            db.session.commit()
            message += "cafey (id #{}) {}:{}".format(b.id, hours, minutes)

        obj.update({'user': user})
        print(obj)
        if message:
            self.slack.chat.post_message(obj['channel'],
                                         message.format(**obj),
                                         username=self.username,
                                         icon_emoji=":chicken:")


"""