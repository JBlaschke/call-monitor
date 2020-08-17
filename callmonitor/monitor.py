#!/usr/bin/env python
# -*- coding: utf-8 -*-


from os      import makedirs
from os.path import join, exists
from pickle  import dump


from functools import wraps
from .counter  import Counter





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
