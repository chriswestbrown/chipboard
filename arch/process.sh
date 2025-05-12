#!/bin/bash

#PBS -l select=16:ncpus=20:mpiprocs=20
#PBS -l place=scatter:excl
#PBS -A MHPCC96650N19
#PBS -q debug
#PBS -l walltime=0:00:30
#PBS -N ProcessTesting
#PBS -j oe

cd ${HOME}
module purge
module load anaconda3/5.2.0
source activate mpi4py
mpirun -n 2 python process.py > out.txt 2> err.txt
