#!/usr/bin/env python
# -*- coding: utf-8 -*-



from .singleton import Singleton



class Settings(object, metaclass=Singleton):

    def __init__(self):
        self._multi_threading = False
        self._tid             = 0


    @property
    def multi_threading_enabled(self):
        return self._multi_threading


    def enable_multi_threading(self, tid):
        self._multi_threading = True
        self._tid = tid


    def disbale_multi_threading(self):
        self._multi_threading = False


    @property
    def tid(self):
        return self._tid


    @property
    def tid_tag(self):
        if self.multi_threading_enabled:
            return f"-tid={self.tid}"
        else:
            return ""
