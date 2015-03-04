""" TimeQueue
Priority Queue based on datetime objects (arrow module)

Could probably support threading
"""

import heapq

import arrow


__all__ = ["TimeQueue"]


class TimeQueue():
    def __init__(self):
        self._queue = []

    def __len__(self):
        return self._queue.__len__()

    def push(self, datetime, item):
        arw = arrow.get(datetime)
        heapq.heappush(self._queue, (arw, item))

    def pop(self):
        _, item = heapq.heappop(self._queue)
        return item

    def pop_earlier(self, dt):
        t = arrow.get(dt)
        items = []
        try:
            item = self.pop()
        except IndexError:
            item = None
        while item and item < (t, None):
            items.append(item)
            try:
                item = self.pop()
            except IndexError:
                item = None
        if item > (t, None):
            self.push(item)
        return items
