#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pickle
from functools  import wraps
from .singleton import Singleton



class Counter(object, metaclass=Singleton):

    def __init__(self):
        self.reset()


    def reset(self):
        self._count = {}


    def reset_key(self, key):
        self._count[key] = 0


    def count(self, key):
        if not key in self._count.keys():
            self.reset_key(key)

        return self._count[key]


    def increment(self, key):
        if not key in self._count.keys():
            self.reset_key(key)

        self._count[key] += 1



def intercept(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        return func(*args, **kwargs)

    return wrapper
