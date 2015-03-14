""" Automaton
Executes timed actions based on a TimeQueue
"""

from TimeQueue import TimeQueue

import arrow
import time

__all__ = ["Automaton"]


class Automaton(object):
    def __init__(self, actions=None, timezone="Europe/Paris"):
        self.actions = TimeQueue(actions)
        self.timezone = timezone

    def __repr__(self):
        return "Automaton(actions={}, timezone={})".format(
            repr(self.actions), repr(self.timezone),
        )

    def run(self):
        while len(self.actions):
            now = arrow.now(self.timezone).float_timestamp
            if self.actions.any_earlier(now):
                for _, action in self.actions.pop_earlier(now):
                    action(self)
            else:
                (action_time, action) = self.actions.pop()
                if now < action_time:
                    time.sleep(action_time - now)
                action(self)
