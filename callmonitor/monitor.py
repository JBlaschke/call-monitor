#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pickle
from functools  import wraps
from .singleton import Singleton



class Counter(object, metaclass=Singleton):

    def __init__(self):
        self.reset()

    def reset(self):
        self.count = 0

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, val):
        self._count = val

    def increment(self, step=1):
        self._count += step



def intercept(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        return func(*args, **kwargs)

    return wrapper
