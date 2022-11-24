import numpy as np
import math
import sys
import toml
import cmath
import lattice #using read.py#

def main():
    input_file  = sys.argv[1] 
    dir_name    = sys.argv[2]
    max_num     = 5
    #[s] tolm load
    input_dict  = toml.load(input_file)
    #[e] tolm load
    # ignoring orbital degrees of freedom
    Lx            = int(input_dict["lattice"]["Lx"])
    Ly            = int(input_dict["lattice"]["Ly"])
    Lz            = int(input_dict["lattice"]["Lz"])
    orb_num       = int(input_dict["lattice"]["orb_num"])
    print('Lx = ',Lx)
    print('Ly = ',Ly)
    print('Lz = ',Lz)
    print('orb_num = ',orb_num)

    All_N = Lx*Ly*Lz*orb_num

    #[s] initialize
    list_tot   = [Lx*orb_num,Ly,Lz,1]
    list_org   = [Lx,Ly,Lz,orb_num]
    #[e] initialize

    #[s] allocate
    G1        = np.zeros((max_num,All_N,All_N,2),dtype=np.float)
    charge    = np.zeros((max_num,All_N),dtype=np.float)
    spin      = np.zeros((max_num,All_N),dtype=np.float)
    all_Nk    = np.full((max_num,list_tot[0]+1,list_tot[1]+1),-100,dtype=np.float)
    #[e] allocate

    #[s] calc Sq,Sz,Nq,Nk
    for num_bin in range(0,max_num):
        file_name ="{}".format(dir_name)+"/zvo_cisajs_00"+"{0:1d}".format(num_bin)+".dat"

        with open(file_name) as f:
            tmp_G1      = f.read()
            tmp_G1      = tmp_G1.split("\n")
            print(len(tmp_G1))
        #[s] count not empty elements
        cnt = 0
        for i in range(0,len(tmp_G1)):
            if tmp_G1[i]: # if data[i] is not empty
                cnt += 1
        #print(cnt)
        cnt_max = cnt
        #[e] count not empty elements
        for cnt in range(0,cnt_max):
            tmp                   = tmp_G1[cnt].split()  
            all_i                 = int(tmp[0]) 
            all_j                 = int(tmp[2]) 
            spn                   = int(tmp[1])
            #print(tmp)
            G1[num_bin][all_i][all_j][spn] = float(tmp[4])
        #
        CalcNk(list_org,G1,dir_name,num_bin,all_Nk)
    #[e] calc Sq,Sz,Nq,Nk
    for num_bin in range(0,max_num):
        for all_i in range(0,All_N):
            charge[num_bin][all_i] = G1[num_bin][all_i][all_i][0]+G1[num_bin][all_i][all_i][1]
            spin[num_bin][all_i]   = G1[num_bin][all_i][all_i][0]-G1[num_bin][all_i][all_i][1]
    #
    #[s] Nk
    ave_Nk  = np.mean(all_Nk,axis=0)
    err_Nk  = np.std(all_Nk,axis=0,ddof=1)
    with open("Nk.dat", 'w') as f:
        for kx in range(-int(list_org[0]/2),int(list_org[0]/2)+1):
            if kx <0:
                tmp_kx = -kx
            else:
                tmp_kx = kx
            for ky in range(-list_org[1],list_org[1]+1):
                if ky <0:
                    tmp_ky = -ky
                else:
                    tmp_ky = ky
                # kx
                print("%d %d %12.8f %12.8f " % (kx,ky,ave_Nk[tmp_kx][tmp_ky],err_Nk[tmp_kx][tmp_ky]), file=f)
            print(" " , file=f)
    #[e] Nk
 

def CalcNk(list_org,G1,dir_name,num_bin,all_Nk):
    Lx        = list_org[0]
    Ly        = list_org[1]
    Lz        = list_org[2]
    orb_num   = list_org[3]
    All_N     = Lx*Ly*Lz*orb_num 
    with open("%s/total_Nk_%d.dat" % (dir_name,num_bin), 'w') as f:
        for kx in range(0,Lx+1):
            for ky in range(0,Ly+1):
                tmp_Nk  = 0.0
                Ncond   = 0
                for all_i in range(0,All_N):
                    Ncond+=  G1[num_bin][all_i][all_i][0]
                    Ncond+=  G1[num_bin][all_i][all_i][1]
                    for all_j in range(0,All_N):
                        list_site       = lattice.func_site(all_i,list_org)
                        i_x             = list_site[0]
                        i_y             = list_site[1]
                        #
                        list_site       = lattice.func_site(all_j,list_org)
                        j_x             = list_site[0]
                        j_y             = list_site[1]
        
                        theta           = 2*math.pi*kx*(i_x-j_x)/Lx+2*math.pi*ky*(i_y-j_y)/Ly
                        #
                        tmp_Nk += G1[num_bin][all_i][all_j][0]*math.cos(theta)
                        tmp_Nk += G1[num_bin][all_i][all_j][1]*math.cos(theta)
                        #
                tmp_Nk  = tmp_Nk/(Lx*Ly)
                all_Nk[num_bin][kx][ky] = tmp_Nk
                #print(kx,ky,tmp_Sq,tmp_Sz,tmp_Nq)
                print("%d %d %12.8f  " % (kx,ky,tmp_Nk), file=f)
            print(" " , file=f)
            #print(" ")

if __name__ == "__main__":
    main()
