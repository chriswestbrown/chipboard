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

from keras.layers import Dense
import keras
import numpy
import random
from learn import Learner
from mpi4py import MPI
from subprocess import Popen,PIPE
import math


comm = MPI.COMM_WORLD
rank,size = (comm.Get_rank(), comm.Get_size())


if rank == 0:
    l = Learner(0,4)
    n_workers = size - 1
    N = l.num_boards # number of tests to be run


    #### MANAGER ####
    # random.seed(a=2020) # note: same seed every time! Don't really do this!

    # Give every worker its own random seed
    for p in range(1,n_workers+1):
        ready = comm.recv(source=p)
        comm.send(random.randint(0,10000),dest=ready)



    for i in range(math.ceil(l.total_boards/N)):
        x = []
        y = []
        weights = l.getWeightArray()
        weight_string = str(weights[0][0])+" "+str(weights[1][0])+" "+str(weights[2][0])+" "+str(weights[3][0])+"\n"

        # Farm out tasks to works until completed
        test_num = 0 # last completed test, tests are numbered 1 through N
        active = 0 # the number of processes currently
        fail = 0

        #prompt worker nodes to communicate if not in first round
        if i!=1:
            for p in range(1,n_workers+1):
                comm.send("wakeup",p)

        while test_num < N or active > 0:
            ready,res = comm.recv()
            if res != "init":
                active = active -1
                try:
                    for line in res.strip().split("\n"):
                        x.append([int(i) for i in line.split(":")[0].split(",")])
                        y.append(float(line.split(":")[1]))
                except:
                    fail += 1
                    print("Fail num: "+str(fail)+"\ncould not parse this result:\n\t"+res)
            if test_num < N:
                test_num = test_num + 1
                comm.send(weight_string,dest=ready) # give worker more work
                active = active + 1
            else:
                active = active-1

        l.model.fit(numpy.array(x),numpy.array(y),epochs=l.epochs,verbose=0)
        l.testKnowledge(100,0)
        l.learning_rate *= l.learning_decay
        l.opt = keras.optimizers.SGD(lr=l.learning_rate,clipvalue=0.5)
        l.model.compile(l.opt,loss='mean_squared_error',metrics=['accuracy'])

    #kill all workers
    for p in range(1,n_workers+1):
        comm.send("die",p)
    exit()

else:
    #### WORKER ####
    comm.send(rank,dest=0)
    seed = comm.recv(source=0)
    if seed < 0:
        sys.exit(0)
    random.seed(a=seed)
    comm.send((rank,"init"),dest=0)
    while True:
        k = comm.recv(source=0) # receive work tasking from manager
        if k == "die":
            break;
        elif k == "wakeup":
            comm.send((rank,"init"),0)
        p = Popen(["./mpichipboard"],stdout=PIPE,stdin=PIPE)
        res = p.communicate(k.encode())[0]
        p.terminate()
        comm.send((rank,res.decode()),dest=0) # send manager result
