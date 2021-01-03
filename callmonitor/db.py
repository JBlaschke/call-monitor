#!/usr/bin/env python
# -*- coding: utf-8 -*-



from os      import makedirs, listdir
from os.path import join, exists, isdir
from pickle  import dump, load as pload

from .version import VERSION
from .counter import Counter
from .args    import Args



class IncompatibleVersion(Exception):
    pass



MIN_VERSION = (0, 3, 0)



def compatible(i, j, k):
    if i < MIN_VERSION[0]:
        return False
    elif i == MIN_VERSION[0] and j < MIN_VERSION[1]:
        return False
    elif i == MIN_VERSION[0] and j == MIN_VERSION[2] and k < MIN_VERSION[2]:
        return False

    return True



def load(root):

    with open(join(root, "db.pkl"), "rb") as f:
        db = pload(f)

    if not compatible(* db.version):
        raise IncompatibleVersion

    # just to be safe
    db.root = root
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



class CallNotLogged(Exception):
    pass



class CannotFindRecord(Exception):
    pass



class DB(object):

    def __init__(self, root=f"call-monitor"):
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

        loc  = join(name, str(self.counter[name]))
        dest = join(self.root, loc)

        if exists(dest):
            raise DestinationNotFree

        makedirs(dest)

        for elt in input_descriptor["args"]:
            elt.save(dest)

        for k, elt in input_descriptor["kwargs"].items():
            elt.save(dest)

        # This needs to happen _after_ each element's .save as the .save
        # method can offload some data to disk (eg. numpy arrays)
        with open(join(dest, "input_descriptor.pkl"), "wb") as f:
            dump(input_descriptor, f)

        if name not in self.calls:
            self.calls[name] = list()

        self.calls[name].append(
            {
                "argspec": input_descriptor["argspec"],
                "loc": loc
            }
        )


    def get(self, name, call_seq): 
        if self.counter[name] < call_seq:
            raise CallNotLogged

        dest = join(self.root, self.calls[name][call_seq - 1]["loc"])

        if not exists(dest):
            raise CannotFindRecord

        with open(join(dest, "input_descriptor.pkl"), "rb") as f:
            input_descriptor = pload(f)
        
        args = [None]*len(input_descriptor["args"])
        for i, elt in enumerate(input_descriptor["args"]):
            elt.load(dest)
            args[i] = elt.data

        kwargs = dict()
        for k, elt in input_descriptor["kwargs"].items():
            elt.load(dest)
            kwargs[k] = elt.data

        return args, kwargs

    
    def get_args(self, name, call_seq):
        args, kwargs = self.get(name, call_seq)
        argspec      = self.calls[name][call_seq - 1]["argspec"]
        return Args(argspec, args, kwargs)


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


    def __str__(self):
        str_out  = "{\n"
        str_out += f"    Locked: {self.locked}\n"

        for key, call in self.calls.items():
            str_out += f"    {key}: "+"{\n"
            str_out += f"        calls: {self.counter[key]}\n"
            str_out += f"        args: {call[0]['argspec'].args}\n"
            str_out += f"        defaults: {call[0]['argspec'].defaults}\n"
            str_out +=  "    }\n"

        str_out += "}"
        return str_out


    def __repr__(self):
        return str(self)
