""" TimeQueue
Priority Queue based on UNIX timestamps

It could support the standard queue.PriorityQueue functionality,
but I've taken the choice of opting out, due to the lock's possible overhead.
"""

import heapq

__all__ = ["TimeQueue"]


class TimeQueue(object):
    def __init__(self, queue=None):
        self._queue = queue or []

    def __len__(self):
        return len(self._queue)

    def __repr__(self):
        return "TimeQueue({})".format(repr(self._queue))

    def push(self, ts, item):
        heapq.heappush(self._queue, (ts, item))

    def pop(self):
        return heapq.heappop(self._queue)

    def pop_earlier(self, ts):
        while True:
            try:
                stamp, item = heapq.heappop(self._queue)
            except IndexError:
                raise StopIteration
            if stamp > ts:
                self.push(stamp, item)
                raise StopIteration
            yield (stamp, item)

    def any_earlier(self, ts):
        return len(self._queue) > 0 and self._queue[0][0] < ts
