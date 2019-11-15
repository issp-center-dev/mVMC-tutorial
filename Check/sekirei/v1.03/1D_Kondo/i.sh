#!/bin/sh
#QSUB -queue i18cpu
#QSUB -node  8
#QSUB -mpi   24
#QSUB -omp   8
#QSUB -place pack
#QSUB -over false
#PBS -l walltime=00:30:00
#PBS -N mVMC
cd ${PBS_O_WORKDIR}
 #. /etc/profile.d/modules.sh
#module list > a
#module list
source /home/issp/materiapps/mVMC/mVMCvars.sh
#[s]aft
#vmcdry.out ./StdFace_aft.def
perl -w CisAjs.pl 
perl -w CisAjsCktAltDC.pl
echo -n "[s]aft"
date
 mpijob vmc.out namelist.def ./zqp_opt.dat
echo -n "[e]aft"
date
mv output aft
#[e]aft

#[s]pl_aft
echo -n "[s]pl_aft"
date
perl -w Aft_Sq_Hub.pl 
echo -n "[e]pl_aft"
date
#[e]aft
