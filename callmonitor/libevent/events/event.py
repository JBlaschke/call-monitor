#!/usr/bin/env python
# -*- coding: utf-8 -*-


from time      import perf_counter
from enum      import Enum, auto

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
