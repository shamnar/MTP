#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 11:57:00 2019

@author: user
"""
import cv2
import numpy as np
import math
import sys
from os import listdir
from os.path import isfile, join
###################Image folder ##########################################
folder_settings=[
["/Users/shamnarpgmail.com/Downloads/ExperimentData/proj/img/MathData/stylusData",
"/Users/shamnarpgmail.com/Downloads/ExperimentData/proj/img/MathData/MyMathData",
"/Users/shamnarpgmail.com/Downloads/ExperimentData/proj/python/MTP/Pyhton/outfilesMath"],

["/Users/shamnarpgmail.com/Downloads/ExperimentData/proj/img/BenData/stylusData",
"/Users/shamnarpgmail.com/Downloads/ExperimentData/proj/img/BenData/MyBenData",
"/Users/shamnarpgmail.com/Downloads/ExperimentData/proj/python/MTP/Pyhton/outfilesBen"],

["/Users/shamnarpgmail.com/Downloads/ExperimentData/proj/img/EnData/StylusData",
"/Users/shamnarpgmail.com/Downloads/ExperimentData/proj/img/EnData/trajectory",
"/Users/shamnarpgmail.com/Downloads/ExperimentData/proj/python/MTP/Pyhton/outfilesEn"]
]

image_sizes_dict= dict([(5,125),(4,128),(3,129),(10,150),(15,150),(20,160),(30,150),(40,160),(50,150),(75,150)])
##########################################################################

def has_image(arr, grid_size):
    if (np.count_nonzero(arr))==(grid_size*grid_size):
        return 0
    else:
        return 1

def generate_matrix(img_array, window_size):
    [row, col] = img_array.shape
    msize = row//window_size
    matrix = np.zeros((msize,msize))
    i=j=0
    c_index=r_index=0
    while(i<row):
        while(j<col):
            window=img_array[i:i+window_size,j:j+window_size]
            val=has_image(window, window_size)
            matrix[r_index, c_index] = val
            c_index+=1
            j+=window_size
        r_index+=1
        i+=window_size
    return(matrix)


def draw_box(img_name):
    img_bw=img_name
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

    new_arr=new_arr[top:bottom+1,:].T
    return (new_arr)

def process_images(image1, image2, img_size, win_size):
    img1=cv2.imread(image1,0)
    img2=cv2.imread(image2,0)

    if (img1 is not None):
        success=True
    else:
        success=False

    if (not success):
        print ("Image reading Error..1")
        sys.exit()

    if (img2 is not None):
        success=True
    else:
        success=False

    if (not success):
        print ("Image reading Error..2")
        sys.exit()

    processed_img1=draw_box(img1)
    processed_img1 = cv2.resize(processed_img1,(img_size,img_size))
    thresh, processed_img1 = cv2.threshold(processed_img1, 150, 255, cv2.THRESH_BINARY)

    processed_img2=draw_box(img2)
    processed_img2 = cv2.resize(processed_img2,(img_size,img_size))
    thresh, processed_img2 = cv2.threshold(processed_img2, 150, 255, cv2.THRESH_BINARY)

    m1 = generate_matrix(processed_img1, win_size)
    m2 = generate_matrix(processed_img2, win_size)
    dist = np.linalg.norm(m1-m2)
    return (dist)

current_window_sizes=[10,15,20,30,40,50,75]
current_lang=2
for sizes in current_window_sizes:
    g_img_size=image_sizes_dict[sizes]
    output_folder=folder_settings[current_lang][2]
    output_file=output_folder+"/win"+str(sizes)+".csv"
    input_folder1=folder_settings[current_lang][0]
    input_folder2=folder_settings[current_lang][1]
    file_to_write = open(output_file, 'w') 
    count=0
    onlyfiles = [f for f in listdir(input_folder1) if isfile(join(input_folder1, f)) and f.endswith(".png")]
    for el in onlyfiles:
        start_str= el.split("_")
        end_str = start_str[1].split(".")
        substr=start_str[0]+"To"+end_str[0]+"F.png"
        matching_files = [f for f in listdir(input_folder2) if isfile(join(input_folder2, f)) and f.endswith(substr)]
        if (len(matching_files)>0):
            count+=1
            filename1=input_folder1+"/"+el
            filename2=input_folder2+"/"+matching_files[0]
            diffval=process_images(filename1, filename2, g_img_size, sizes)
            str_combined=el+","+matching_files[0]+","+str(diffval)
            print(str_combined, file = file_to_write)
            print(count,diffval)
#print (count)
    file_to_write.close() 





        


        
        

