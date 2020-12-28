#!/usr/bin/env python
# -*- coding: utf-8 -*-


from functools  import wraps
from inspect    import getfullargspec
from .args      import ArgsHandler
from .singleton import Singleton
from .db        import DB, new, save
from .settings  import Settings



class Context(object, metaclass=Singleton):

    def __init__(self):

        settings = Settings()
        print(settings.multi_threading_enabled)

        self._db = DB(root=f"call-monitor{settings.tid_tag}")
        new(self.db)


    @property
    def db(self):
        return self._db


    def new(self):
        save(self.db)
        new(self.db)



def intercept(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        name = func.__name__

        context = Context()
        handler = ArgsHandler(name, getfullargspec(func))

        context.db.log(name, handler.save(args, kwargs))

        return func(*args, **kwargs)

    return wrapper
