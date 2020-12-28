#!/usr/bin/env python
# -*- coding: utf-8 -*-


from .singleton import Singleton
from .handler   import DefaultHandler



class MethodNotRegistered(Exception):
    pass



class Registry(object, metaclass=Singleton):

    def __init__(self):
        self._registry = dict()


    def add(self, target, method):
        self._registry[target] = method


    def accumulator_done(self):
        for elt in self:
            elt.accumulator_done()


    def __getitem__(self, target):
        if target in self:
            return self._registry[target]
        else:
            return DefaultHandler


    def __iter__(self):
        for key in self._registry:
            yield key


    def __str__(self):
        str_out = "["

        for key in self:
            str_out += f"{key}:{self[key]}, "

        str_out = str_out[:-2]
        str_out += "]"
        return str_out


    def __repr__(self):
        return str(self)
