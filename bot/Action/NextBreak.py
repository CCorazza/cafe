from . import Action

__all__ = ["NextBreak"]


class NextBreak(Action):
    def __init__(self):
        super(NextBreak, self).__init__(0)
        self.next = None

    def __call__(self, automaton):
        pass
