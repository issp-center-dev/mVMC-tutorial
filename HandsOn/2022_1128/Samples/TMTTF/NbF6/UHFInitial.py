import numpy as np
import math
import cmath
import sys
import toml

def main():
    #[s] tolm load
    input_file  = sys.argv[1] 
    input_dict  = toml.load(input_file)
    #[e] tolm load
    #[s]define constants
    shift_x       = int((int(input_dict["abinitio"]["kx"])-1)/2)
    shift_y       = int((int(input_dict["abinitio"]["ky"])-1)/2)
    shift_z       = int((int(input_dict["abinitio"]["kz"])-1)/2)
    Lx            = int(input_dict["lattice"]["Lx"])
    Ly            = int(input_dict["lattice"]["Ly"])
    Lz            = int(input_dict["lattice"]["Lz"])
    orb_num       = int(input_dict["lattice"]["orb_num"])
    ham_lambda    = float(input_dict["param"]["lambda"])
    ddf           = float(input_dict["param"]["ddf"])
    mod_chemi     = float(input_dict["param"]["mod_chemi"])
    in_file_trans = input_dict["file"]["in_file_trans"]
    in_file_int   = input_dict["file"]["in_file_int"]
    sub_x         = int(input_dict["mVMC"]["sub_x"])
    sub_y         = int(input_dict["mVMC"]["sub_y"])
    sub_z         = int(input_dict["mVMC"]["sub_z"])
    method        = input_dict["method"]["method"]
    UHF_co        = float(input_dict["UHF"]["UHF_co"])
    UHF_mag       = float(input_dict["UHF"]["UHF_co"])
    #[e]define constants
    All_N = Lx*Ly*Lz*orb_num
    print('shift_x = ',shift_x)
    print('shift_y = ',shift_y)
    print('shift_z = ',shift_z)
    print('Lx = ',Lx)
    print('Ly = ',Ly)
    print('Lz = ',Lz)
    print('orb_num = ',orb_num)
    print('lambda  = ',ham_lambda)
    print('ddf     = ',ddf)

    #[s] initialize
    list_org   = [Lx,Ly,Lz,orb_num]
    list_sub   = [sub_x,sub_y,sub_z]
    #[e] initialize
 
    #UHF_mag = 0.1
    #UHF_co = 0.1
    Output_UHFInitial(list_org,UHF_mag,UHF_co)

def Output_UHFInitial(list_org,UHF_mag,UHF_co):
    All_N      = list_org[0]*list_org[1]*list_org[2]*list_org[3]
    Lx         = list_org[0]
    Ly         = list_org[1]
    orb_num    = list_org[3]
    tmp_N      = 0.75
    with open("initial.def", 'w') as f:
        print("=== " , file=f)
        print("N %d  "%(2*All_N) , file=f)
        print("=== " , file=f)
        print("=== " , file=f)
        print("=== " , file=f)
        for all_i in range(All_N):
             orb_i  = all_i%orb_num
             site_i = int((all_i-orb_i)/orb_num)
             x_i    = site_i%Lx
             y_i    = int((site_i-x_i)/Lx)
             #sgn    = math.cos(math.pi*x_i+math.pi*y_i)   
             #print(all_i,orb_i,x_i,y_i,sgn)
             if orb_i == 0:
                 print(" %d 0 %d 0 %f 0.0 "%(all_i,all_i,tmp_N+UHF_mag+UHF_co) , file=f)
                 print(" %d 1 %d 1 %f 0.0 "%(all_i,all_i,tmp_N-UHF_mag+UHF_co) , file=f)
             elif orb_i == 1:
                 print(" %d 0 %d 0 %f 0.0 "%(all_i,all_i,tmp_N-UHF_co) , file=f)
                 print(" %d 1 %d 1 %f 0.0 "%(all_i,all_i,tmp_N-UHF_co) , file=f)

if __name__ == "__main__":
    main()
