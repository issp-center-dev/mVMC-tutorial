from __future__ import print_function
import numpy as np
import math
import cmath

def geom(file_name,orb_num):
    lat_vec = np.zeros([3,3], dtype=np.float)
    orb_vec = np.zeros([orb_num,3], dtype=np.float)
    with open(file_name) as f:
        data = f.read()
        data = data.split("\n")
    cnt = 0
    for cnt_i in range(0,len(data)-1):
        if cnt_i <  3: # if data[i] is not empty
            tmp          = data[cnt_i].split()
            lat_vec[cnt_i][0] = float(tmp[0]) 
            lat_vec[cnt_i][1] = float(tmp[1]) 
            lat_vec[cnt_i][2] = float(tmp[2]) 
        if cnt_i == 3: # if data[i] is not empty
            tmp = data[cnt_i].split()
            tmp_num = int(tmp[0])
            print("read orb is ",tmp_num)
            if tmp_num != orb_num:
                print("fatal error in orb_num")
        if cnt_i > 3 : # if data[i] is not empty
            tmp_i = cnt_i - 4
            tmp          = data[cnt_i].split()
            orb_vec[tmp_i][0] = float(tmp[0])
            orb_vec[tmp_i][1] = float(tmp[1])
            orb_vec[tmp_i][2] = float(tmp[2])
    return lat_vec,orb_vec


def count(file_name):
    #[s] file name
    #[e] file name
    #print(file_name)
    with open(file_name) as f:
        data = f.read()
        data = data.split("\n")
        #print(len(data))
    #[s] count R1R1R2R2 density-density int
    cnt = 0
    for cnt_i in range(0,len(data)):
        if len(data[cnt_i]) > 0: # if data[i] is not empty
            tmp = data[cnt_i].split()
            #print(tmp,len(tmp))
            if len(tmp)==7 and cnt_i>0 : # if data[i] is not empty
                cnt += 1
    #[e] count R1R1R2R2 density-density int
    cnt_max = cnt
    #print(cnt_max)
    return cnt_max

def readHam(file_name,R1,R2,V):
    #print(file_name)
    with open(file_name) as f:
        data = f.read()
        data = data.split("\n")
        #print(len(data))
    # [s] count not empty elements
    cnt = 0
    for cnt_i in range(0, len(data)):
        if len(data[cnt_i]) > 0:  # if data[i] is not empty
            tmp = data[cnt_i].split()
            if len(tmp)==7 and cnt_i>0 : # if data[i] is not empty
                R1[cnt][0] = 0
                R1[cnt][1] = 0
                R1[cnt][2] = 0
                #
                R2[cnt][0] = float(tmp[0])
                R2[cnt][1] = float(tmp[1])
                R2[cnt][2] = float(tmp[2])
                # 
                R1[cnt][3] = float(tmp[3])
                R2[cnt][3] = float(tmp[4])
                V[cnt]     = float(tmp[5])
                cnt += 1
        # [e] count not empty elements
        # print(cnt_max)
