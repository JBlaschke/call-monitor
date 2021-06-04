#!/usr/bin/env python
# -*- coding: utf-8 -*-



from mpi4py      import MPI
from callmonitor import intercept, rc


@intercept
def test_fn_1(x, y, z=3):
    pass



@intercept
def test_fn_2(x, y=2, z=3):
    pass



if __name__ == "__main__":

    rc(multi_threading=True, pid=MPI.COMM_WORLD.Get_rank())
    

    test_fn_1(1, "two")
    test_fn_1(2, y="three", z=[])
    test_fn_2(10)
