#!/usr/bin/env python
# -*- coding: utf-8 -*-



from os.path import join
from pickle  import load

import numpy as np



# class HasNoRoot(Exception):
#     """Has No Root"""
#     pass



class Handler(object):


    def __init__(self, data, target):
        self._data     = data
        self._target   = target


    # def __init__(self, dest, target):
    #     self._dest     = dest
    #     self._target   = target
    #     self._has_root = False


    # @property
    # def has_root(self):
    #     return self._has_root


    # @property
    # def root(self):
    #     if self.has_root:
    #         return self._root
    #     else:
    #         raise HasNoRoot


    # @root.setter
    # def root(self, val):
    #     self._root = val
    #     self._has_root = True


    # @property
    # def dest(self):
    #     # if self.has_root:
    #     #     return join(self.root, self._dest)
    #     # else:
    #     #     return self._dest
    #     return self._dest


    # @dest.setter
    # def dest(self, val):
    #     self._dest = val


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

