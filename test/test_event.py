#!/usr/bin/env python
# -*- coding: utf-8 -*-


from time import sleep

from callmonitor.libevent import event_here, start, stop, log, event_log

from deps_event import dependent_function


@log
def inner_function(n):
    dependent_function(n)
    sleep(n)


@log
def outer_function(n1, n2):
    @log
    def inplace_function():
        pass
    sleep(n1)
    inner_function(n2)
    inplace_function()


@log
def test_inplace_logger(n):

    start(f"sleep({n})")
    sleep(n)  # sleep for n seconds
    stop("sleep")
    outer_function(n, 2*n)
    inner_function(n)


if __name__ == "__main__":

    event_here("start", "    ")
    test_inplace_logger(1)
    event_here("inplace_test", "done")

    print("Testing inplace event logger:")
    for entry in event_log():
        print(f"{entry}")
