#!/usr/bin/env python
# -*- coding: utf-8 -*-


from functools import wraps
from inspect   import getfullargspec
from .files    import ArgsHandler





def intercept(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        name = func.__name__

        handler = ArgsHandler(name, argspec=getfullargspec(func))
        handler.save(args, kwargs)

        return func(*args, **kwargs)

    return wrapper
