#!/usr/bin/env python
# -*- coding: utf-8 -*-



from os      import makedirs
from os.path import join, exists
from pickle  import dump, load

import numpy as np

from .counter import Counter



class HasNoRoot(Exception):
    """Has No Root"""
    pass



class Handler(object):

    def __init__(self, dest, target):
        self._dest     = dest
        self._target   = target
        self._has_root = False


    @property
    def has_root(self):
        return self._has_root


    @property
    def root(self):
        if self.has_root:
            return self._root
        else:
            raise HasNoRoot


    @root.setter
    def root(self, val):
        self._root = val
        self._has_root = True


    @property
    def dest(self):
        if self.has_root:
            return join(self.root, self._dest)
        else:
            return self._dest


    @property
    def target(self):
        return self._target



class NPHandler(Handler):

    def load(self):
        return np.load(join(self.dest, f"arg_{self.target}.npy"))


    def save(self, data):
        np.save(join(self.dest, f"arg_{self.target}.npy"), data)



class ArgsHandler(object):

    def __init__(self, name, argspec=None):
        c = Counter()
        c.increment(name)

        self.dest = join("call-monitor", name, str(c.count(name)))
        if not exists(self.dest):
            makedirs(self.dest)

        self._has_argspec = False
        if argspec is not None:
            self._has_argspec = True
            self.argspec = argspec


    @staticmethod
    def types(args, kwargs):
        args_types   = [type(a) for a in args]
        kwargs_types = {kw: type(kwargs[kw]) for kw in kwargs}
        return args_types, kwargs_types


    def filter(self, type_arg):
        if type_arg is np.ndarray:
            return False

        return True


    def save(self, args, kwargs):
        types, kwtypes = self.types(args, kwargs)

        pickle_mask = list()
        for i, (a, t) in enumerate(zip(args, types)):
            if self.filter(t):
                pickle_mask.append(a)
            else:
                h = NPHandler(self.dest, i)
                pickle_mask.append(h)
                h.save(a)

        pickle_kwmask = dict()
        for kw in kwtypes:
            if self.filter(kwtypes[kw]):
                pickle_kwmask[kw] = kwargs[kw]
            else:
                h = NPHandler(self.dest, kw)
                pickle_kwmask[kw] = h
                h.save(kwargs[kw])

        with open(join(self.dest, "args.pkl"), "wb") as f:
            dump(pickle_mask, f)

        with open(join(self.dest, "kwargs.pkl"), "wb") as f:
            dump(pickle_kwmask, f)

        if self._has_argspec:
            with open(join(self.dest, "argspec.pkl"), "wb") as f:
                dump(self.argspec, f)



class ArgspecUnknown(Exception):
    """Argspec not known."""
    pass



class Loader(object):

    def __init__(self, name, count, root=None):

        self._dest = join("call-monitor", name, str(count))
        self._has_root = False
        if root is not None:
            self.root = root

        self._has_argspec = False
        if exists(join(self.dest, "argspec.pkl")):
            self._has_argspec = True
            with open(join(self.dest, "argspec.pkl"), "rb") as f:
                self._argspec = load(f)


    @property
    def argspec(self):
        if self._has_argspec:
            return self._argspec
        else:
            raise ArgspecUnknown


    @property
    def has_root(self):
        return self._has_root


    @property
    def root(self):
        if self.has_root:
            return self._root
        else:
            raise HasNoRoot


    @root.setter
    def root(self, val):
        self._root = val
        self._has_root = True


    @property
    def dest(self):
        if self.has_root:
            return join(self.root, self._dest)
        else:
            return self._dest


    def load(self):

        with open(join(self.dest, "args.pkl"), "rb") as f:
            args = load(f)
            for i, arg in enumerate(args):
                if isinstance(arg, Handler):
                    if self.has_root:
                        arg.root = self.root
                    args[i] = arg.load()


        with open(join(self.dest, "kwargs.pkl"), "rb") as f:
            kwargs = load(f)
            for kw in kwargs:
                if isinstance(kwargs[kw], Handler):
                    kwargs[kw] = kwargs[kw].load()

        return args, kwargs
