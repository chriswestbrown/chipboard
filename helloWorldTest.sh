#!/bin/bash

#PBS -l select=1:ncpus=5:mpiprocs=5
#PBS -l place=scatter:excl
#PBS -A MHPCC96650N19
#PBS -q debug
#PBS -l walltime=0:01:00
#PBS -j oe
#PBS -o $WORKDIR/output.txt
#PBS -e $WORKDIR/error.txt
#PBS -N helloWorldTest


export PYTHONWARNINGS="ignore"
cd $WORKDIR
module purge
module load pbs tensorflow/1.8.0 spectrum-mpi cuda/9.2
mpirun ./mpiHelloWorld.py
