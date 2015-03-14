import os
import heapq

import arrow
import slacker
from sqlalchemy.orm.exc import NoResultFound

from . import Action
from models import Break, User


__all__ = ["BreakChecker"]


class BreakChecker(Action):
    def __init__(self):
        super(BreakChecker, self).__init__(60)
        self.next = None

    def __call__(self, automaton):
        super(BreakChecker, self).__call__(automaton)
        now = arrow.now("Europe/Paris").float_timestamp
        try:
            earlier = Break.query \
                .filter(Break.start_time > now) \
                .order_by(Break.start_time) \
                .first()
        except NoResultFound:
            earlier = None
        if self.next:
            ts, ann = self.next
            if ts < now:
                self.next = None
            if earlier and earlier.start_time < ts:
                if self.next in automaton.actions._queue:
                    automaton.actions._queue.remove(self.next)
                    heapq.heapify(automaton.actions._queue)
                self.next = None
        if not self.next and earlier:
            ts = earlier.start_time
            ann = BreakAnnounce(earlier.id)
            automaton.actions.push(ts, ann)
            self.next = (ts, ann)


class BreakAnnounce(Action):
    def __init__(self, break_id, username="Serge", icon=":chicken:", slack_api_key=os.getenv("SLACK_API_KEY", None)):
        super(BreakAnnounce, self).__init__(0)
        self.break_id = break_id
        self.slack_api_key = slack_api_key
        self.username = username
        self.icon = icon

    def __call__(self, automaton):
        chat = slacker.Chat(self.slack_api_key)
        req = Break.query.get(self.break_id)
        users = map(User.slack_format, req.users)
        message = ":coffee: ! cc {}".format(", ".join(users))
        chat.post_message(req.channel, message,
                          username=self.username,
                          icon_emoji=self.icon)

