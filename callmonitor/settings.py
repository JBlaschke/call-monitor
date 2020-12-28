#!/usr/bin/env python
# -*- coding: utf-8 -*-



from .singleton import Singleton



class Settings(object, metaclass=Singleton):

    def __init__(self):
        self._mpi_rank = 0


    @property
    def mpi_rank(self):
        return self._mpi_rank


    @mpi_rank.setter
    def mpi_rank(self, val):
        self._mpi_rank = val
