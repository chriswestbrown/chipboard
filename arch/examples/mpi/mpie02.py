#!/usr/bin/env python3

######################################################################
# Example pattern for using mpi with a manager/worker approach.
#
# run for example as: mpirun -n 4 ./mpie02.py
#
# We will run N tests.  Each test produces a value (the 'width') and
# we would like to print out the average 'width'.
# process 0 manages the process, keeping the worker threads busy.
# 1. each worder thread is given a seed value
# 2. worker's repeatedly signal that they are ready for work (also
#    returning a value if they've computed one, and the mangager
#    sends them a new test to run, summing up the results as it goes.
######################################################################
import random
from mpi4py import MPI
comm = MPI.COMM_WORLD
rank,size = (comm.Get_rank(), comm.Get_size())
n_workers = size - 1
N = 10 # number of tests to be run

if rank == 0:
    #### MANAGER ####
    random.seed(a=2020) # note: same seed every time! Don't really do this!

    # Give every worker its own random seed
    for p in range(1,n_workers+1):
        ready = comm.recv(source=p)
        comm.send(random.randint(0,10000),dest=ready)

    # Farm out tasks to works until completed
    test_num = 0 # last completed test, tests are numbered 1 through N
    active = 0 # the number of processes currently 
    sum = 0
    while test_num < N or active > 0:
        ready,val = comm.recv()
        if val >= 0:
           sum = sum + val
           active = active - 1
        if test_num < 10:
            test_num = test_num + 1
            comm.send(test_num,dest=ready) # give worker more work
            active = active + 1
        else:
            comm.send(-1,dest=ready) # tell worker to die
    res = sum/float(N)
    print(f"Averge width is {res}")

else:
    #### WORKER ####
    comm.send(rank,dest=0)
    seed = comm.recv(source=0)
    if seed < 0:
        sys.exit(0)
    random.seed(a=seed)
    comm.send((rank,-1),dest=0)
    while True:
        k = comm.recv(source=0) # receive work tasking from manager
        if k < 0:
            break;            
        s = 1 - random.randint(0,2)
        mx = s
        mn = s
        for i in range(0,100000):
            s += 1 - random.randint(0,2)
            mn = s if s < mn else mn
            mx = s if s > mx else mx
        print("I am %d doing task %d and I saw mx=%d mn=%d (seed = %d)!" % (rank,k,mx,mn,seed))
        comm.send((rank,mx-mn),dest=0) # send manager result
