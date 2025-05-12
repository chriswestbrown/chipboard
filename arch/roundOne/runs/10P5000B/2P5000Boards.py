#!/usr/bin/env python
#4Feature

import sys
import re
from mpi4py import MPI
import time
import os

start_time = time.time()
rank = MPI.COMM_WORLD.Get_rank()
size = MPI.COMM_WORLD.Get_size()
name = MPI.Get_processor_name()
nodeNum = int(sys.argv[2])-1
seed = 10*nodeNum+rank
if seed>624: 
 sys.exit(0)

f =   sys.argv[1] + "_r_" + str(nodeNum)+ "_" + str(rank)+ ".txt"
wf =  sys.argv[1] + "_w_" + str(nodeNum) + "_"+ str(rank) + ".txt"
t = sys.argv[1] + "_t_" + str(nodeNum) + "_" + str(rank) + ".txt"

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"   # see issue #152
if rank in range(4):
 os.environ["CUDA_VISIBLE_DEVICES"] = str(rank)
else:
 os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

from learn import Learner
l = Learner(seed, 4)
l.total_boards=5000
l.learnThingsCPP(kind=0, file=f, weightFile=wf)
a = open(t, 'w')
a.write(str(time.time() - start_time))
a.close()
sys.exit(0)
