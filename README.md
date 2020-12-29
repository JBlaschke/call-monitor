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


### We don't Overwrite Output

If the `call-monitor` folder already exists (eg. a previous run), then a new
folder `call-monitor-1`, or `call-monitor-2`, and so on, is created.


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

The `Loader` class helps load the input arguments:
```python
l = callmonitor.Loader("<function name>", invocation_count)
args, kwargs = l.load()
```
loads the `invocation_count`-th call to `<function_name>`.

If the call data has been saved using `v0.2.0` or greater, then the
`inspect.FullArgSpec` will also be saved. This can be accessed using
`l.argspec`. Otherwise `l.argspec` will throw an `ArgspecUnkown` error.



## Backward Compatibility

Version 0.3.0 brigns many enhancements to `callmonitor`. We therefore could no
longer enable native backward compatibility. We are working on a tool that can
convert an `callmonitor v0.2.0` database to a version 0.3.0 (or later).
Versions pre-dating 0.2.0 are no longer supported.
