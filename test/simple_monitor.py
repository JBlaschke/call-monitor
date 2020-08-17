#!/usr/bin/env python
# -*- coding: utf-8 -*-

from callmonitor import intercept


@intercept
def test_fn_1(x, y, z=3):
    pass



if __name__ == "__main__":

    test_fn_1(1, "two")
