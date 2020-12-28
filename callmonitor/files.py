#!/usr/bin/env python
# -*- coding: utf-8 -*-



from os.path import join, exists

from .handler import Handler



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
