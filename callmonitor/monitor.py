#!/usr/bin/env python
# -*- coding: utf-8 -*-


from functools import wraps
from .files    import ArgsHandler





def intercept(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        name = func.__name__

        handler = ArgsHandler(name)
        handler.save(args, kwargs)

        return func(*args, **kwargs)

    return wrapper
