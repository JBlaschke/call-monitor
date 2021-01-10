#!/usr/bin/env python
# -*- coding: utf-8 -*-


from functools  import wraps
from inspect    import getfullargspec, signature
from .args      import ArgsHandler
from .singleton import Singleton
from .db        import DB, new, save
from .settings  import Settings



class DBNotInitialized(Exception):
    pass



class Context(object, metaclass=Singleton):

    def __init__(self):
        self._initialized = False


    @property
    def initialized(self):
        return self._initialized


    @property
    def db(self):
        if not self.initialized:
            raise DBNotInitialized

        return self._db


    def new(self):
        self.db.lock()
        save(self.db)

        self.init()


    def init(self):
        settings = Settings()
        self._db = DB(root=f"call-monitor{settings.tid_tag}")
        new(self._db)

        self._initialized = True



def intercept(func, spec=None):

    spec = getfullargspec(func)
    name = func.__name__

    @wraps(func)
    def wrapper(*args, **kwargs):

        context = Context()
        handler = ArgsHandler(name, spec)

        if not context.initialized:
            context.init()

        context.db.log(name, handler.save(args, kwargs))

        return func(*args, **kwargs)

    wrapper.__signature__ = signature(func)

    return wrapper
