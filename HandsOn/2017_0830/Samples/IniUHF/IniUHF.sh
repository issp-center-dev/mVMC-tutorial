#[s]UHF
mkdir tmpUHF
cp IniGreen.pl ./tmpUHF
cp *def        ./tmpUHF
cp input.txt   ./tmpUHF
cp ./UHF       ./tmpUHF
cd ./tmpUHF
  perl -w IniGreen.pl
  echo "        Initial zinitial.def" >> namelist.def 
  ./UHF namelist.def
cd -
#[e]UHF
cp tmpUHF/zqp_APOrbital_opt.dat . 
echo "         InOrbital  zqp_APOrbital_opt.dat" >> namelist.def 
