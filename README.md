# `callmonitor` -- A Simple Tool to Monitor Function Calls

It's simple to use, just decorate any function with the `@intercept` decorator.
This will save the input arguments to the
`call-monitor/<function_name>/<invocation count>` folder.

The `Loader` class helps load the input arguments:
```python
l = callmonitor.Loader("<function name>", invocation_count)
args, kwargs = l.load()
```
loads the `invocation_count`-th call to `<function_name>`.

If the call data has been saved using `v0.2.0` or greater, then the
`inspect.FullArgSpec` will also be saved. This can be accessed using
`l.argspec`. Otherwise `l.argspec` will throw an `ArgspecUnkown` error.
