#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 11:57:00 2019

@author: user
"""
import cv2
import numpy as np
import heapq
from matplotlib.mlab import PCA

###################Image folder ##########################################
img_folder="/home/user/Documents/MTP/Images/AlphaNumericForProcessing/"

fnames=["IMG_20190925_184055", "IMG_20190831_152814", "IMG_20190831_152903", "IMG_20190831_152951",
        "IMG_20190831_153029", "IMG_20190831_153120", "IMG_20190831_172919", "IMG_20190831_173009",
        "IMG_20190831_153419", "IMG_20190831_153459", "IMG_20190831_173113","IMG_20190925_184037",
        "IMG_20190831_173229","IMG_20190831_173328"]

fnames_s=[["V7TrajectoryFilter_MatlabProcess_DiscreteDataset_Moto360G1_GYRO_GYRO_08312019_15_27_05_0WhiteBoardF","0"],
          ["V7TrajectoryFilter_MatlabProcess_DiscreteDataset_Moto360G1_GYRO_GYRO_08312019_15_27_55_1WhiteBoardF","1"],
          ["V7TrajectoryFilter_MatlabProcess_DiscreteDataset_Moto360G1_GYRO_GYRO_08312019_15_28_35_2WhiteBoardF","2"],
          ["V7TrajectoryFilter_MatlabProcess_DiscreteDataset_Moto360G1_GYRO_GYRO_08312019_15_29_30_3WhiteBoardF","3"],
          ["V7TrajectoryFilter_MatlabProcess_DiscreteDataset_Moto360G1_GYRO_GYRO_08312019_15_30_10_4WhiteBoardF","4"],
          ["V7TrajectoryFilter_MatlabProcess_DiscreteDataset_Moto360G1_GYRO_GYRO_08312019_15_31_00_5WhiteBoardF","5"],
          ["V7TrajectoryFilter_MatlabProcess_DiscreteDataset_Moto360G1_GYRO_GYRO_08312019_17_28_57_6WhiteBoardF","6"],
          ["V7TrajectoryFilter_MatlabProcess_DiscreteDataset_Moto360G1_GYRO_GYRO_08312019_17_29_47_7WhiteBoardF","7"],
          ["V7TrajectoryFilter_MatlabProcess_DiscreteDataset_Moto360G1_GYRO_GYRO_08312019_15_34_00_8WhiteBoardF","8"],
          ["V7TrajectoryFilter_MatlabProcess_DiscreteDataset_Moto360G1_GYRO_GYRO_08312019_15_34_40_9WhiteBoardF","9"],
          ["V7TrajectoryFilter_MatlabProcess_DiscreteDataset_Moto360G1_GYRO_GYRO_08312019_17_30_52_aWhiteBoardF","a"],
          ["V7TrajectoryFilter_MatlabProcess_DiscreteDataset_Moto360G1_GYRO_GYRO_08312019_17_31_37_bWhiteBoardF","b"],
          ["V7TrajectoryFilter_MatlabProcess_DiscreteDataset_Moto360G1_GYRO_GYRO_08312019_17_32_12_cWhiteBoardF","c"],
          ["V7TrajectoryFilter_MatlabProcess_DiscreteDataset_Moto360G1_GYRO_GYRO_08312019_17_33_12_dWhiteBoardF","d"]]


labels=["zero","one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
        "a","b","c","d"]
##########################################################################


#file_name=img_folder + "IMG_20190831_152951" + ".jpg"

def pca(X):
  n, m = X.shape
  assert np.allclose(X.mean(axis=0), np.zeros(m))
  C = np.dot(X.T, X) / (n-1)
  eigen_vals, eigen_vecs = np.linalg.eig(C)
  X_pca = np.dot(X, eigen_vecs)
  print (X_pca.shape)
  return X_pca


def draw_box(filename,outname):
    img_gray=cv2.imread(filename,0) #1 for color 0 for gray 
    mean, std = cv2.meanStdDev(img_gray)
    if (std>15.0):
        thresh, img_bw = cv2.threshold(img_gray, 128, 255, cv2.THRESH_BINARY)
    else:
        thresh, img_bw = cv2.threshold(img_gray, 150, 255, cv2.THRESH_BINARY)
        
    i=0
    prev_count=0
    img_width=img_bw.shape[1]
    hline_start=hline_end=0
    max_hline_start=max_hline_end=0
    diff=0
    state=0 # start line found
    
    #print (img_bw.shape)

    for row in img_bw:
        current_count=np.count_nonzero(row)
        #print (current_count)
        if (current_count!=img_width and prev_count==img_width and state==0):
            hline_start=i
            state=1 
            #print ("came here 1", i)
    
        if (current_count==img_width and prev_count==img_width and (i-hline_start)>10 and state==1):
            hline_end=i-1
            state=0
            #print ("came here 2", i)

            if ((hline_end-hline_start)>diff):
                diff=(hline_end-hline_start)
                max_hline_start=hline_start
                max_hline_end=hline_end
                
        
        prev_count=current_count
        i+=1
    
    new_arr=img_bw[max_hline_start:max_hline_end+1,:].T
    img_width=new_arr.shape[1]
    #print (new_arr.shape)
    state=0
    i=-1
    top=bottom=0
    min_height=20
    max_gap=10
    for row in new_arr:
        i+=1
        current_count = np.count_nonzero(row)
        if (state==0 and current_count!=img_width):
            state=1
            top=i
            blnk_count=0
            #print ("count rxd", current_count, top, i)
            continue
        
        if (state==1 and current_count==img_width):
            blnk_count+=1
            if (blnk_count>max_gap):
                #print ("resting to state 0 count rxd", current_count, top, i, blnk_count, max_gap)
                state=0
                top=0;
                continue
        
        if (state==1 and current_count==img_width and blnk_count<max_gap):
            bottom=i-1
            if ((bottom-top)<min_height):
                bottom=0
                state=1
            else:
                state=2
                blnk_count=0
            continue    
            
        
        if (state==2):
            if (current_count==img_width):
                blnk_count+=1
                if (blnk_count>max_gap):
                    state=3
            else:
                state=2;
                bottom=i-1
                
        if (state==3):
            break
    
    #print (new_arr.shape, top, bottom)
    #print (max_hline_start, max_hline_end)
    new_arr=new_arr[top:bottom+1,:].T
    newimg = cv2.resize(new_arr,(128,128))
    oname="img_bw_"+outname+".png"
    cv2.imwrite(oname, newimg)
    print ("image created for "+ outname)


def Nmaxelements(list1, N): 
    final_list = [] 
    idx_list=[]
    for i in range(0, N):  
        max1 = 0
          
        for j in range(len(list1)):
            if (j in idx_list):
                continue;
            if abs(list1[j].real) > max1: 
                max1 = (list1[j].real); 
                idx_list.append(j)
                  
        final_list.append(max1) 
          
    return (final_list) 

def euclidian_distance(list1, list2):
    """Distance between two vectors."""
    squares = [(p-q) ** 2 for p, q in zip(list1, list2)]
    return sum(squares) ** .5

'''   
for idx in range(0, 14):
    print ("index " + str(idx))
    fname=img_folder + fnames[idx] + ".jpg"
    draw_box(fname,labels[idx])
'''    
for el1 in labels:
    oname="img_bw_"+el1+".png"
    img1=cv2.imread(oname,0) 
    eigenvalues1, eigenvectors1 = np.linalg.eig(img1)
    max3_of_eigen1= Nmaxelements(eigenvalues1,3)
    print (max3_of_eigen1)
    #max3_of_eigen1= heapq.nlargest(3, eigenvalues1, key=abs)
    #max3_of_eigen1= heapq.nlargest(3, eigenvalues1, key=abs)
    #print ("max of eign1" + str(max3_of_eigen1))
    for el2 in fnames_s:
        fn=img_folder + el2[0] + ".png"
        img2=cv2.imread(fn,0)  
        eigenvalues2, eigenvectors2 = np.linalg.eig(img2)
        max3_of_eigen2= Nmaxelements(eigenvalues2,3)
        #print ("max of eign2" + str(max3_of_eigen2))
        #print (max3_of_eigen2)
        diff = euclidian_distance(max3_of_eigen1, max3_of_eigen2) 
        print ("diff(" + el1 +"," + el2[1] + ") " +str(diff))
