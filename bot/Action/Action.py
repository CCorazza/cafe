import arrow

__all__ = ["Action"]


class Action(object):
    """
    Example of an action that repeats itself if called with a positive integer argument
    """

    def __init__(self, recurrence=0):
        self.recurrence = recurrence

    def __call__(self, automaton):
        if self.recurrence:
            automaton.actions.push(
                arrow.now(automaton.timezone).float_timestamp + self.recurrence,
                self
            )
