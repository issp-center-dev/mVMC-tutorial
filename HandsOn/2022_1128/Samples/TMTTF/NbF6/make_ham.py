from __future__ import print_function
import numpy as np
import math
import cmath
import lattice        #using read.py#

def make_trHam(R1,R2,V,shift_x,shift_y,shift_z,lat_vec,orb_vec,cnt_max,list_org,wannier_center):
    Lx       = list_org[0]
    Ly       = list_org[1]
    orb_num  = list_org[3]
    tr_Trans = np.full([shift_x*2+1,shift_y*2+1,shift_z*2+1,orb_num,orb_num],-100,dtype=np.float)
    tr_dis   = np.full([shift_x*2+1,shift_y*2+1,shift_z*2+1,orb_num,orb_num],-100,dtype=np.float)
    cnt_cut  = 0
    diff_eps = 1e-10
    for cnt in range(0, cnt_max):
        if (abs(R1[cnt][2]) < 0.0001) and (abs(R2[cnt][2]) < 0.0001):  # for 2D
            if (abs(R2[cnt][0])<=Lx/2) and (abs(R2[cnt][1])<=Ly/2) :  # for 2D only, Rx <= Lx/2 Ry <= Ly/2
                orb1   = int(R1[cnt][3]-1) # -1 for RESPACK
                orb2   = int(R2[cnt][3]-1) # -1 for RESPACK
                R1_x   = wannier_center[orb1][0]
                R1_y   = wannier_center[orb1][1]
                R1_z   = wannier_center[orb1][2]
                R2_x   = wannier_center[orb2][0]
                R2_y   = wannier_center[orb2][1]
                R2_z   = wannier_center[orb2][2]
                for cord in range(3):
                    R1_x   += R1[cnt][cord]*lat_vec[cord][0]
                    R1_y   += R1[cnt][cord]*lat_vec[cord][1]
                    R1_z   += R1[cnt][cord]*lat_vec[cord][2]
                    R2_x   += R2[cnt][cord]*lat_vec[cord][0]
                    R2_y   += R2[cnt][cord]*lat_vec[cord][1]
                    R2_z   += R2[cnt][cord]*lat_vec[cord][2]
                    #print(abs(R2[0][cnt]),Lx/2,R2[1][cnt],Ly/2)
                diff_x = int(R2[cnt][0]-R1[cnt][0]+shift_x)
                diff_y = int(R2[cnt][1]-R1[cnt][1]+shift_y)
                diff_z = int(R2[cnt][2]-R1[cnt][2]+shift_z)
                dis    = (R2_x-R1_x)**2+(R2_y-R1_y)**2+(R2_z-R1_z)**2
                dis    = math.sqrt(dis)
                tr_Trans[diff_x][diff_y][diff_z][orb1][orb2]   = V[cnt]
                tr_dis[diff_x][diff_y][diff_z][orb1][orb2] = dis
    return tr_Trans,tr_dis

def make_Ham(tr_param,tr_dis,vec_x,vec_y,vec_z,max_vec,shift_x,shift_y,shift_z,list_org,max_dis,max_vec_x,max_vec_y):
    list_trans = [0, 0, 0, 0]  # x,y,z,orb
    Lx         = list_org[0]
    Ly         = list_org[1]
    All_N      = list_org[0]*list_org[1]*list_org[2]*list_org[3]
    orb_num    = list_org[3]
    all_param  = np.full([All_N,All_N],-100,dtype=np.float)
    all_dis    = np.full([All_N,All_N],-100,dtype=np.float)
    diff_eps   = 1e-8
    cut_cnt    = 0
    for all_i in range(All_N):
        list_site = lattice.func_site(all_i, list_org)
        orb_i = list_site[3]
        for cnt_vec in range(max_vec):
            list_trans[0] = vec_x[cnt_vec]
            list_trans[1] = vec_y[cnt_vec]
            list_trans[2] = vec_z[cnt_vec]
            tr_x = int(vec_x[cnt_vec]+shift_x)
            tr_y = int(vec_y[cnt_vec]+shift_y)
            if vec_z[cnt_vec] == 0 and abs(vec_x[cnt_vec])<=max_vec_x and abs(vec_y[cnt_vec])<=max_vec_y: # for 2D
                tr_z = int(vec_z[cnt_vec]+shift_z)
                for orb_j in range(0,orb_num):
                    list_trans[3] = orb_j
                    all_j     = lattice.func_strans_2D(list_trans, list_site, list_org)
                    tmp_param = tr_param[tr_x][tr_y][tr_z][orb_i][orb_j]
                    tmp_dis   = tr_dis[tr_x][tr_y][tr_z][orb_i][orb_j]
                    if tmp_dis < max_dis+1e-8:
                        if all_param[all_i][all_j] < -100+1e-8:
                            all_param[all_i][all_j] = tmp_param
                            all_dis[all_i][all_j]   = tmp_dis
                        else:
                            print("double count exists !",all_i,all_j,all_param[all_i][all_j],vec_x[cnt_vec],vec_y[cnt_vec],orb_i,orb_j,tmp_param,tmp_dis)
    return all_param,all_dis
