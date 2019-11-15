#!/bin/sh
#QSUB -queue i18cpu
#QSUB -node  1
#QSUB -mpi   1
#QSUB -omp   24
#QSUB -place pack
#QSUB -over false
#PBS -l walltime=00:30:00
#PBS -N mVMC
cd ${PBS_O_WORKDIR}
 #. /etc/profile.d/modules.sh
#module list > a
#module list

source /home/issp/materiapps/mVMC/mVMCvars.sh
VMC="vmc.out "
VMCDRY="vmcdry.out "

perl -w MakeMod.pl
#[s]opt1
$VMCDRY ./StdFace.def
echo -n "[s]opt1"
date
 mpijob $VMC namelist.def 
echo -n "[e]opt1"
date
cp ./output/zqp_opt.dat . 
mv output opt1
#[e]opt1

#[s]opt2
$VMCDRY ./StdFace_2.def
echo -n "[s]opt2"
date
 mpijob $VMC namelist.def ./zqp_opt.dat
echo -n "[e]opt2"
date
cp ./output/zqp_opt.dat . 
mv output opt2
#[e]opt2

#[s]aft
$VMCDRY ./StdFace_aft.def
perl -w CisAjs.pl 
perl -w CisAjsCktAltDC.pl
echo -n "[s]aft"
date
 mpijob $VMC namelist.def ./zqp_opt.dat
echo -n "[e]aft"
date
mv output aft
#[e]aft

#[s]pl_aft
echo -n "[s]pl_aft"
date
perl -w Aft_energy.pl 
perl -w Aft_Sq.pl 
perl -w Aft_SiSj.pl 
echo -n "[e]pl_aft"
date
#[e]aft
