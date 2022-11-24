import numpy as np
import math
import cmath
import toml
import sys
import make_ham    #using make_ham.py#
import read_ham    #using read_ham.py#
import Misc        #using Misc.py#
import WF          #using WF.py#

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
    AF_mag        = float(input_dict["param"]["AF_mag"])
    AF_Qx         = float(input_dict["param"]["AF_Qx"])
    AF_Qy         = float(input_dict["param"]["AF_Qy"])
    flag_PH       = input_dict["param"]["PH"]
    in_file_trans = input_dict["file"]["in_file_trans"]
    in_file_int   = input_dict["file"]["in_file_int"]
    in_file_geom  = input_dict["file"]["in_file_geom"]
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
    #list_site  = [0,0,0,0]  # x,y,z,orb
    if flag_PH == "no":
        Ncond = int(2*All_N*(3/4))
        name_trans = "trans.def"
    elif flag_PH == "yes":
        Ncond = int(2*All_N*(1/4))
        name_trans = "trans_PH.def"
    else:
        print("Fatal error: PH should be \"yes\" of \"no\" ")
        return 0
    #[e] initialize
    #[s] output misc files
    Misc.OutputMisc_Common(list_org)
    if method == "HPhi":  
        Misc.OutputMisc_HPhi(list_org,Ncond,name_trans)
    elif method == "mVMC":
        Misc.OutputMisc_mVMC(list_org,Ncond,name_trans)
        #[s] output WF
        WF.Gutz(list_org,list_sub)
        Full_Orb = WF.APOrbital(list_org,list_sub)
        WF.Jast(list_org,list_sub,Full_Orb)
        #[e] output WF 
    else:
        print("method should be specified !")
    #[e] output misc files

    # output Hamiltonian
    #[s] set orbital positions  
    lat_vec,orb_vec = read_ham.geom(in_file_geom,orb_num)
    print("lat vec",lat_vec)
    print("orb_vec",orb_vec)

    wannier_center   = np.zeros([orb_num,3], dtype=np.float64)
    for orb_i in range(orb_num):
        for int_i in range(3):
            wannier_center[orb_i][0] += lat_vec[int_i][0]*orb_vec[orb_i][int_i]           
            wannier_center[orb_i][1] += lat_vec[int_i][1]*orb_vec[orb_i][int_i]           
            wannier_center[orb_i][2] += lat_vec[int_i][2]*orb_vec[orb_i][int_i]           
    #print(wannier_center[0][0])
    #[e] set orbital positions  

    #[s] avoid negative index
    max_vec = (2*shift_x+1)*(2*shift_y+1)*(2*shift_z+1)
    vec_x   = np.zeros([max_vec], dtype=np.int64)
    vec_y   = np.zeros([max_vec], dtype=np.int64)
    vec_z   = np.zeros([max_vec], dtype=np.int64)
    tmp_cnt = 0
    for tmp_i in range(2*shift_x+1):
        for tmp_j in range(2*shift_y+1):
            for tmp_k in range(2*shift_z+1):
                vec_x[tmp_cnt]   = tmp_i-shift_x
                vec_y[tmp_cnt]   = tmp_j-shift_y
                vec_z[tmp_cnt]   = tmp_k-shift_z
                tmp_cnt         += 1
    #[e] avoid negative index

    tr_V,tr_V_dis = Make_AllV(in_file_int,list_org,lat_vec,orb_vec,shift_x,shift_y,shift_z,wannier_center)
    with open("check_dis.dat", 'w') as f:
        for tr_x in range(-2,3):
            for tr_y in range(-2,3):
                print("%d %d %d %d %.5f %.5f"  %(tr_x,tr_y,0,0,tr_V_dis[tr_x+shift_x][tr_y+shift_y][0+shift_z][0][0],tr_V[tr_x+shift_x][tr_y+shift_y][0+shift_z][0][0]),file=f) 
                print("%d %d %d %d %.5f %.5f"  %(tr_x,tr_y,0,1,tr_V_dis[tr_x+shift_x][tr_y+shift_y][0+shift_z][0][1],tr_V[tr_x+shift_x][tr_y+shift_y][0+shift_z][0][1]),file=f) 
                print("%d %d %d %d %.5f %.5f"  %(tr_x,tr_y,1,0,tr_V_dis[tr_x+shift_x][tr_y+shift_y][0+shift_z][1][0],tr_V[tr_x+shift_x][tr_y+shift_y][0+shift_z][1][0]),file=f) 
                print("%d %d %d %d %.5f %.5f"  %(tr_x,tr_y,1,1,tr_V_dis[tr_x+shift_x][tr_y+shift_y][0+shift_z][1][1],tr_V[tr_x+shift_x][tr_y+shift_y][0+shift_z][1][1]),file=f) 
    dis_3a  = tr_V_dis[1+shift_x][0+shift_y][0+shift_z][0][1]
    dis_3b  = tr_V_dis[1+shift_x][-1+shift_y][0+shift_z][0][1]
    dis_3c  = tr_V_dis[2+shift_x][0+shift_y][0+shift_z][1][0]
    dis_3d  = tr_V_dis[-2+shift_x][0+shift_y][0+shift_z][0][1]
    max_dis = max(dis_3a,dis_3b,dis_3c,dis_3d)
    print("max_dis",max_dis)
    print("3a",dis_3a,tr_V[1+shift_x][0+shift_y][0+shift_z][0][1])
    print("3b",dis_3b,tr_V[1+shift_x][-1+shift_y][0+shift_z][0][1])
    print("3c",dis_3c,tr_V[2+shift_x][0+shift_y][0+shift_z][1][0])
    print("3d",dis_3d,tr_V[-2+shift_x][0+shift_y][0+shift_z][0][1])
    #[s] set cut off
    #max_dis       = 10.76 #math.sqrt(1.0*2)
    max_vec_x     = 2
    max_vec_y     = 2
    #[e] set cut off

    all_V,all_V_dis = make_ham.make_Ham(tr_V,tr_V_dis,vec_x,vec_y,vec_z,max_vec,\
    shift_x,shift_y,shift_z,list_org,max_dis,max_vec_x,max_vec_y)
    #[s] mod V
    all_V   = ham_lambda*(all_V-ddf)
    Output_allV(all_V,all_V_dis,list_org,max_dis,orb_num)
    #[e] mod V

    tr_Trans,tr_Trans_dis = Make_AllTrans(in_file_trans,list_org,lat_vec,orb_vec,shift_x,shift_y,shift_z,wannier_center)
    all_Trans,all_Trans_dis = make_ham.make_Ham(tr_Trans,tr_Trans_dis,vec_x,vec_y,vec_z,max_vec,\
    shift_x,shift_y,shift_z,list_org,max_dis,max_vec_x,max_vec_y)

    #[s]symmetrized t_ij = t_ji
    All_N = list_org[0]*list_org[1]*list_org[2]*list_org[3]
    for all_i in range(All_N):
        for all_j in range(All_N):
            if (abs(all_Trans[all_i][all_j])<100):
                all_Trans[all_j][all_i]     = all_Trans[all_i][all_j]
                all_Trans_dis[all_j][all_i] = all_Trans_dis[all_i][all_j]
    #[e]symmetrized t_ij = t_ji
    
    #[s] set chemi = 0
    chemi      = np.zeros([orb_num], dtype=np.float64)
    org_chemi  = all_Trans[0][0]
    chemi[0]   = 0
    for orb_i in range(1,orb_num):
        chemi[orb_i] = all_Trans[orb_i][orb_i]-org_chemi
    #[e] set chemi = 0
    #[s] set AF
    AF =  np.zeros([All_N], dtype=np.float64)
    for all_i in range(All_N):
        orb_i  = all_i%orb_num
        site_i = int((all_i-orb_i)/orb_num)
        x_i    = site_i%Lx
        y_i    = int((site_i-x_i)/Lx)
        AF[all_i] = AF_mag*math.cos(math.pi*x_i*AF_Qx+math.pi*y_i*AF_Qy)
        #print(all_i,orb_i,x_i,y_i,AF[all_i])

    #[e] set AF
    Output_AllTrans(all_Trans,all_Trans_dis,list_org,max_dis,chemi,AF)
    #[s] for check
    Output_ForCheck(all_V,all_Trans,list_org)
    #[e] for check
 
def Make_AllV(in_file,list_org,lat_vec,orb_vec,shift_x,shift_y,shift_z,wannier_center):
    All_N   = list_org[0]*list_org[1]*list_org[2]*list_org[3]
    orb_num = list_org[3]
    cnt_max = read_ham.count(in_file)
    print("cnt_max (number of all interactions)",cnt_max) 
    #
    R1  = np.zeros([cnt_max,4], dtype=np.float64)
    R2  = np.zeros([cnt_max,4], dtype=np.float64)

    Vbare   = np.zeros([cnt_max], dtype=np.float64)
    V       = np.zeros([cnt_max], dtype=np.float64)
    #[s] read only V (density-density)
    read_ham.readHam(in_file,R1,R2,V)
    #[e] read only V (density-density)
    #[s] only 2D V
    tr_V,tr_dis = make_ham.make_trHam(R1,R2,V,shift_x,shift_y,shift_z,lat_vec,orb_vec,cnt_max,list_org,wannier_center)
    #[e] only 2D V

    return tr_V,tr_dis

def Output_ForCheck(all_V,all_Trans,list_org):
    Lx      = list_org[0]
    Ly      = list_org[1]
    Lz      = list_org[2]
    orb_num = list_org[3]
    with open("check_int.dat", 'w') as f:
        print("U",all_V[0][0],file=f)
        print("Va1",all_V[0][1],file=f)
        print("Va2",all_V[1][2],file=f)
        print("Vb",all_V[0][Lx*orb_num],file=f)
        print("Vq1",all_V[0][2*Lx*orb_num-1],file=f)
        print("Vq2",all_V[0][Lx*(Ly-1)*orb_num+1],file=f)
        print("Vp1",all_V[0][Lx*orb_num+1],file=f)
        print("Vp2",all_V[0][Lx*Ly*orb_num-1],file=f)
        if Lx > 2:
            print("V2a",all_V[0][2],file=f)
            print("V2a",all_V[1][3],file=f)

    with open("check_trans.dat", 'w') as f:
        print("chemi",all_Trans[0][0],file=f)
        print("ta1",all_Trans[0][1],file=f)
        print("ta2",all_Trans[1][2],file=f)
        print("tb",all_Trans[0][Lx*orb_num],file=f)
        print("tq1",all_Trans[0][2*Lx*orb_num-1],file=f)
        print("tq2",all_Trans[0][Lx*(Ly-1)*orb_num+1],file=f)
        print("tp1",all_Trans[0][Lx*orb_num+1],file=f)
        print("tp2",all_Trans[0][Lx*Ly*orb_num-1],file=f)
        if Lx > 2:
            print("t2a",all_Trans[0][2],file=f)
            print("t2a",all_Trans[1][3],file=f)
   
def Output_allV(all_V,all_dis,list_org,max_dis,orb_num):
    All_N        = list_org[0]*list_org[1]*list_org[2]*list_org[3]
    cnt_V = 0
    for all_i in range(All_N):
        for all_j in range(all_i + 1, All_N):
            if (all_V[all_i][all_j] > 0) & (all_dis[all_i][all_j]< max_dis+1e-8):
                cnt_V += 1
    #print(' cnt_V = ',cnt_V)
    with open("coulombinter.def", 'w') as f:
        print("====== ", file=f)
        print("%s %d " % ('N', cnt_V), file=f)
        print("====== ", file=f)
        print("====== ", file=f)
        print("====== ", file=f)
        for all_i in range(All_N):
            for all_j in range(all_i + 1,All_N):
                if (all_V[all_i][all_j] > 0) & (all_dis[all_i][all_j]< max_dis+1e-8):
                    print("%4d %4d %.3f " % (all_i,all_j,all_V[all_i][all_j]), file=f)
    #
    cnt_V = All_N
    with open("coulombintra.def", 'w') as f:
        print("====== ", file=f)
        print("%s %d " % ('N', cnt_V), file=f)
        print("====== ", file=f)
        print("====== ", file=f)
        print("====== ", file=f)
        for all_i in range(All_N):
            print("%4d %.3f " % (all_i,all_V[all_i][all_i]), file=f)
    #
def Make_AllTrans(in_file,list_org,lat_vec,orb_vec,shift_x,shift_y,shift_z,wannier_center):
    All_N      = list_org[0]*list_org[1]*list_org[2]*list_org[3]
    orb_num    = list_org[3]
    cnt_max    = read_ham.count(in_file)
    print("cnt_max (total transfers)",cnt_max)
    #
    R1  = np.zeros([cnt_max,4], dtype=np.float64)
    R2  = np.zeros([cnt_max,4], dtype=np.float64)
    #
    trans     = np.zeros([cnt_max], dtype=np.float64)
    all_Trans = np.full([All_N,All_N],-100,dtype=np.float64)
    all_dis   = np.full([All_N,All_N],-100,dtype=np.float64)

    read_ham.readHam(in_file,R1,R2,trans)
    tr_Trans,tr_dis = make_ham.make_trHam(R1,R2,trans,shift_x,shift_y,shift_z,lat_vec,orb_vec,cnt_max,list_org,wannier_center)

    return tr_Trans,tr_dis

def Output_AllTrans(all_Trans,all_dis,list_org,max_dis,chemi,AF):
    Lx         = list_org[0]
    orb_num    = list_org[3]
    All_N      = list_org[0]*list_org[1]*list_org[2]*list_org[3]
    cnt_V = 0
    for all_i in range(All_N):
        for all_j in range(all_i+1, All_N):
            if (all_Trans[all_j][all_i]> -100) and (all_dis[all_j][all_i]< max_dis+1e-8) and abs(all_Trans[all_j][all_i])>=1e-2:
                cnt_V += 1
    print('trans cnt_V = ',cnt_V)
    with open("trans.def", 'w') as f:
        print("====== ", file=f)
        print("%s %d " % ('N', cnt_V*4+2*All_N), file=f)
        print("====== ", file=f)
        print("====== ", file=f)
        print("====== ", file=f)
        for all_i in range(All_N):
            for all_j in range(all_i,All_N):
                if all_i == all_j:
                    orb_i   = all_i%orb_num
                    print("%4d 0 %4d 0 %.3f 0.0 " % (all_i,all_i,-chemi[orb_i]), file=f) # note: - for HPhi
                    print("%4d 1 %4d 1 %.3f 0.0 " % (all_i,all_i,-chemi[orb_i]), file=f) # note: - for HPhi
                elif (all_Trans[all_i][all_j]> -100) and (all_dis[all_i][all_j]< max_dis+1e-8) and abs(all_Trans[all_j][all_i])>=1e-2:
                    print("%4d 0 %4d 0 %.3f 0.0 " % (all_j,all_i,-all_Trans[all_j][all_i]), file=f) # note: - for HPhi
                    print("%4d 0 %4d 0 %.3f 0.0 " % (all_i,all_j,-all_Trans[all_j][all_i]), file=f) # note: - for HPhi
                    print("%4d 1 %4d 1 %.3f 0.0 " % (all_j,all_i,-all_Trans[all_j][all_i]), file=f) # note: - for HPhi
                    print("%4d 1 %4d 1 %.3f 0.0 " % (all_i,all_j,-all_Trans[all_j][all_i]), file=f) # note: - for HPhi

    with open("mag_trans.def", 'w') as f:
        print("====== ", file=f)
        print("%s %d " % ('N', cnt_V*4+2*All_N), file=f)
        print("====== ", file=f)
        print("====== ", file=f)
        print("====== ", file=f)
        for all_i in range(All_N):
            for all_j in range(all_i,All_N):
                if all_i == all_j:
                    orb_i   = all_i%orb_num
                    print("%4d 0 %4d 0 %.3f 0.0 " % (all_i,all_i,-chemi[orb_i]+AF[all_i]), file=f) # note: - for HPhi
                    print("%4d 1 %4d 1 %.3f 0.0 " % (all_i,all_i,-chemi[orb_i]-AF[all_i]), file=f) # note: - for HPhi
                elif (all_Trans[all_i][all_j]> -100) and (all_dis[all_i][all_j]< max_dis+1e-8) and abs(all_Trans[all_j][all_i])>=1e-2:
                    print("%4d 0 %4d 0 %.3f 0.0 " % (all_j,all_i,-all_Trans[all_j][all_i]), file=f) # note: - for HPhi
                    print("%4d 0 %4d 0 %.3f 0.0 " % (all_i,all_j,-all_Trans[all_j][all_i]), file=f) # note: - for HPhi
                    print("%4d 1 %4d 1 %.3f 0.0 " % (all_j,all_i,-all_Trans[all_j][all_i]), file=f) # note: - for HPhi
                    print("%4d 1 %4d 1 %.3f 0.0 " % (all_i,all_j,-all_Trans[all_j][all_i]), file=f) # note: - for HPhi




if __name__ == "__main__":
    main()
