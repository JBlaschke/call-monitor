#!/usr/bin/env python
# -*- coding: utf-8 -*-


from time import sleep

from callmonitor.libevent import event_here, start, stop, log, event_log


@log
def test_inplace_logger(n):

    start(f"sleep({n})")
    sleep(n)  # sleep for n seconds
    stop("sleep")



if __name__ == "__main__":

    event_here("start", "    ")
    test_inplace_logger(1)
    event_here("inplace_test", "done")

    print("Testing inplace event logger:")
    for entry in event_log():
        print(f"{entry}")