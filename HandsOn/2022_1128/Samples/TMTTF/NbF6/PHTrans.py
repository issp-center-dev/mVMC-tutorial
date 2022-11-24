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
    list_site  = [0,0,0,0]  # x,y,z,orb
    #[e] initialize

    mag_SiteI,mag_SpinI,mag_SiteJ,mag_SpinJ,Trans_mag_Re,Trans_mag_Im = Trans("mag_trans.def")
    SiteI,SpinI,SiteJ,SpinJ,Trans_Re,Trans_Im = Trans("trans.def")
    USiteI,all_U = OnsiteCoulomb("coulombintra.def")
    VSiteI,VSiteJ,all_V = OffsiteCoulomb("coulombinter.def")

    PH,const = Make_CorrectMu(USiteI,all_U,VSiteI,VSiteJ,all_V,list_org)
   # print(PH,const)

    #[s] define staggaered magnetic field
    AF    = np.zeros([orb_num], dtype=np.float64)
    AF[0] = 0
    AF[1] = 0
    #[e] define staggaered magnetic field
    const_mu=Output_AllTrans(SiteI,SpinI,SiteJ,SpinJ,Trans_Re,Trans_Im,Trans_mag_Re,Trans_mag_Im,orb_num,AF,PH)
    print(const+const_mu,const_mu,const)
    with open("const.dat", 'w') as f:
        print(const+const_mu,const_mu,const,file=f)

def Output_AllTrans(SiteI,SpinI,SiteJ,SpinJ,Trans_Re,Trans_Im,Trans_mag_Re,Trans_mag_Im,orb_num,AF,PH):
    cnt_max = len(SiteI)
    print(cnt_max)
    with open("mag_trans_PH.def", 'w') as f:
        print("====== ", file=f)
        print("%s %d " % ('N', cnt_max), file=f)
        print("====== ", file=f)
        print("====== ", file=f)
        print("====== ", file=f)
        for cnt in range(cnt_max):
            all_i = SiteI[cnt]
            spn_i = SpinI[cnt]
            all_j = SiteJ[cnt]
            spn_j = SpinJ[cnt]
            if spn_i != spn_j:
                print("fatal error")
            else:
                sgn = 2.0*(spn_i-0.5)
            if all_i == all_j:
                orb_i   = int(all_i%orb_num)
                mu      = -Trans_mag_Re[cnt]
                mu_PH   = -mu-PH[all_i]
                print("%8d %8d %8d %8d %.15f 0.0 " % (all_i,spn_i,all_i,spn_i,-mu_PH), file=f)
            else:
                print("%8d %8d %8d %8d %.15f 0.0 " % (all_i,spn_i,all_j,spn_j,-Trans_Re[cnt]), file=f)

    tmp_const = 0
    with open("trans_PH.def", 'w') as f:
        print("====== ", file=f)
        print("%s %d " % ('N', cnt_max), file=f)
        print("====== ", file=f)
        print("====== ", file=f)
        print("====== ", file=f)
        for cnt in range(cnt_max):
            all_i = SiteI[cnt]
            spn_i = SpinI[cnt]
            all_j = SiteJ[cnt]
            spn_j = SpinJ[cnt]
            if spn_i != spn_j:
                print("fatal error")
            if all_i == all_j:
                orb_i   = int(all_i%orb_num)
                mu      = -Trans_Re[cnt]
                mu_PH   = -mu-PH[all_i]
                #print(all_i,orb_i,mu_PH,-mu,PH[all_i])
                tmp_const += mu
                print("%8d %8d %8d %8d %.15f 0.0 " % (all_i,spn_i,all_i,spn_i,-mu_PH), file=f)
            else:
                print("%8d %8d %8d %8d %.15f 0.0 " % (all_i,spn_i,all_j,spn_j,-Trans_Re[cnt]), file=f)
    return tmp_const


def Make_CorrectMu(USiteI,all_U,VSiteI,VSiteJ,all_V,list_org):
    All_N      = list_org[0]*list_org[1]*list_org[2]*list_org[3]
    orb_num    = list_org[3]
    tmp_PH     = np.zeros([All_N], dtype=np.float64)
    tmp_const  = 0.0

    #check_cnt    = np.zeros([orb_num], dtype=np.float64)
    for cnt in range(len(USiteI)):
        all_i          = USiteI[cnt]
        tmp_PH[all_i] += all_U[cnt]
        tmp_const     += all_U[cnt]

    for cnt in range(len(VSiteI)):
        all_i          = VSiteI[cnt]
        all_j          = VSiteJ[cnt]
        #print(cnt,all_i,all_j,all_V[cnt])
        tmp_PH[all_i] += 2*all_V[cnt]
        tmp_PH[all_j] += 2*all_V[cnt]
        tmp_const     += 4*all_V[cnt]

    return tmp_PH,tmp_const

def OffsiteCoulomb(file_name):
    #[s] file name
    #[e] file name
    #print(file_name)
    with open(file_name) as f:
        data = f.read()
        data = data.split("\n")
    print(len(data))
    #[s] count R1R1R2R2 density-density int
    cnt_max     = len(data)-6
    SiteI       = np.zeros([cnt_max], dtype=np.int64)
    SiteJ       = np.zeros([cnt_max], dtype=np.int64)
    Param_Re    = np.zeros([cnt_max], dtype=np.float64)
    for cnt_i in range(5,len(data)-1):
        cnt = cnt_i -5
        if len(data[cnt_i]) > 0: # if data[i] is not empty
            tmp           = data[cnt_i].split()
            SiteI[cnt]    = int(tmp[0])
            SiteJ[cnt]    = int(tmp[1])
            Param_Re[cnt] = float(tmp[2])
    #[e] count R1R1R2R2 density-density
    #cnt_max = cnt
    return SiteI,SiteJ,Param_Re



def OnsiteCoulomb(file_name):
    #[s] file name
    #[e] file name
    #print(file_name)
    with open(file_name) as f:
        data = f.read()
        data = data.split("\n")
    print(len(data))
    #[s] count R1R1R2R2 density-density int
    cnt_max     = len(data)-6
    SiteI       = np.zeros([cnt_max], dtype=np.int64)
    Param_Re    = np.zeros([cnt_max], dtype=np.float64)
    for cnt_i in range(5,len(data)-1):
        cnt = cnt_i -5
        if len(data[cnt_i]) > 0: # if data[i] is not empty
            tmp           = data[cnt_i].split()
            SiteI[cnt]    = int(tmp[0])
            Param_Re[cnt] = float(tmp[1])
    #[e] count R1R1R2R2 density-density
    #cnt_max = cnt
    return SiteI,Param_Re


def Trans(file_name):
    #[s] file name
    #[e] file name
    #print(file_name)
    with open(file_name) as f:
        data = f.read()
        data = data.split("\n")
    print(len(data))
    #[s] count R1R1R2R2 density-density int
    cnt_max     = len(data)-6
    SiteI       = np.zeros([cnt_max], dtype=np.int64)
    SpinI       = np.zeros([cnt_max], dtype=np.int64)
    SiteJ       = np.zeros([cnt_max], dtype=np.int64)
    SpinJ       = np.zeros([cnt_max], dtype=np.int64)
    Param_Re    = np.zeros([cnt_max], dtype=np.float64)
    Param_Im    = np.zeros([cnt_max], dtype=np.float64)
    for cnt_i in range(5,len(data)-1):
        cnt = cnt_i -5
        if len(data[cnt_i]) > 0: # if data[i] is not empty
            tmp           = data[cnt_i].split()
            SiteI[cnt]    = int(tmp[0])
            SpinI[cnt]    = int(tmp[1])
            SiteJ[cnt]    = int(tmp[2])
            SpinJ[cnt]    = int(tmp[3])
            Param_Re[cnt] = float(tmp[4])
            Param_Im[cnt] = float(tmp[5])
    #[e] count R1R1R2R2 density-density
    #cnt_max = cnt
    return SiteI,SpinI,SiteJ,SpinJ,Param_Re,Param_Im



if __name__ == "__main__":
    main()
