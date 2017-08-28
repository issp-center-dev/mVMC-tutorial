#!/bin/sh
#QSUB -queue i9acc
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
#[s]opt1
echo -n "[s]opt1"
date
 mpijob vmc.out namelist.def 
echo -n "[e]opt1"
date
cp ./output/zqp_opt.dat . 
mv output opt1
#[e]opt1

#[s]opt2
vmcdry.out ./StdFace_2.def
echo -n "[s]opt2"
date
 mpijob vmc.out namelist.def ./zqp_opt.dat
echo -n "[e]opt2"
date
cp ./output/zqp_opt.dat . 
mv output opt2
#[e]opt2

#[s]aft
vmcdry.out ./StdFace_aft.def
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
