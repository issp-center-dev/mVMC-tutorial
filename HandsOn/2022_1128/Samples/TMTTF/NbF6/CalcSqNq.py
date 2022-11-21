import numpy as np
import math
import sys
import toml
import cmath
import lattice #using read.py#

def CalcSq_decomp(list_org,G1,G2,dir_name):
    Lx        = list_org[0]
    Ly        = list_org[1]
    Lz        = list_org[2]
    orb_num   = list_org[3]
    All_N     = Lx*Ly*Lz*orb_num 
    with open("%s/decomp_SqNq_%d.dat" % (dir_name,num_cg), 'w') as f:
        for kx in range(0,Lx+1):
            for ky in range(0,Ly+1):
                tmp_Sq    = 0.0
                tmp_Sz_p  = 0.0
                tmp_Sz_m  = 0.0
                tmp_Nq_p  = 0.0
                tmp_Nq_m  = 0.0
                Ncond   = 0
                for all_i in range(0,All_N):
                    list_site       = lattice.func_site(all_i,list_org)
                    i_x             = list_site[0]
                    i_y             = list_site[1]
                    i_orb           = list_site[3]
                    i_sgn           = 2.0*(0.5-i_orb)
                    Ncond+=  G1[all_i][all_i][0]
                    Ncond+=  G1[all_i][all_i][1]
                    for all_j in range(0,All_N):
                        #
                        list_site       = lattice.func_site(all_j,list_org)
                        j_x             = list_site[0]
                        j_y             = list_site[1]
                        j_orb           = list_site[3]
                        j_sgn           = 2.0*(0.5-j_orb)
        
                        theta           = 2*math.pi*kx*(i_x-j_x)/Lx+2*math.pi*ky*(i_y-j_y)/Ly
                        #
                        tmp_uu  = G2[all_i][all_i][all_j][all_j][0][0]
                        tmp_ud  = G2[all_i][all_i][all_j][all_j][0][1]
                        tmp_du  = G2[all_i][all_i][all_j][all_j][1][0]
                        tmp_dd  = G2[all_i][all_i][all_j][all_j][1][1]

                        tmp_Nq_p += tmp_uu*math.cos(theta)
                        tmp_Nq_p += tmp_dd*math.cos(theta)
                        tmp_Nq_m += tmp_uu*math.cos(theta)*i_sgn*j_sgn
                        tmp_Nq_m += tmp_dd*math.cos(theta)*i_sgn*j_sgn
                        tmp_Sq += 0.25*tmp_uu*math.cos(theta)
                        tmp_Sq += 0.25*tmp_dd*math.cos(theta)
                        tmp_Sz_p += 0.25*tmp_uu*math.cos(theta)
                        tmp_Sz_p += 0.25*tmp_dd*math.cos(theta)
                        tmp_Sz_m += 0.25*tmp_uu*math.cos(theta)*i_sgn*j_sgn
                        tmp_Sz_m += 0.25*tmp_dd*math.cos(theta)*i_sgn*j_sgn
                        #
                        tmp_Nq_p += tmp_ud*math.cos(theta)
                        tmp_Nq_p += tmp_du*math.cos(theta)
                        tmp_Nq_m += tmp_ud*math.cos(theta)*i_sgn*j_sgn
                        tmp_Nq_m += tmp_du*math.cos(theta)*i_sgn*j_sgn
                        tmp_Sq += -0.25*tmp_ud*math.cos(theta)
                        tmp_Sq += -0.25*tmp_du*math.cos(theta)
                        tmp_Sz_p += -0.25*tmp_ud*math.cos(theta)
                        tmp_Sz_p += -0.25*tmp_du*math.cos(theta)
                        tmp_Sz_m += -0.25*tmp_ud*math.cos(theta)*i_sgn*j_sgn
                        tmp_Sz_m += -0.25*tmp_du*math.cos(theta)*i_sgn*j_sgn
                        #
                        tmp_Sq += -0.5*G2[all_i][all_j][all_j][all_i][0][1]*math.cos(theta)
                        tmp_Sq += -0.5*G2[all_i][all_j][all_j][all_i][1][0]*math.cos(theta)
                tmp_Sq += Ncond/2
                if kx%Lx == 0 and ky%Ly ==0:
                   tmp_Nq_p = tmp_Nq_p - Ncond**2
                tmp_Sq    = tmp_Sq/(Lx*Ly)
                tmp_Sz_p  = tmp_Sz_p/(Lx*Ly)
                tmp_Sz_m  = tmp_Sz_m/(Lx*Ly)
                tmp_Nq_p  = tmp_Nq_p/(Lx*Ly)
                tmp_Nq_m  = tmp_Nq_m/(Lx*Ly)
                #print(kx,ky,tmp_Sq,tmp_Sz,tmp_Nq)
                print("%d %d %12.8f %12.8f %12.8f %12.8f %12.8f" % (kx,ky,tmp_Sq,tmp_Sz_p,tmp_Sz_m,tmp_Nq_p,tmp_Nq_m), file=f)
            print(" " , file=f)
            #print(" ")



def CalcSq_tot(list_org,G1,G2,dir_name):
    Lx        = list_org[0]
    Ly        = list_org[1]
    Lz        = list_org[2]
    orb_num   = list_org[3]
    All_N     = Lx*Ly*Lz*orb_num 
    with open("%s/total_SqNq_%d.dat" % (dir_name,num_cg), 'w') as f:
        for kx in range(0,Lx+1):
            for ky in range(0,Ly+1):
                tmp_Sq  = 0.0
                tmp_Sz  = 0.0
                tmp_Nq  = 0.0
                Ncond   = 0
                for all_i in range(0,All_N):
                    Ncond+=  G1[all_i][all_i][0]
                    Ncond+=  G1[all_i][all_i][1]
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
                        tmp_uu  = G2[all_i][all_i][all_j][all_j][0][0]
                        tmp_ud  = G2[all_i][all_i][all_j][all_j][0][1]
                        tmp_du  = G2[all_i][all_i][all_j][all_j][1][0]
                        tmp_dd  = G2[all_i][all_i][all_j][all_j][1][1]

                        tmp_Nq += tmp_uu*math.cos(theta)
                        tmp_Nq += tmp_dd*math.cos(theta)
                        tmp_Sq += 0.25*tmp_uu*math.cos(theta)
                        tmp_Sq += 0.25*tmp_dd*math.cos(theta)
                        tmp_Sz += 0.25*tmp_uu*math.cos(theta)
                        tmp_Sz += 0.25*tmp_dd*math.cos(theta)
                        #
                        tmp_Nq += tmp_ud*math.cos(theta)
                        tmp_Nq += tmp_du*math.cos(theta)
                        tmp_Sq += -0.25*tmp_ud*math.cos(theta)
                        tmp_Sq += -0.25*tmp_du*math.cos(theta)
                        tmp_Sz += -0.25*tmp_ud*math.cos(theta)
                        tmp_Sz += -0.25*tmp_du*math.cos(theta)
                        #
                        tmp_Sq += -0.5*G2[all_i][all_j][all_j][all_i][0][1]*math.cos(theta)
                        tmp_Sq += -0.5*G2[all_i][all_j][all_j][all_i][1][0]*math.cos(theta)
                tmp_Sq += Ncond/2
                if kx%Lx == 0 and ky%Ly ==0:
                   tmp_Nq = tmp_Nq- Ncond**2
                tmp_Sq  = tmp_Sq/(Lx*Ly)
                tmp_Sz  = tmp_Sz/(Lx*Ly)
                tmp_Nq  = tmp_Nq/(Lx*Ly)
                #print(kx,ky,tmp_Sq,tmp_Sz,tmp_Nq)
                print("%d %d %12.8f %12.8f %12.8f " % (kx,ky,tmp_Sq,tmp_Sz,tmp_Nq), file=f)
            print(" " , file=f)
            #print(" ")

dir_name = sys.argv[2]
max_num  = 1
#[s] tolm load
input_file  = sys.argv[1] 
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
G1        = np.zeros((All_N,All_N,2),dtype=np.float)
G2        = np.full((All_N,All_N,All_N,All_N,2,2),-100,dtype=np.float)
#[e] allocate

#dir_output = "old_VBS"
for num_cg in range(0,max_num):
    file_name ="{}".format(dir_name)+"/zvo_cisajs_eigen"+"{0:1d}".format(num_cg)+".dat"

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
        G1[all_i][all_j][spn] = float(tmp[4])
 
    file_name ="{}".format(dir_name)+"/zvo_cisajscktalt_eigen"+"{0:1d}".format(num_cg)+".dat"

    with open(file_name) as f:
        data      = f.read()
        data      = data.split("\n")
        print(len(data))
    #[s] count not empty elements
    cnt = 0
    for i in range(0,len(data)):
        if data[i]: # if data[i] is not empty
            cnt += 1
    #print(cnt)
    cnt_max = cnt
    #[e] count not empty elements
    for cnt in range(0,cnt_max):
        tmp                   = data[cnt].split()  
        all_i                 = int(tmp[0]) 
        all_j                 = int(tmp[2]) 
        all_k                 = int(tmp[4]) 
        all_l                 = int(tmp[6]) 
        spn_0                 = int(tmp[1])
        spn_1                 = int(tmp[5])
        G2[all_i][all_j][all_k][all_l][spn_0][spn_1] = float(tmp[8])
    #
    CalcSq_tot(list_tot,G1,G2,dir_name)
    CalcSq_decomp(list_org,G1,G2,dir_name)
