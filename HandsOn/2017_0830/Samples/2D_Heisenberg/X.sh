perl -w MakeMod.pl
#[s]opt1
./vmcdry.out ./StdFace.def
echo -n "[s]opt1"
date
 mpirun ./vmc.out namelist.def 
echo -n "[e]opt1"
date
cp ./output/zqp_opt.dat . 
mv output opt1
#[e]opt1

#[s]opt2
./vmcdry.out ./StdFace_2.def
echo -n "[s]opt2"
date
 mpirun ./vmc.out namelist.def ./zqp_opt.dat
echo -n "[e]opt2"
date
cp ./output/zqp_opt.dat . 
mv output opt2
#[e]opt2

#[s]aft
./vmcdry.out ./StdFace_aft.def
perl -w CisAjs.pl 
perl -w CisAjsCktAltDC.pl
echo -n "[s]aft"
date
 mpirun ./vmc.out namelist.def ./zqp_opt.dat
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
