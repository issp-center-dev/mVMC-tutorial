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
    G2_ex     = np.full((max_num,All_N,All_N,2,2),-100,dtype=np.float)
    G2_sz     = np.full((max_num,All_N,All_N,2,2),-100,dtype=np.float)
    all_Sq    = np.full((max_num,list_tot[0]+1,list_tot[1]+1),-100,dtype=np.float)
    all_Sz    = np.full((max_num,list_tot[0]+1,list_tot[1]+1),-100,dtype=np.float)
    all_Nq    = np.full((max_num,list_tot[0]+1,list_tot[1]+1),-100,dtype=np.float)
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
    
        file_name ="{}".format(dir_name)+"/zvo_cisajscktalt_00"+"{0:1d}".format(num_bin)+".dat"

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
            if all_i == all_j and all_k == all_l and all_i==all_k:
                G2_sz[num_bin][all_i][all_j][spn_0][spn_1] = float(tmp[8])
                G2_ex[num_bin][all_i][all_j][spn_0][spn_1] = float(tmp[8])
            elif all_i == all_j and all_k == all_l:
                G2_sz[num_bin][all_i][all_k][spn_0][spn_1] = float(tmp[8])
            elif all_i == all_l and all_j == all_k:
                G2_ex[num_bin][all_i][all_j][spn_0][spn_1] = float(tmp[8])
            else:
                print("fatal error")
        #
        CalcSq_tot(list_tot,G1,G2_sz,G2_ex,dir_name,num_bin,all_Sq,all_Sz,all_Nq,all_Nk)
    #[e] calc Sq,Sz,Nq,Nk
    for num_bin in range(0,max_num):
        for all_i in range(0,All_N):
            charge[num_bin][all_i] = G1[num_bin][all_i][all_i][0]+G1[num_bin][all_i][all_i][1]
            spin[num_bin][all_i]   = G1[num_bin][all_i][all_i][0]-G1[num_bin][all_i][all_i][1]
    #
    ave_charge  = np.mean(charge,axis=0)
    err_charge  = np.std(charge,axis=0,ddof=1)
    ave_spin    = np.mean(spin,axis=0)
    err_spin    = np.std(spin,axis=0,ddof=1)
    with open("Real.dat", 'w') as f:
        for i_x in range(0,list_tot[0]):
            for i_y in range(0,list_tot[1]):
                all_i =  i_x+i_y*list_tot[0]
                print("%d %d %12.8f %12.8f %12.8f %12.8f" % (i_x,i_y,ave_charge[all_i],err_charge[all_i],ave_spin[all_i],err_spin[all_i]), file=f)
            print(" " , file=f)
    #
    #[s] Sq,Nq
    ave_Sq  = np.mean(all_Sq,axis=0)
    err_Sq  = np.std(all_Sq,axis=0,ddof=1)
    ave_Sz  = np.mean(all_Sz,axis=0)
    err_Sz  = np.std(all_Sz,axis=0,ddof=1)
    ave_Nq  = np.mean(all_Nq,axis=0)
    err_Nq  = np.std(all_Nq,axis=0,ddof=1)
    max_Sq  = 0.0
    max_Nq  = 0.0
    with open("SqNq.dat", 'w') as f:
        for kx in range(0,list_tot[0]+1):
            for ky in range(0,list_tot[1]+1):
                if ave_Sq[kx][ky] > max_Sq:
                    max_Sq     = ave_Sq[kx][ky] 
                    max_Sq_err = err_Sq[kx][ky] 
                    max_Sq_kx  = kx 
                    max_Sq_ky  = ky
                    #
                if ave_Nq[kx][ky] > max_Nq:
                    max_Nq     = ave_Nq[kx][ky] 
                    max_Nq_err = err_Nq[kx][ky] 
                    max_Nq_kx  = kx 
                    max_Nq_ky  = ky
                print("%d %d %12.8f %12.8f %12.8f %12.8f %12.8f %12.8f" % (kx,ky,ave_Sq[kx][ky],err_Sq[kx][ky],ave_Sz[kx][ky],err_Sz[kx][ky],ave_Nq[kx][ky],err_Nq[kx][ky]), file=f)
            print(" " , file=f)
    with open("MaxSq.dat", 'w') as f:
        print("%12.8f %12.8f  %d %d " % (max_Sq,max_Sq_err,max_Sq_kx,max_Sq_ky), file=f)
    #
    with open("MaxNq.dat", 'w') as f:
        print("%12.8f %12.8f  %d %d " % (max_Nq,max_Nq_err,max_Nq_kx,max_Nq_ky), file=f)
    #[e] Sq,Nq
    #[s] Nk
    ave_Nk  = np.mean(all_Nk,axis=0)
    err_Nk  = np.std(all_Nk,axis=0,ddof=1)
    with open("Nk.dat", 'w') as f:
        for kx in range(-list_tot[0],list_tot[0]+1):
            if kx <0:
                tmp_kx = kx+list_tot[0]
            else:
                tmp_kx = kx
            for ky in range(-list_tot[1],list_tot[1]+1):
                if ky <0:
                    tmp_ky = ky+list_tot[1]
                else:
                    tmp_ky = ky
                # kx
                print("%d %d %12.8f %12.8f " % (kx,ky,ave_Nk[tmp_kx][tmp_ky],err_Nk[tmp_kx][tmp_ky]), file=f)
            print(" " , file=f)
    #[e] Nk
 



def CalcSq_tot(list_org,G1,G2_sz,G2_ex,dir_name,num_bin,all_Sq,all_Sz,all_Nq,all_Nk):
    Lx        = list_org[0]
    Ly        = list_org[1]
    Lz        = list_org[2]
    orb_num   = list_org[3]
    All_N     = Lx*Ly*Lz*orb_num 
    with open("%s/total_SqNq_%d.dat" % (dir_name,num_bin), 'w') as f:
        for kx in range(0,Lx+1):
            for ky in range(0,Ly+1):
                tmp_Sq  = 0.0
                tmp_Sz  = 0.0
                tmp_Nq  = 0.0
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
                        tmp_uu  = G2_sz[num_bin][all_i][all_j][0][0]
                        tmp_ud  = G2_sz[num_bin][all_i][all_j][0][1]
                        tmp_du  = G2_sz[num_bin][all_i][all_j][1][0]
                        tmp_dd  = G2_sz[num_bin][all_i][all_j][1][1]

                        #
                        tmp_Nk += G1[num_bin][all_i][all_j][0]*math.cos(theta)
                        tmp_Nk += G1[num_bin][all_i][all_j][1]*math.cos(theta)
                        #
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
                        tmp_Sq += -0.5*G2_ex[num_bin][all_i][all_j][0][1]*math.cos(theta)
                        tmp_Sq += -0.5*G2_ex[num_bin][all_i][all_j][1][0]*math.cos(theta)
                tmp_Sq += Ncond/2
                if kx%Lx == 0 and ky%Ly ==0:
                   tmp_Nq = tmp_Nq- Ncond**2
                tmp_Sq  = tmp_Sq/(Lx*Ly)
                tmp_Sz  = tmp_Sz/(Lx*Ly)
                tmp_Nq  = tmp_Nq/(Lx*Ly)
                tmp_Nk  = tmp_Nk/(Lx*Ly)
                all_Sq[num_bin][kx][ky] = tmp_Sq
                print(num_bin,kx,ky)
                all_Sz[num_bin][kx][ky] = tmp_Sz
                all_Nq[num_bin][kx][ky] = tmp_Nq
                all_Nk[num_bin][kx][ky] = tmp_Nk
                #print(kx,ky,tmp_Sq,tmp_Sz,tmp_Nq)
                print("%d %d %12.8f %12.8f %12.8f " % (kx,ky,tmp_Sq,tmp_Sz,tmp_Nq), file=f)
            print(" " , file=f)
            #print(" ")

if __name__ == "__main__":
    main()
