#!/usr/bin/env python
#4Feature

import sys
from learn import Learner
from mpi4py import MPI
import time


start_time = time.time()
rank = MPI.COMM_WORLD.Get_rank()

if rank>624: 
 sys.exit(0)
f =  "r" + sys.argv[1] + str(rank) + ".txt"
wf =  "w" + sys.argv[1] + str(rank) + ".txt"

l = Learner(rank, 4);
l.totalBoards=10;
l.num_boards=10;
l.learnThingsCPP(kind=0, file=f, weightFile=wf)
print("--- %s seconds ---" % (time.time() - start_time))
sys.exit(0)
