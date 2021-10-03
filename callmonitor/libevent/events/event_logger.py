#!/usr/bin/env python
# -*- coding: utf-8 -*-

from socket    import gethostname
from os        import getpid
from threading import get_ident


from ..util import Singleton
from .event import EventType



class EventLogger(object, metaclass=Singleton):

    def __init__(self, hostname=None, pid=None, tident=None):
        """
        EventLogger(hostname=None, pid=None, tident=None)
        Stores Event object in sequence, together with hostname, rank, and
        thread id. If hostname, pid, or tident are not set, they default to
        stdlib.

        The EventLogger tracks how ofter an event with the same `name` and
        `module` has been called (i.e. entered as PUSH, or CALL)

        Singleton class, use clear to reset.
        """
        self.clear()

        self._hostname = gethostname() if hostname is None else hostname
        self._pid      = getpid()      if pid      is None else pid
        self._tident   = get_ident()   if tident   is None else tident


    def add(self, evt):
        """
        Add event to ordered list of events
        """
        self._events.append(evt)
        if evt.status in (EventType.PUSH, EventType.CALL):
            self._increment(evt)


    def clear(self):
        """
        Blank the event list
        """
        self._events = list()
        self._count  = dict()


    def _increment(self, evt):
        """
        Increment count for `evt.name` in `evt.module`
        """
        key = (evt.name, evt.module)

        if not key in self._count.keys():
            self._count[key] = 0

        self._count[key] += 1


    def count(self, name, module):
        """
        Get the count for `name` in `module`
        """
        key = (name, module)

        if not key in self._count:
            return 0

        return self._count[key]


    @property
    def hostname(self):
        return self._hostname


    @property
    def pid(self):
        return self._pid


    @property
    def tident(self):
        return self._tident


    @property
    def events(self):
        return self._events


    @property
    def times(self):
        for e in self.events:
            yield e.t


    @property
    def names(self):
        for e in self.events:
            yield e.name


    @property
    def modules(self):
        for e in self.events:
            yield e.module


    @property
    def statuses(self):
        for e in self.events:
            yield e.status


    @property
    def counts(self):
        for e in self.events:
            yield e.count
