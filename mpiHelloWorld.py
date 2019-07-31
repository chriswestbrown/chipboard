
#!/usr/bin/env python
#Parallel HelloWorld

from mpi4py import MPI
import sys

size = MPI.COMM_WORLD.Get_size()
rank = MPI.COMM_WORLD.Get_rank()
name = MPI.Get_processor_name()
sys.stdout = open('file' + str(rank) + 'of' + str(size), 'w')
print(
    "Hello, World! I am process %d of %d on %s.\n"
    % (rank, size, name))
