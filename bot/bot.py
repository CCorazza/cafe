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
        (now, NextBreak()),
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

