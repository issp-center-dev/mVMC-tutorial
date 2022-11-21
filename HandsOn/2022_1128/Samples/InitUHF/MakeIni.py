import cmath
import math
import sys

import numpy as np
import toml

import qlms_lattice


def main():
    #[s] tolm load
    input_file  = sys.argv[1] 
    input_dict  = toml.load(input_file)
    #[e] tolm load
    #[s]define constants
    Lx            = int(input_dict["lattice"]["Lx"])
    Ly            = int(input_dict["lattice"]["Ly"])
    Lz            = int(input_dict["lattice"]["Lz"])
    orb_num       = int(input_dict["lattice"]["orb_num"])
    sub_x         = int(input_dict["mVMC"]["sub_x"])
    sub_y         = int(input_dict["mVMC"]["sub_y"])
    sub_z         = int(input_dict["mVMC"]["sub_z"])
    #[e]define constants
    All_N = Lx*Ly*Lz*orb_num
    print('Lx    = ',Lx)
    print('Ly    = ',Lx)
    print('sub_x = ',sub_x)
    print('sub_y = ',sub_x)

    #[s] initialize
    list_org   = [Lx,Ly,Lz,orb_num]
    #[e] initialize
    #[s] output StdFace files
    OutputIniGreen(list_org)
    #[s] output StdFace files

def OutputIniGreen(list_org): 
    Intensity = 0.1
    Qx        = math.pi
    Qy        = math.pi
    All_N = list_org[0]*list_org[1]*list_org[2]*list_org[3]

    with open("initial.def", 'w') as f:
        print("==================", file=f)
        print("initial %d "%(2*All_N), file=f)
        print("==================", file=f)
        print("==================", file=f)
        print("==================", file=f)
        for all_i in range(0,All_N):
            list_site = qlms_lattice.get_site(all_i,list_org)
            x_i       = list_site[0]
            y_i       = list_site[1]
            theta     = Qx*x_i+Qy*y_i
            mag_re    = Intensity*math.cos(theta)
            mag_im    = 0.0
            print(" %d %d %d %d %f %f "% (all_i,0,all_i,0,mag_re,mag_im), file=f)
            print(" %d %d %d %d %f %f "% (all_i,1,all_i,1,-1.0*mag_re,mag_im), file=f)





if __name__ == "__main__":
    main()
