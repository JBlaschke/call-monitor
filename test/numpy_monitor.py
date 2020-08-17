#!/usr/bin/env python
# -*- coding: utf-8 -*-



import numpy as np

from callmonitor import intercept


@intercept
def test_np_1(x, n):
    pass



if __name__ == "__main__":

    M    = 10
    ar_1 = np.zeros(M)
    ar_2 = np.ones_like(ar_1)

    test_np_1(M, ar_1)
    test_np_1(M, n=ar_2)
