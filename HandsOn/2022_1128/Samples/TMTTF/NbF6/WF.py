from __future__ import print_function
import numpy as np
import math
import cmath
import lattice

def Jast(list_org,list_sub,Full_Orb): 
    All_N      = list_org[0]*list_org[1]*list_org[2]*list_org[3]
    Lx         = list_org[0]
    Ly         = list_org[1]
    orb_num    = list_org[3]
    #
    sub_x      = list_sub[0]
    sub_y      = list_sub[1]
    tot_APorb  = sub_x*sub_y*orb_num*All_N 
    tot_Jast   = sub_x*sub_y*orb_num*All_N 
    Full_Jast  = np.full([All_N,All_N],-100,dtype=np.int)
    Check_Jast = np.full([tot_APorb],-100,dtype=np.int)
    Trans_Jast = np.full([tot_APorb],-100,dtype=np.int)
    #
    Inv_Jast_I = np.full([tot_APorb,All_N],-100,dtype=np.int)
    Inv_Jast_J = np.full([tot_APorb,All_N],-100,dtype=np.int)
    Inv_cnt    = np.full([tot_APorb],0,dtype=np.int)

    for all_i in range(0,All_N):
        for all_j in range(0,All_N):
            Full_Jast[all_i][all_j] = Full_Orb[all_i][all_j]
    #[s] Symmetrize
    for cnt_APorb in range(0,tot_APorb):
        for all_i in range(0,All_N):
            for all_j in range(0,All_N):
                if (Full_Jast[all_i][all_j]==cnt_APorb):
                    Full_Jast[all_j][all_i] = Full_Jast[all_i][all_j]
    #[e] Symmetrize
    cnt_Jast = 0
    for all_i in range(0,All_N):
        for all_j in range(all_i+1,All_N):
            tmp_cnt = Full_Jast[all_i][all_j]
            if(Check_Jast[tmp_cnt]<0):
                Trans_Jast[tmp_cnt]      = cnt_Jast
                Full_Jast[all_i][all_j]  = cnt_Jast
                Full_Jast[all_j][all_i]  = cnt_Jast
                Inv_Jast_I[cnt_Jast][Inv_cnt[cnt_Jast]]     = all_i
                Inv_Jast_J[cnt_Jast][Inv_cnt[cnt_Jast]]     = all_j
                Inv_cnt[cnt_Jast]       += 1
                cnt_Jast                += 1
                Check_Jast[tmp_cnt]      = 1
            else:
                Full_Jast[all_i][all_j]         = Trans_Jast[tmp_cnt]
                Full_Jast[all_j][all_i]         = Trans_Jast[tmp_cnt]
                Inv_Jast_I[Trans_Jast[tmp_cnt]][Inv_cnt[Trans_Jast[tmp_cnt]]] = all_i
                Inv_Jast_J[Trans_Jast[tmp_cnt]][Inv_cnt[Trans_Jast[tmp_cnt]]] = all_j
                Inv_cnt[Trans_Jast[tmp_cnt]]   += 1
    #
    tot_Jast = cnt_Jast
    #
    with open("Jast.def", 'w') as f:
        print("==================", file=f)
        print("NOrbital  %d "%(tot_Jast), file=f)
        print("Complex    0 ", file=f)
        print("==================", file=f)
        print("==================", file=f)
        for all_i in range(0,All_N):
            for all_j in range(all_i+1,All_N):
                print(" %3d %3d %3d"% (all_i,all_j,Full_Jast[all_i][all_j]), file=f)
                print(" %3d %3d %3d"% (all_j,all_i,Full_Jast[all_j][all_i]), file=f)
        for all_i in range(0,tot_Jast):
            print(" %3d %3d "% (all_i,1), file=f)

    with open("Check_Jast.def", 'w') as f:
        for cnt_Jast in range(0,tot_Jast):
            max_cnt = Inv_cnt[cnt_Jast]
            print("cnt=%3d,%3d equiv. pairs: " % (cnt_Jast,max_cnt),end="", file=f)
            for tmp_cnt in range(0,max_cnt):
                all_i = Inv_Jast_I[cnt_Jast][tmp_cnt]
                all_j = Inv_Jast_J[cnt_Jast][tmp_cnt]
                print(" %3d=(%3d,%3d)  " % (tmp_cnt,all_i,all_j),end="", file=f)
            print("", file=f)

def APOrbital(list_org,list_sub): 
    All_N     = list_org[0]*list_org[1]*list_org[2]*list_org[3]
    Lx        = list_org[0]
    Ly        = list_org[1]
    orb_num   = list_org[3]
    #
    sub_x     = list_sub[0]
    sub_y     = list_sub[1]
    tot_APorb = sub_x*sub_y*orb_num*All_N 
    Full_Orb  = np.full([All_N,All_N],-100,dtype=np.int)
    Inv_Orb_I = np.full([tot_APorb,All_N],-100,dtype=np.int)
    Inv_Orb_J = np.full([tot_APorb,All_N],-100,dtype=np.int)
    Inv_cnt   = np.full([tot_APorb],0,dtype=np.int)

    with open("APOrbital.def", 'w') as f:
        print("==================", file=f)
        print("NOrbital  %d "%(tot_APorb), file=f)
        print("Complex    0 ", file=f)
        print("==================", file=f)
        print("==================", file=f)
        for all_i in range(0,All_N):
            list_site_i = lattice.func_site(all_i,list_org)
            x_i         = list_site_i[0]      
            y_i         = list_site_i[1]      
            sub_x_i     = x_i%sub_x
            sub_y_i     = y_i%sub_y
            orb_i       = list_site_i[3]
            tmp_i       = orb_i + orb_num*(sub_x_i+sub_y_i*sub_x)
            for tmp_j in range(0,All_N):
                list_site_j = lattice.func_site(tmp_j,list_org)
                vec_x       = list_site_j[0] 
                vec_y       = list_site_j[1] 
                x_j         = (x_i+vec_x)%Lx
                y_j         = (y_i+vec_y)%Ly
                site_j      = x_j+y_j*Lx
                orb_j       = list_site_j[3] 
                all_j       = orb_j + orb_num*site_j
                cnt_APorb   = tmp_j + tmp_i*All_N
                Full_Orb[all_i][all_j] = cnt_APorb 
                Inv_Orb_I[cnt_APorb][Inv_cnt[cnt_APorb]] = all_i
                Inv_Orb_J[cnt_APorb][Inv_cnt[cnt_APorb]] = all_j
                Inv_cnt[cnt_APorb] += 1
                print(" %3d %3d  %3d"% (all_i,all_j,cnt_APorb), file=f)
        for all_i in range(0,tot_APorb):
            print(" %3d %3d "% (all_i,1), file=f)

    with open("Check_APOrbital.def", 'w') as f:
        for cnt_APorb in range(0,tot_APorb):
            max_cnt = Inv_cnt[cnt_APorb]
            print("cnt=%3d,%3d equiv. pairs: " % (cnt_APorb,max_cnt),end="", file=f)
            for tmp_cnt in range(0,max_cnt):
                all_i = Inv_Orb_I[cnt_APorb][tmp_cnt]
                all_j = Inv_Orb_J[cnt_APorb][tmp_cnt]
                print(" %3d=(%3d,%3d)  " % (tmp_cnt,all_i,all_j),end="", file=f)
            print("", file=f)

    return Full_Orb

def Gutz(list_org,list_sub): 
    All_N    = list_org[0]*list_org[1]*list_org[2]*list_org[3]
    orb_num  = list_org[3]
    sub_x    = list_sub[0]
    sub_y    = list_sub[1]
    tot_Gutz = sub_x*sub_y*orb_num

    with open("Gutz.def", 'w') as f:
        print("==================", file=f)
        print("NGutz    %3d "%(tot_Gutz), file=f)
        print("Complex   0 ", file=f)
        print("==================", file=f)
        print("==================", file=f)
        for all_i in range(0,All_N):
            list_site = lattice.func_site(all_i,list_org)
            sub_x_i   = list_site[0]%sub_x
            sub_y_i   = list_site[1]%sub_y
            num_gutz  = list_site[3]+orb_num*(sub_x_i+sub_y_i*sub_x)
            print(" %3d %3d "% (all_i,num_gutz), file=f)
        for all_i in range(0,tot_Gutz):
            print(" %3d %3d "% (all_i,1), file=f)
