#!/usr/bin/env python
# -*- coding: utf-8 -*-


from os      import makedirs
from os.path import join, exists
from pickle  import dump


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
        name = func.__name__

        c = Counter()
        c.increment(name)

        dest = join("call-monitor", name, str(c.count(name)))
        if not exists(dest):
            makedirs(dest)

        with open(join(dest, "args.pkl"), "wb") as f:
            dump(args, f)

        with open(join(dest, "kwargs.pkl"), "wb") as f:
            dump(kwargs, f)

        return func(*args, **kwargs)

    return wrapper
