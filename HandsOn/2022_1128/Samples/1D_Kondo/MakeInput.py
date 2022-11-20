import numpy as np
import math
import cmath
import toml
import sys

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
    Ncond = int(All_N/2)
    print('Lx    = ',Lx)
    print('sub_x = ',sub_x)
    print('Ncond = ',Ncond)

    #[s] initialize
    list_org   = [Lx,Ly,Lz,orb_num]
    list_sub   = [sub_x,sub_y,sub_z]
    #[e] initialize
    #[s] output StdFace files
    OutputStdFace(list_org,list_sub,Ncond)
    #[s] output StdFace files
    #[s] output StdFace files
    OutputGreen(list_org)
    #[s] output StdFace files

def OutputStdFace(list_org,list_sub,Ncond):
    Lx      = list_org[0]
    Ly      = list_org[1]
    Lz      = list_org[2]
    orb_num = list_org[3]
    sub_x   = list_sub[0]
    sub_y   = list_sub[1]
    sub_z   = list_sub[2]
    with open("StdFace.def", 'w') as f:
        print("L             = %d       "%(Lx),file=f)
        print("Lsub          = %d       "%(sub_x),file=f)
        print("model         = \"kondo\" ",file=f)
        print("lattice       = \"chain\"",file=f)
        print("t             = 1.0      ",file=f)
        print("J             = 1.0      ",file=f)
        print("2Sz           = 0        ",file=f)
        print("ncond         = %d       "%(Ncond),file=f)
        print("NVMCSample    = 200      ",file=f)
        print("NSROptItrStep = 600      ",file=f)
        print("NMPTrans      = 1        ",file=f)
        print("NSPStot       = 0        ",file=f)

    with open("StdFace_aft.def", 'w') as f:
        print("L             = %d       "%(Lx),file=f)
        print("Lsub          = %d       "%(sub_x),file=f)
        print("model         = \"Kondo\" ",file=f)
        print("lattice       = \"chain\"",file=f)
        print("t             = 1.0      ",file=f)
        print("J             = 1.0      ",file=f)
        print("2Sz           = 0        ",file=f)
        print("ncond         = %d       "%(Ncond),file=f)
        print("NVMCSample    = 200      ",file=f)
        print("NSROptItrStep = 600      ",file=f)
        print("NMPTrans      = 1        ",file=f)
        print("NSPStot       = 0        ",file=f)
        print("NVMCCalMode   = 1        ",file=f)
        print("NDataIdxStart = 0        ",file=f)
        print("NDataQtySmp   = 5        ",file=f)

def OutputGreen(list_org): 
    All_N = list_org[0]*list_org[1]*list_org[2]*list_org[3]

    with open("green1.def", 'w') as f:
        print("==================", file=f)
        print("onebody %d "%(2*All_N**2), file=f)
        print("==================", file=f)
        print("==================", file=f)
        print("==================", file=f)
        for all_i in range(0,All_N):
            for all_j in range(0,All_N):
                print(" %d %d %d %d "% (all_i,0,all_j,0), file=f)
                print(" %d %d %d %d "% (all_i,1,all_j,1), file=f)

    with open("green2.def", 'w') as f:
        print("==================", file=f)
        print("twobody %d "%(6*All_N**2), file=f)
        print("==================", file=f)
        print("==================", file=f)
        print("==================", file=f)
        for all_i in range(0,All_N):
            for all_j in range(0,All_N):
                print(" %d %d %d %d %d %d %d %d"% (all_i,0,all_i,0,all_j,0,all_j,0), file=f)
                print(" %d %d %d %d %d %d %d %d"% (all_i,0,all_i,0,all_j,1,all_j,1), file=f)
                print(" %d %d %d %d %d %d %d %d"% (all_i,1,all_i,1,all_j,0,all_j,0), file=f)
                print(" %d %d %d %d %d %d %d %d"% (all_i,1,all_i,1,all_j,1,all_j,1), file=f)
                #
                print(" %d %d %d %d %d %d %d %d"% (all_i,0,all_j,0,all_j,1,all_i,1), file=f)
                print(" %d %d %d %d %d %d %d %d"% (all_i,1,all_j,1,all_j,0,all_i,0), file=f)
 




if __name__ == "__main__":
    main()
