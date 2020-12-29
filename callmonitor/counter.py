#!/usr/bin/env python
# -*- coding: utf-8 -*-



class CounterLocked(Exception):
    pass



class Counter(object):

    def __init__(self):
        self._locked = False
        self.reset()


    def lock(self):
        self._locked = True


    @property
    def locked(self):
        return self._locked


    def reset(self):
        if self.locked:
            raise CounterLocked

        self._count = {}


    def reset_key(self, key):
        if self.locked:
            raise CounterLocked

        self._count[key] = 0


    def __iter__(self):
        for key in self._count:
            if self._count[key] > 0:
                yield key


    def __getitem__(self, key):
        if not key in self:
            return 0

        return self._count[key]


    def increment(self, key):
        if self.locked:
            raise CounterLocked

        if not key in self._count.keys():
            self.reset_key(key)

        self._count[key] += 1


    def __str__(self):
        str_out = "{\n"

        for key in self:
            str_out += f"    {key}: {self[key]}\n"

        str_out += "}"
        return str_out


    def __repr__(self):
        return str(self)
