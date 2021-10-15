#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import wraps
from inspect   import getfile
from os.path   import abspath

from .event        import Event, EventType
from .event_logger import EventLogger



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
            yield f"{prefix},{e.t:.16f},{status},{e.module}::{e.name}:{e.count}"
        else:
            yield f"{prefix},{e.t:.16f},{status},{e.module}::{e.name}"



#
# Decorator to log function calls
#

def log(func):
    name   = str(func.__name__)
    module = str(abspath(getfile(func)))

    @wraps(func)
    def wrapper(*args, **kwargs):
        # Calculate count number: this number tracks how many times this
        # function will have been called
        ct = count(name, module) + 1

        event_here(name, module, status=EventType.CALL, count=ct)
        ret = func(*args, **kwargs)
        event_here(name, module, status=EventType.RETURN, count=ct)

        return ret

    return wrapper
