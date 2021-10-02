from time import sleep

from callmonitor.libevent import log


@log
def dependent_function(n):
    sleep(n)


