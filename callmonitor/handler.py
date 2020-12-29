#!/usr/bin/env python
# -*- coding: utf-8 -*-



from os.path import join

import numpy as np



class Handler(object):


    def __init__(self, data, target):
        self._data   = data
        self._target = target


    @property
    def data(self):
        return self._data


    @data.setter
    def data(self, val):
        self._data = val


    @property
    def target(self):
        return self._target


    @target.setter
    def target(self, val):
        self._target = vale



class DefaultHandler(Handler):

    def load(self, path):
        pass


    def save(self, path):
        pass


    @classmethod
    def accumulator_done(cls):
        pass



class NPHandler(Handler):

    def load(self, path):
        self.data = np.load(join(path, f"arg_{self.target}.npy"))


    def save(self, path):
        np.save(join(path, f"arg_{self.target}.npy"), self.data)


    @classmethod
    def accumulator_done(cls):
        pass

