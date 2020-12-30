# `callmonitor` -- A Simple Tool to Monitor and Log Function Calls


## Installation

```bash
pip install callmonitor
```
or clone this repo and:
```bash
python setup.py install
```


## Usage

It's simple to use, just decorate any function with the `@intercept` decorator.
Eg:
```python
from callmonitor import intercept

@intercept
def test_fn_2(x, y=2, z=3):
    pass
```
This will save the inputs (`args`, `kwargs` and `argspec`) along with a call
database (`callmonitor.DB`) to: `call-monitor/test_fn_2/<invocation count>`.


### `callmonitor` Doesn't Overwrite Output

If the `call-monitor` folder already exists (eg. a previous run), then a new
folder `call-monitor-1`, or `call-monitor-2`, and so on, is created. See the
sections on `Data Structure` for more details on _how_ this data is saved.


### Multi-Threading/Process Safe

To avoid different processes from writing to the same location, `callmonitor`
appends `-tid=<N>` to the root (`call-monitor`) folder. Currently `callmonitor`
supports `mpi4py` out of the box: if `mpi4py.MPI.COMM_WORLD.Get_rank() > 1`,
`callmonitor` automatically assumes that it's running im multi-threaded mode
and appends `-tid=<Get_rank()>` to the output. If your programm is
multi-threaded with another framwork (eg. `concurrent.Futures`) then you need
to tell `callmonitor` your thread ID using `callmonitor.Settings`:
```python
from callmonitor import Settings

settings = Settings()
settings.enable_multi_threading(THREAD_ID)
```
__before__ the first invocation of `intercept` (the database is created on disk
when it is first needed, it is at that point when `callmonitor.Settings` is
read. Any changes made to `callmonitor.Settings` afterwards will only take
effect if the database is recreated -- using `callmonitor.CONTEXT.new`).


### Registering your own Argument `Handler`s

Sometimes `pickle` just won't cut it in terms of saving function inputs -- eg.
when we need to save our own fancy data types. `callmonitor` provides a way of
building your down argument handlers and registering to the global
`callmonitor.REGISTRY`. The registry is queried every time function inputs are
processed, so if you build your own `ArgHandler` and add them usingg
`callmonitor.REGISTRY.add`, it will process any arguments of the associated
datatype from that point forward. Eg, `numpy` provides its own `save`/`load`
functions. We have already build (and registered) a numpy arggument handler
like so:
```python
import numpy as np

from os.path     import join
from callmonitor import Handler, REGISTRY

class NPHandler(Handler):

    def load(self, path):
        self.data = np.load(join(path, f"arg_{self.target}.npy"))


    def save(self, path):
        np.save(join(path, f"arg_{self.target}.npy"), self.data)


    @classmethod
    def accumulator_done(cls):
        pass

REGISTRY.add(np.ndarray, NPHandler)
```
(remember that `callmonitor.REGISTRY.add` needs to be called __before__ the
first invocation of `@intercept` that needs this particular `Handler`). A
custom handler needs to inherit the `callmonitor.Handler` class and define
`save`, `load`, and `accumulator_done` (the last one being a `@classmethod`).


### Loading Data

`callmonitor.load(<path>)` will load a database at `<path>` (see section on
`Data Structure`). Eg:
```python
from callmonitor import load

db = load("call-monitor")
```

We can now get individual function calls data from the database using `DB.get`:
```python
args, kwargs = db.get("function_name", invocation_count)
```
(which will also automatically load `.npy` files and any custom handlers --
remember to register these in `callmonitor.REGISTRY` before executing `db.get`)

__Remember:__ `invocation_count` starts at 1. Therefore to access the _first_ call to `test_np_1`, run:
```python
In [4]: db.get("test_np_1", 1)
Out[4]: ([10, array([0., 0., 0., 0., 0., 0., 0., 0., 0., 0.])], {})
```


## Interacting with `callmonitor`

We try to enable top-level summaries of the following user-facing classes:
1. `REGISTRY`
2. `DB`
3. `DB.get_args`, and `Args`
via the `__str__` and `__repr__` functions. Eg, `callmonitor.REGISTRY` shows
which datatype/handler pairs are configured:
```python
In [2]: callmonitor.REGISTRY
Out[2]:
{
    <class 'numpy.ndarray'>: <class 'callmonitor.handler.NPHandler'>
}
```
Likewise the `DB` object displays a summary of functions called and how often.
```python
In [3]: db = callmonitor.load("call-monitor")
In [4]: db
Out[4]:
{
    Locked: True
    test_np_1: {
        calls: 2
        args: ['x', 'n']
        defaults: None
    }
}
```


### `Args` Container

Picking apart `args`, `kwargs`, and `argspec.defaults` can be very tedious --
especially if you're trying to find out the value of a specific argument. Hence
`callmonitor.DB` provides an additionl getter -- `get_args` which returns an
`Args` object. `callmonitor.Args` are container classes that store each input
argument by name as an attributed. Eg:
```python
In [3]: args = db.get_args("test_fn_1", 1)
In [4]: args
Out[4]: dict_keys(['x', 'y', 'z'])
In [5]: args.x
Out[5]: 1
```

Note: the `callmonitor.Args` constructor will fill in any arguments not in
`args` and `kwargs` from the `FullArgSpec` defaults. If you just want to
recreate the original function call the `args` and `kwargs` returned by
`callmonitor.DB.get` should be enough.


## Data Structure

While not technically a _database_, let's call the directories generated by
`callmonitor` a database for the lack of a better term. Each database consists
of a `db.pkl` file (containing metadata), as well as folders for each function
(each function call is enumerated). Eg:
```
call-monitor
├── db.pkl
├── test_fn_1
│   ├── 1
│   │   └── input_descriptor.pkl
│   └── 2
│       └── input_descriptor.pkl
└── test_fn_2
    └── 1
        └── input_descriptor.pkl
```
Special attention is given to `numpy` inputs -- these are called
`arg_<label>.npy`, where `<label>` is either the index of the input argument,
or the `kw` for kwargs. Eg:
```
call-monitor
├── db.pkl
└── test_np_1
    ├── 1
    │   ├── arg_1.npy
    │   └── input_descriptor.pkl
    └── 2
        ├── arg_n.npy
        └── input_descriptor.pkl
```

Full consideration was given to saving _all_ call data in a single data
structure -- maybe even a _real_ database ;) -- but to do this efficiently at
scale is not easy, and might make this package cumbersome. Future versions will
include the ability to fuse multiple small function calls into a single
accumulator object to avoid large numbers of small files.


## Backward Compatibility

Version 0.3.0 brigns many enhancements to `callmonitor`. We therefore could no
longer enable native backward compatibility. A tool that can convert an version
0.2.0 database to a version 0.3.0 (or later) is currently being developed.
Versions pre-dating 0.2.0 are no longer supported.
