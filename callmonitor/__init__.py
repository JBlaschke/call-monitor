#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .version  import __version__, VERSION
from .monitor  import intercept, Context
from .files    import Loader
from .handler  import Handler, DefaultHandler, NPHandler
from .args     import ArgsHandler
from .counter  import Counter
from .registry import Registry
from .db       import DB, new, save

import numpy as np

from atexit import register



REGISTRY = Registry()
REGISTRY.add(np.ndarray, NPHandler)

CONTEXT = Context()

def save_db():
    save(CONTEXT.db)

register(save_db)
