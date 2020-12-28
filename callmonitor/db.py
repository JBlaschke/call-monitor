#!/usr/bin/env python
# -*- coding: utf-8 -*-



from os      import makedirs, listdir
from os.path import join, exists, isdir
from pickle  import dump, load

from .version   import VERSION
from .singleton import Singleton
from .counter   import Counter



class IncompatibleVersion(Exception):
    pass



MIN_VERSION = (0, 3, 0)



def compatible(i, j, k):
    if i > MIN_VERSION[0] &&
       j > MIN_VERSION[1] &&
       k > MIN_VERSION[2]:
        return True

    return False



def load(root):

    with open(join(root, "db.pkl"), "rb") as f:
        db = load(f)

    if not compatible(* db.version):
        raise IncompatibleVersion

    # just to be safe
    db.lock()

    return db



def save(db):
    with open(join(db.root, "db.pkl"), "wb") as f:
        dump(db, f)



def new(db):

    if exists(db.root):
        n = 1
        while True:
            if exists(f"{db.root}-{n}"):
                n += 1
            else:
                break
        db.root = f"{db.root}-{n}"

    makedirs(db.root)




class DBLocked(Exception):
    pass



class DestinationNotFree(Exception):
    pass



class DB(object):

    def __init__(self, root="call-monitor"):
        self.min_version = (0, 3, 0)
        self._version = VERSION
        self._root    = root
        self._locked  = False
        self._counter = Counter()
        self._calls   = dict()


    def log(self, name, input_descriptor):
        if self.locked:
            raise DBLocked

        self.counter.increment(name)

        dest = join(self.root, name, self.counter[name])

        if exists(dest):
            raise DestinationNotFree

        makedirs(dest)

        with open(join(dest, "input_descriptor.pkl"), "wb") as f:
            dump(input_descriptor, f)

        for elt in input_descriptor["args"]:
            elt.save(dest)

        for elt in input_descriptor["kwargs"]:
            input_descriptor["kwargs"].save(dest)

        if name not in self.calls:
            self.calls[name] = list()

        self.calls[name].append(
            {
                "argspec": input_descriptor["argspec"],
                "dest": dest
            }
        )

    
    def lock(self):
        self._locked = True
        self._counter.lock()


    @property
    def version(self):
        return self._version


    @property
    def root(self):
        return self._root


    @root.setter
    def root(self, val):
        self._root = val


    @property
    def locked(self):
        return self._locked


    @property
    def counter(self):
        return self._counter


    @property
    def calls(self):
        return self._calls


    @property
    def dirs(self):
        # freeze state -- allows the stable use of yield below
        directory_contents = listdir(self.root)

        for element in directory_contents:
            if isdir(element):
                yield element
