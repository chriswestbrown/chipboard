#!/bin/bash

#PBS -l select=32:ncpus=20:mpiprocs=20
#PBS -l place=scatter:excl
#PBS -A MHPCC96650N19
#PBS -q debug
#PBS -l walltime=0:25:00
#PBS -o ${WORKDIR}/roundOneO.txt
#PBS -e ${WORKDIR}/roundTwoE.txt
#PBS -N RoundOneTesting

cd ${WORKDIR}
module purge
module load anaconda3/5.2.0
source activate mpi4py
module load gcc/5.3.0 cuda/9.2 openmpi/2.1.1/gnu/5.3.0
echo $(date) > roundOneTime.dt
mpirun python roundOneSubmit.py 4FeatureR1
echo $(date) >> roundOneTime.dt
