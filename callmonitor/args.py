#!/usr/bin/env python
# -*- coding: utf-8 -*-



from .registry import Registry



class ArgsHandler(object):

    def __init__(self, name, argspec):
        self._name    = name
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
            handler = registry[t](a, i)
            pickle_mask.append(handler)


        pickle_kwmask = dict()
        for kw in kwtypes:
            handler = registry[kwtypes[kw]](kwargs[kw], kw)
            pickle_kwmask[kw] = handler

        registry.accumulator_done()

        return {
            "args": pickle_mask,
            "kwargs": pickle_kwmask,
            "argspec": self.argspec
        }

