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

from atexit import register



REGISTRY = Registry()
REGISTRY.add(np.ndarray, NPHandler)


try:
    from mpi4py import MPI
    settings = Settings()
    if MPI.COMM_WORLD.Get_size() > 1:
        settings.enable_multi_threading(MPI.COMM_WORLD.Get_rank())
except ImportError:
    pass


CONTEXT = Context()

def save_db():
    if CONTEXT.initialized:
        # Context().new() saves the db before creating a new one
        CONTEXT.new()

register(save_db)
