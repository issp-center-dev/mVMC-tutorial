#[s] definitions of executions
MPI=" "
VMC="vmc.out"
VMCDRY="vmcdry.out"
UHF="/usr/share/mvmc/tool/UHF"
#[e] definitions of executions

python3 MakeInput.py input.toml

${VMCDRY} stan_opt.in

#[s]UHF
mkdir tmpUHF
python3 MakeIni.py input.toml
echo "        Initial initial.def" >> namelist.def 
${UHF} namelist.def
#[e]UHF
