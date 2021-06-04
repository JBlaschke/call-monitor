#!/usr/bin/env python
# -*- coding: utf-8 -*-



from .singleton import Singleton



class Settings(object, metaclass=Singleton):

    def __init__(self):
        self._multi_threading = False
        self._pid             = None
        self._tident          = None


    @property
    def multi_threading_enabled(self):
        return self._multi_threading


    def enable_multi_threading(self, pid, tident=None):
        self._multi_threading = True
        self._pid = pid
        self._tident = tident


    def disbale_multi_threading(self):
        self._multi_threading = False


    @property
    def pid(self):
        return self._pid


    @property
    def tident(self):
        return self._tident


    @property
    def tid_tag(self):
        if self.multi_threading_enabled:
            if self._tident is None:
                return f"-pid={self.pid}"
            return f"-pid={self.pid}-tident={self.tident}"
        else:
            return ""
