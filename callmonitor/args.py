#!/usr/bin/env python
# -*- coding: utf-8 -*-



from os      import makedirs
from os.path import join, exists
from pickle  import dump

# from .counter  import Counter
from .registry import Registry



class ArgsHandler(object):

    def __init__(self, name, argspec):
        # c = Counter()
        # c.increment(name)

        self._name = name
        # self.dest = join("call-monitor", name, str(c.count(name)))
        # if not exists(self.dest):
        #     makedirs(self.dest)

        self._argspec = argspec


    @property
    def name(self):
        return self._name


    @property
    def argspec(self):
        return self._argspec


    @staticmethod
    def types(args, kwargs):
        args_types   = [type(a) for a in args]
        kwargs_types = {kw: type(kwargs[kw]) for kw in kwargs}
        return args_types, kwargs_types


    def save(self, args, kwargs):
        registry       = Registry()
        types, kwtypes = self.types(args, kwargs)

        pickle_mask = list()
        for i, (a, t) in enumerate(zip(args, types)):
            # if self.filter(t):
            #     pickle_mask.append(a)
            # else:
            #     h = NPHandler(self.dest, i)
            #     pickle_mask.append(h)
            #     h.save(a)
            handler = registry[t](a, i)
            pickle_mask.append(handler)


        pickle_kwmask = dict()
        for kw in kwtypes:
            # if self.filter(kwtypes[kw]):
            #     pickle_kwmask[kw] = kwargs[kw]
            # else:
            #     h = NPHandler(self.dest, kw)
            #     pickle_kwmask[kw] = h
            #     h.save(kwargs[kw])
            handler = registry[kwtypes[kw]](kwargs[kw], kw)
            pickle_kwmask[kw] = handler

        registry.accumulator_done()

        # with open(join(self.dest, "args.pkl"), "wb") as f:
        #     dump(pickle_mask, f)

        # with open(join(self.dest, "kwargs.pkl"), "wb") as f:
        #     dump(pickle_kwmask, f)

        # with open(join(self.dest, "argspec.pkl"), "wb") as f:
        #     dump(self.argspec, f)

        return {
            "args": pickle_mask,
            "kwargs": pickle_kwmask,
            "argspec": self.argspec
        }

