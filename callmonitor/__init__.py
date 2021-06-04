#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .version  import __version__, VERSION
from .monitor  import intercept, Context
from .handler  import Handler, DefaultHandler, NPHandler
from .args     import ArgsHandler, Args
from .counter  import Counter
from .registry import Registry
from .db       import DB, new, save, load
from .settings import Settings

import numpy as np

from os     import getpid
from threading import get_ident
from atexit import register



REGISTRY = Registry()
REGISTRY.add(np.ndarray, NPHandler)

SETTINGS = Settings()
SETTINGS.enable_multi_threading(getpid(), get_ident())
CONTEXT = Context()


def save_db():
    if CONTEXT.initialized:
        CONTEXT.db.lock()
        save(CONTEXT.db)


def snapshot():
    if CONTEXT.initialized:
        # Context().new() saves the db before creating a new one
        CONTEXT.new()


def rc(multi_threading=None, pid=None, tident=None):
    if multi_threading is not None:
        if multi_threading:
            pid = getpid() if pid is None else pid
            tident = get_ident() if tident is None else tident
            SETTINGS.enable_multi_threading(pid, tident=tident)


register(save_db)
