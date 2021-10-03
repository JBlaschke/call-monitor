#!/usr/bin/env python
# -*- coding: utf-8 -*-


from socket    import gethostname
from functools import wraps
from math      import floor
from time      import perf_counter, strftime, gmtime
from inspect   import getmodule
from enum      import Enum, auto
from os        import getpid
from threading import get_ident


from ..util import Singleton


class EventType(Enum):
    """
    Event type flag.
    """

    NONE   = auto()
    CALL   = auto()
    RETURN = auto()
    PUSH   = auto()
    POP    = auto()


class Event(object):

    def __init__(self, name, module="", status=EventType.NONE, count=0):
        """
        Event(name, module="", status=EventType.NONE, count=0)
        """
        self._name   = name
        self._module = module
        self._status = status
        self._count  = count
        self._t      = perf_counter()


    @property
    def t(self):
        """
        Time the event was recorded
        """
        return self._t


    @property
    def name(self):
        """
        Name of function
        """
        return self._name


    @property
    def module(self):
        """
        Name of functions module
        """
        return self._module


    @property
    def status(self):
        """
        Event type/function call status
        """
        return self._status


    @property
    def count(self):
        """
        Function invocation count
        """
        return self._count



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


#
# Functions to operate on the singleton EventLogger
#


def event_here(name, module, status=EventType.NONE, count=0):
    """
    Enter Event into the EventLogger
    """
    EventLogger().add(Event(name, module, status, count))


def start(name, module, count):
    """
    Enter start of event into EventLogger
    """
    event_here(name, module, status=EventType.PUSH, count=count)


def stop(name, module, count):
    """
    Enter end of event into EventLogger
    """
    event_here(name, module, status=EventType.POP, count=count)


def count(name, module):
    """
    Count occurences of events
    """
    return EventLogger().count(name, module)


def event_log():
    """
    Get string representation of the event log
    """

    hostname = EventLogger().hostname
    pid      = EventLogger().pid
    tident   = EventLogger().tident

    prefix = f"{hostname},{pid},{tident}"

    for e in EventLogger().events:
        status = "none"
        if e.status == EventType.PUSH:
            status = "push"
        elif e.status == EventType.POP:
            status = "pop "
        elif e.status == EventType.CALL:
            status = "call"
        elif e.status == EventType.RETURN:
            status = "rtrn"

        if e.status in (EventType.PUSH, EventType.CALL):
            yield f"{prefix},{e.t:.16f},{status},{e.module}.{e.name}:{e.count}"
        else:
            yield f"{prefix},{e.t:.16f},{status},{e.module}.{e.name}"



#
# Decorator to log function calls
#

def log(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        name   = str(func.__name__)
        module = str(getmodule(func).__name__)

        # Calculate count number: this number tracks how many times this
        # function will have been called
        ct = count(name, module) + 1

        event_here(name, module, status=EventType.CALL, count=ct)
        ret = func(*args, **kwargs)
        event_here(name, module, status=EventType.RETURN, count=ct)

        return ret

    return wrapper
