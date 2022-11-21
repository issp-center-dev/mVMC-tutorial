#[s] definitions of executions
MPI=" "
VMC="./vmc.out"
VMCDRY="./vmcdry.out"
UHF="./UHF"
#[e] definitions of executions

python3 MakeInput.py input.toml
./vmcdry.out StdFace.def
#[s]UHF
mkdir tmpUHF
cp MakeIni.py ./tmpUHF
cp *def        ./tmpUHF
cp input.toml  ./tmpUHF
cp ./UHF       ./tmpUHF
cd ./tmpUHF
  python3 MakeIni.py input.toml
  echo "        Initial initial.def" >> namelist.def 
  ./UHF namelist.def
cd -
#[e]UHF
cp tmpUHF/zqp_APOrbital_opt.dat . 
