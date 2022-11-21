#[s] definitions of executions
MPI=" "
VMC="./vmc.out"
VMCDRY="./vmcdry.out"
#[e] definitions of executions

echo "InOrbital  zqp_APOrbital_opt.dat" >> namelist.def 
#[s] opt
  ${VMCDRY} ./StdFace.def
  ${MPI} ${VMC} namelist.def 
  cp ./output/zqp_opt.dat . 
  mv output opt
#[e] opt

#[s] aft
  ${VMCDRY} ./StdFace_aft.def
  cp green1.def greenone.def 
  cp green2.def greentwo.def
  ${MPI} ${VMC} namelist.def ./zqp_opt.dat
  mv output aft
#[e] aft

#[s] post process
  #python3 VMClocal.py  input.toml
  #python3 VMCcor.py    input.toml
#[e] post process
