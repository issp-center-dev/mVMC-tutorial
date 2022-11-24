import numpy as np
import math
import cmath
import sys
import toml
import lattice 

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
 
    file_name = "zvo_UHF_cisajs.dat" 
    with open(file_name) as f:
        data      = f.read()
        data      = data.split("\n")
        print(len(data))
    #[s] count not empty elements
    cnt = 0
    occ     = np.zeros([Lx*Ly,orb_num,2], dtype=np.float)
    tot_occ = np.zeros([orb_num], dtype=np.float)
    for i in range(0,len(data)):
        if data[i]: # if data[i] is not empty
            tmp = data[i].split()
            if tmp[0] == tmp[2]:
                all_i = int(tmp[0])
                orb_i = all_i%orb_num
                site_i = int((all_i-orb_i)/orb_num)
                x_i    = site_i%Lx
                y_i    = int((site_i-x_i)/Lx)
                sgn    = math.cos(math.pi*x_i+math.pi*y_i)   
                if tmp[1] == tmp[3] and int(tmp[1]) == 0: 
                    tot_occ[orb_i]       += float(tmp[4])   
                    occ[site_i][orb_i][0] = float(tmp[4])     
                if tmp[1] == tmp[3] and int(tmp[1]) == 1: 
                    tot_occ[orb_i]       += float(tmp[4])   
                    occ[site_i][orb_i][1]  =float(tmp[4])     
    for orb_i in range(0,orb_num):
        with open("Real_%d.dat" % (orb_i), 'w') as f:
             for x_i in range(0,Lx):
                 for y_i in range(0,Ly):
                     site_i = x_i + y_i*Lx
                     all_i  = orb_i+site_i*orb_num
                     print(orb_i,site_i)
                     charge = occ[site_i][orb_i][0]+occ[site_i][orb_i][1]
                     spin   = occ[site_i][orb_i][0]-occ[site_i][orb_i][1]
                     print("%d %d %f %f " % (x_i,y_i,charge,spin),file=f)
                 print(" ",file=f)
    #[e] count not empty elements
    tot_occ   = tot_occ/(Lx*Ly)
    print(tot_occ)
    print(2-tot_occ)
    with open("UHF_occ.dat", 'w') as f:
        print("%f %f  " % (tot_occ[0],tot_occ[1]),file=f)
        print("%f %f  " % (2-tot_occ[0],2-tot_occ[1]),file=f)



if __name__ == "__main__":
    main()
