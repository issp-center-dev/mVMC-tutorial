import numpy as np
import math
import cmath
import sys
import lattice #using read.py#
import toml    #using toml.py#

def main():
    input_file  = sys.argv[1]
    dir_name    = sys.argv[2]
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
    max_sample = 5

    #[s] initialize
    list_org = [Lx,Ly,Lz,orb_num]
    #list_site  = [0,0,0,0]  # x,y,z,orb
    #[e] initialize
    tot_Ene    = np.zeros([max_sample], dtype=np.float)
    tot_occ    = np.zeros([max_sample,orb_num], dtype=np.float)
    tot_AF     = np.zeros([max_sample,orb_num], dtype=np.float)
    for i_smp in range(max_sample):
        file_name = "%s/zvo_cisajs_00%d.dat" % (dir_name,i_smp)
        occ,AF    = ReadG1(file_name,list_org,i_smp)
        for orb_i in range(orb_num):
            tot_occ[i_smp][orb_i] = occ[orb_i] 
            tot_AF[i_smp][orb_i]  = AF[orb_i] 
        #
        file_name = "%s/zvo_out_00%d.dat" % (dir_name,i_smp)
        tot_Ene[i_smp] = ReadEne(file_name,list_org,i_smp)

    Ave_Ene = np.mean(tot_Ene,axis=0)
    Err_Ene = np.std(tot_Ene,axis=0,ddof=1)/math.sqrt(1.0*max_sample)
    # 
    Ave_occ = np.mean(tot_occ,axis=0)
    Err_occ = np.std(tot_occ,axis=0,ddof=1)/math.sqrt(1.0*max_sample)
    Ave_AF  = np.mean(tot_AF,axis=0)
    Err_AF  = np.std(tot_AF,axis=0,ddof=1)/math.sqrt(1.0*max_sample)
    
    print(Ave_Ene,Err_Ene,Ave_Ene/(Lx*Ly),Err_Ene/(Lx*Ly))
    print(Ave_occ)
    #print(Ave_AF)
    with open("Ene.dat", 'w') as f:
        print("%f %f %f %f" % (Ave_Ene,Err_Ene,Ave_Ene/(Lx*Ly),Err_Ene/(Lx*Ly)),file=f)
    with open("occ.dat", 'w') as f:
        for orb_i in range(orb_num):
            print("%f %f " % (Ave_occ[orb_i],Err_occ[orb_i]),end="",file=f)
        print(" " ,file=f)
    with open("AF.dat", 'w') as f:
        for orb_i in range(orb_num):
            print("%f %f " % (Ave_AF[orb_i],Err_AF[orb_i]),end="",file=f)
        print(" " ,file=f)

def ReadEne(file_name,list_org,i_smp):
    with open(file_name) as f:
        data      = f.read()
        data      = data.split("\n")
        #print(len(data))
    tmp     = data[0].split()
    tmp_Ene = tmp[0]
    return tmp_Ene
 
 

def ReadG1(file_name,list_org,i_smp):
    Lx       = list_org[0]
    Ly       = list_org[1]
    orb_num  = list_org[3]
    #file_name = "output/zvo_aft_cisajs_001.dat" 
    with open(file_name) as f:
        data      = f.read()
        data      = data.split("\n")
        #print(len(data))
    #[s] count not empty elements
    cnt = 0
    all_occ = np.zeros([Lx*Ly,orb_num,2], dtype=np.float)
    occ     = np.zeros([orb_num], dtype=np.float)
    AF      = np.zeros([orb_num], dtype=np.float)
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
                    occ[orb_i]       += float(tmp[4])   
                    all_occ[site_i][orb_i][0] = float(tmp[4])     
                    AF[orb_i]    +=sgn*float(tmp[4]) 
                if tmp[1] == tmp[3] and int(tmp[1]) == 1: 
                    occ[orb_i]       += float(tmp[4])   
                    all_occ[site_i][orb_i][1]  =float(tmp[4])     
                    AF[orb_i]    +=-sgn*float(tmp[4]) 
    with open("Real_sample%d.dat" % (i_smp), 'w') as f:
        for x_i in range(0,Lx):
            for y_i in range(0,Ly):
                site_i = x_i + y_i*Lx
                print("%d %d " % (x_i,y_i),end=" ",file=f)
                for orb_i in range(orb_num):
                    print("%f %f " % (all_occ[site_i][orb_i][0],all_occ[site_i][orb_i][1]),end=" ",file=f)
                print(" ",file=f)
            print(" ",file=f)
    #[e] count not empty elements
    occ   = occ/(Lx*Ly)
    AF    = AF/(Lx*Ly)
    #print(AF)
    #print(occ)
    #print(2-occ)
    return occ,AF
 


if __name__ == "__main__":
    main()
