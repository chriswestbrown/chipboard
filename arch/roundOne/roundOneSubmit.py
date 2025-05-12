#!/usr/bin/env python
#4Feature

import sys
import re
from learn import Learner
from mpi4py import MPI
import time

start_time = time.time()
rank = MPI.COMM_WORLD.Get_rank()
size = MPI.COMM_WORLD.Get_size()
name = MPI.Get_processor_name()
nodeNum = int(sys.argv[2])-1
seed = 80*nodeNum+rank
if seed>624: 
 sys.exit(0)

f =   sys.argv[1] + "_r_" + str(nodeNum)+ "_" + str(rank)+ ".txt"
wf =  sys.argv[1] + "_w_" + str(nodeNum) + "_"+ str(rank) + ".txt"
t = sys.argv[1] + "_t_" + str(nodeNum) + "_" + str(rank) + ".txt"
l = Learner(seed, 4)
learnThingsCPP(kind=0, file=f, weightFile=wf)
a = open(t, 'w')
a.write(str(time.time() - start_time))
a.close()
sys.exit(0)
