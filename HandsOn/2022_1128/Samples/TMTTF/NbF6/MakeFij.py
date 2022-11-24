import numpy as np
import math
import cmath
import sys
import toml
import random

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
    dx = np.zeros([4],dtype=np.int)
    dy = np.zeros([4],dtype=np.int)
    # 
    dx[0]      = 0
    dy[0]      = 0
    #
    dx[1]      = 1
    dy[1]      = 0
    #
    dx[2]      = 0
    dy[2]      = 1
    #
    dx[3]      = 1
    dy[3]      = 1
    #[e] initialize
 
 
    Fij_num           = np.zeros([All_N,All_N],dtype=np.int)
    Fij_real          = np.zeros([All_N,All_N],dtype=np.float)
    Fij_imag          = np.zeros([All_N,All_N],dtype=np.float)
    # 
    file_Fij          =  "zqp_AP_Fij.dat" 
    Fij_real,Fij_imag = ReadFij(file_Fij,All_N)
    Fij_num,cnt_max   = ReadOrbital("APOrbital.def",All_N)
    # 
    Non_Ave_Fij_real  = np.zeros([cnt_max],dtype=np.float)
    Non_Ave_Fij_imag  = np.zeros([cnt_max],dtype=np.float)
    Ave_Fij_real      = np.zeros([cnt_max],dtype=np.float)
    Ave_Fij_imag      = np.zeros([cnt_max],dtype=np.float)
    Ave_cnt           = np.zeros([cnt_max],dtype=np.int)
    with open("Fij.dat", 'w') as f:
        print("==== ", file=f)
        print("N %d " % (cnt_max), file=f)
        print("==== ", file=f)
        print("==== ", file=f)
        print("==== ", file=f)
        for ini_i in range(4):
            i_x = dx[ini_i]
            i_y = dy[ini_i]
            for orb_i in range(orb_num):
                all_i = orb_i+(i_x+i_y*Lx)*orb_num
                for all_j in range(All_N):
                    tmp_num = Fij_num[all_i][all_j] 
                    tmp_fij = Fij_real[all_i][all_j]
                    Non_Ave_Fij_real[tmp_num] = Fij_real[all_i][all_j]
                    Non_Ave_Fij_imag[tmp_num] = Fij_imag[all_i][all_j]
        for tmp_num in range(cnt_max):
            print("%d %f %f " % (tmp_num,Non_Ave_Fij_real[tmp_num],Non_Ave_Fij_imag[tmp_num]), file=f)

    with open("Fij_AddRand.dat", 'w') as f:
        print("==== ", file=f)
        print("N %d " % (cnt_max), file=f)
        print("==== ", file=f)
        print("==== ", file=f)
        print("==== ", file=f)
        for ini_i in range(4):
            i_x = dx[ini_i]
            i_y = dy[ini_i]
            for orb_i in range(orb_num):
                all_i = orb_i+(i_x+i_y*Lx)*orb_num
                for all_j in range(All_N):
                    tmp_num = Fij_num[all_i][all_j] 
                    tmp_fij = Fij_real[all_i][all_j]
                    Non_Ave_Fij_real[tmp_num] = Fij_real[all_i][all_j]
                    Non_Ave_Fij_imag[tmp_num] = Fij_imag[all_i][all_j]
        for tmp_num in range(cnt_max):
            tmp_fij= Non_Ave_Fij_real[tmp_num]+random.uniform(-1.0,1.0)*1e-2 
            print("%d %f %f " % (tmp_num,tmp_fij,Non_Ave_Fij_imag[tmp_num]), file=f)
 
    

    with open("Ave_Fij.dat", 'w') as f:
        print("==== ", file=f)
        print("N %d " % (cnt_max), file=f)
        print("==== ", file=f)
        print("==== ", file=f)
        print("==== ", file=f)
        for all_i in range(All_N):
            for all_j in range(All_N):
                tmp_num                = Fij_num[all_i][all_j] 
                Ave_Fij_real[tmp_num] += Fij_real[all_i][all_j]
                Ave_Fij_imag[tmp_num] += Fij_imag[all_i][all_j]
                Ave_cnt[tmp_num] += 1  
                #print(all_i,all_j,tmp_num,tmp_fij)
        for tmp_num in range(cnt_max):
            if Ave_cnt[tmp_num] == 0:
                print(tmp_num, Ave_Fij[tmp_num])
            tmp_fij_real = Ave_Fij_real[tmp_num]/Ave_cnt[tmp_num] 
            tmp_fij_imag = Ave_Fij_imag[tmp_num]/Ave_cnt[tmp_num] 
            print("%d %f %f " % (tmp_num,tmp_fij_real,tmp_fij_imag), file=f)

def ReadFij(file_name,All_N):
    #[s] allocate
    Fij_real        = np.zeros((All_N,All_N),dtype=np.float)
    Fij_imag        = np.zeros((All_N,All_N),dtype=np.float)
    #[e] allocate

    with open(file_name) as f:
        tmp      = f.read()
        tmp      = tmp.split("\n")
    #[s] count not empty elements
    cnt_max = len(tmp)
    print(cnt_max)
    #[e] count not empty elements
    for cnt in range(0,cnt_max-1):
        tmp_2                  = tmp[cnt].split()  
        all_i                  = int(tmp_2[0]) 
        all_j                  = int(tmp_2[1]) 
        Fij_real[all_i][all_j] = float(tmp_2[2])
        Fij_imag[all_i][all_j] = float(tmp_2[3])
    return Fij_real,Fij_imag

def ReadOrbital(file_name,All_N):
    #[s] allocate
    Fij_num       = np.zeros((All_N,All_N),dtype=np.int)
    #[e] allocate
    with open(file_name) as f:
        tmp      = f.read()
        tmp      = tmp.split("\n")
    #[s] count not empty elements
    tmp_2   = tmp[1].split()  
    cnt_max = int(tmp_2[1])
    print(tmp_2)
    #[e] count not empty elements
    for cnt in range(5,All_N*All_N+5):
        tmp_2                 = tmp[cnt].split()  
        all_i                 = int(tmp_2[0])
        all_j                 = int(tmp_2[1])
        Fij_num[all_i][all_j] = int(tmp_2[2])
    return Fij_num,cnt_max

if __name__ == "__main__":
    main()  
