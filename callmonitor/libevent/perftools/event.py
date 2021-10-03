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
        stdlib

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


    def clear(self):
        """
        Blank the event list
        """
        self._events = list()


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
    event_here(name, module, status=EventType.PUSH, count=count)



def stop(name, module, count):
    event_here(name, module, status=EventType.POP, count=count)



def event_log():

    hostname = EventLogger().hostname
    pid      = EventLogger().pid
    tident   = EventLogger().tident

    for e in EventLogger().events:
        yield f"{hostname},{pid},{tident},{e.t},{e.module}.{e.name}:{e.count}"



#
# Decorator to log function calls
#
def log(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        func_module = str(getmodule(func).__name__)
        func_name = str(func.__name__)
        event_here(func_name, func_module, status=EventType.CALL, count=0)
        ret = func(*args, **kwargs)
        event_here(func_name, func_module, status=EventType.RETURN, count=0)
        return ret

    return wrapper
