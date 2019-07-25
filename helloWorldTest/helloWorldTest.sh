#!/bin/bash

#PBS -l select=1:ncpus=30:mpiprocs=30
#PBS -l place=scatter:excl
#PBS -A MHPCC96650N19
#PBS -q background
#PBS -l walltime=0:03:00
#PBS -j oe
#PBS -N HelloWorldTest

export PYTHONWARNINGS="ignore"
cd $WORKDIR/HPC
module purge
module load pbs tensorflow/1.8.0 spectrum-mpi cuda/9.2
export PYTHONPATH="$WORKDIR"
mpiexec -n 30 python mpiHelloWorld.py
