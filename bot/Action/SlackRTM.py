from . import Action

__all__ = ["SlackRTM"]


class SlackRTM(Action):
    def __init__(self, slack, username="Serge", icon="chicken", listen=None):
        super(SlackRTM, self).__init__(3)
        self.slack = slack
        self.username = username
        self.icon = icon
        self.listen = listen or ["G03CCAS2U", "G03TJ0L4F"]

    def __call__(self, automaton):
        super(SlackRTM, self).__call__(automaton)  # We let default action take care of the recurrence.