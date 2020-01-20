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
from os import path
###################Image folder ##########################################
stylus_data_common="/home/user/Documents/MTP/Images/1FreeFormResults/StylusDatas"
traj_common="/home/user/Documents/MTP/Images/1FreeFormResults"
methods=["MultiUserProcess","MultiUserProcess_GyroPen","MultiUserProcess_NaiveBaseline"]
types=["MyBenData","MyData","MyMathBenData","MyMathEngData"]
users=["u00","u01","u02","u03","u04","u05","u06","u07","u08","u09"]
out_common="/home/user/Documents/MTP/Images/1FreeFormResults/Output"
'''
folder_settings=[
["/Users/shamnarpgmail.com/Downloads/ExperimentData/proj/img/MathData/stylusData",
"/Users/shamnarpgmail.com/Downloads/ExperimentData/proj/img/MathData/MyMathData",
"/Users/shamnarpgmail.com/Downloads/ExperimentData/proj/python/MTP/Pyhton/outfilesMath",
"MATH"],

["/Users/shamnarpgmail.com/Downloads/ExperimentData/proj/img/BenData/stylusData",
"/Users/shamnarpgmail.com/Downloads/ExperimentData/proj/img/BenData/MyBenData",
"/Users/shamnarpgmail.com/Downloads/ExperimentData/proj/python/MTP/Pyhton/outfilesBen",
"BEN"],

["/Users/shamnarpgmail.com/Downloads/ExperimentData/proj/img/EnData/StylusData",
"/Users/shamnarpgmail.com/Downloads/ExperimentData/proj/img/EnData/trajectory",
"/Users/shamnarpgmail.com/Downloads/ExperimentData/proj/python/MTP/Pyhton/outfilesEn",
"EN"],

[
"/Users/shamnarpgmail.com/Downloads/ExperimentData/proj/img/EnData/test/StylusData",
"/Users/shamnarpgmail.com/Downloads/ExperimentData/proj/img/EnData/test/TrajectoryData",
"/Users/shamnarpgmail.com/Downloads/ExperimentData/proj/img/EnData/test",
"TEST"
]
]
'''

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
    c_index=0
    r_index=0
    while(i<row):
        c_index=0
        j=0
        while(j<col):
            window=img_array[i:i+window_size,j:j+window_size]
            val=has_image(window, window_size)
            matrix[r_index, c_index] = val
            c_index+=1
            j+=window_size
        r_index=r_index+1
        i+=window_size
    return(matrix)

def get_boundaries(image):
    start=end=0
    w,h = image.shape
    for i in range(w):
        row=image[i]
        if (np.count_nonzero(row)!=h):
            start=i;
            break;
        
    for j in range(w-1, start, -1):
        row=image[j]
        if (np.count_nonzero(row)!=h):
            end=j
            break;
            
    return [start, end]    

def draw_box(image_name):
    top,bottom=get_boundaries(image_name)
    left,right=get_boundaries(image_name.T)
    cropped = image_name[top: bottom, left: right]
    return (cropped)


def draw_box_old(img_name):
    img_bw=img_name
    i=0
    prev_count=0
    img_width=img_bw.shape[1]
    hline_start=hline_end=0
    max_hline_start=max_hline_end=0
    diff=0
    state=0 # start line found
    
    for row in img_bw:
        current_count=np.count_nonzero(row)
        if (current_count!=img_width and prev_count==img_width and state==0):
            hline_start=i
            state=1 
    
        if (current_count==img_width and prev_count==img_width and (i-hline_start)>10 and state==1):
            hline_end=i-1
            state=0

            if ((hline_end-hline_start)>diff):
                diff=(hline_end-hline_start)
                max_hline_start=hline_start
                max_hline_end=hline_end
                
        
        prev_count=current_count
        i+=1
    
    new_arr=img_bw[max_hline_start:max_hline_end+1,:].T
    img_width=new_arr.shape[1]

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
            continue
        
        if (state==1 and current_count==img_width):
            blnk_count+=1
            if (blnk_count>max_gap):
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

def process_images1(image1, image2, img_size, win_size):
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
    thresh, processed_img1 = cv2.threshold(processed_img1, 200, 255, cv2.THRESH_BINARY)[1]

    processed_img2=draw_box(img2)
    processed_img2 = cv2.resize(processed_img2,(img_size,img_size))
    thresh, processed_img2 = cv2.threshold(processed_img2, 127, 255, cv2.THRESH_BINARY)[1]

    m1 = generate_matrix(processed_img1, win_size)
    m2 = generate_matrix(processed_img2, win_size)
    dist = np.linalg.norm(m1-m2)
    return (dist)

def draw_grids(image, grid_size, filename):
    [row,col]=image.shape
    points=list()
    for i in range(0,row,grid_size):
        points.append([0,i,row,i])
        points.append([i,0,i,row])
    for el in points:
        image = cv2.line(image, (el[0],el[1]), (el[2],el[3]), (100,0,0), 1)
    oimg_name=filename + "_"+str(grid_size)+".png"
    cv2.imwrite(oimg_name, image)
    
def get_only_filename(filename):
    f=filename.split("/")
    f1=f[len(f)-1]
    return (f1[:-4])

def process_images(image1, image2, diff_type):
    print_flag=False
    diff_list=[]
    win_sizes=[3,4,5,7,10,15,20,30,40,50]
    print_windows=[3,5,7,10,15,20,30,40,50]
    img_sizes_dict= dict([(3,129),(4,128),(5,125),(7,126),(10,150),(15,150),(20,160),(30,150),(40,160),(50,150),(75,150)])
    img1=cv2.imread(image1,cv2.IMREAD_UNCHANGED)
    img2=cv2.imread(image2,0)
    *_,alpha=cv2.split(img1)
    img1=cv2.bitwise_not(alpha)
    nzcount=np.count_nonzero(img1)
    if (nzcount==0):
        print ("errr img1")
        sys.exit()
        return (diff_list)
    
    if (np.count_nonzero(img2)==0):
        print ("errr img1")
        sys.exit()
        return (diff_list)
    

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
        #print (image2)
        #print (image1)
        #return diff_list
        sys.exit()
    for size in win_sizes:
        img_size = img_sizes_dict[size]
        processed_img1=draw_box(img1)
        processed_img1 = cv2.resize(processed_img1,(img_size,img_size))
        thresh, processed_img1 = cv2.threshold(processed_img1, 127, 255, cv2.THRESH_BINARY)

        processed_img2=draw_box(img2)
        w,h=processed_img2.shape
        if (w == 0 and h==0):
            return (diff_list)
        else:
            processed_img2 = cv2.resize(processed_img2,(img_size,img_size))
        thresh, processed_img2 = cv2.threshold(processed_img2, 127, 255, cv2.THRESH_BINARY)
        m1 = generate_matrix(processed_img1, size)
        m2 = generate_matrix(processed_img2, size)
                       
        if (diff_type==0): #euclidian dist
            dist = np.linalg.norm(m1-m2)
        elif (diff_type==1):
            dist = np.count_nonzero(m1!=m2)
        diff_list.append(dist)
        
        if (print_flag):        
            extracted_filename1 = get_only_filename(image1)
            extracted_filename2 = get_only_filename(image2)
            outf1="/home/user/Documents/MTP/Images/1FreeFormResults/Output/GridImages/"
            outf2="/home/user/Documents/MTP/Images/1FreeFormResults/Output/GridImages/"
            extracted_filename1 = outf1 + extracted_filename1
            extracted_filename2 = outf2 + extracted_filename2
            if (size in print_windows):
                draw_grids(processed_img1, size, extracted_filename1)
                draw_grids(processed_img2, size, extracted_filename2)
            
    return (diff_list)



for u in range(10):
    user_index = u
    for p in range(3):
        process_index=p
        input_folder = stylus_data_common + "/" + users[user_index]
        input_folder1 = traj_common + "/" + methods[process_index]+"/"+users[user_index]+"/"+types[0]
        input_folder2 = traj_common + "/" + methods[process_index]+"/"+users[user_index]+"/"+types[1]
        input_folder3 = traj_common + "/" + methods[process_index]+"/"+users[user_index]+"/"+types[2]
        input_folder4 = traj_common + "/" + methods[process_index]+"/"+users[user_index]+"/"+types[3]
        output_file = out_common + "/" + methods[process_index] + "/"+users[user_index] + ".csv"
        file_to_write = open(output_file, 'w') 
        count=0
    
        onlyfiles = [f for f in listdir(input_folder) if isfile(join(input_folder, f)) and f.endswith(".png")]
        for el in onlyfiles:
            start_str= el.split("_")
            end_str = start_str[1].split(".")
            if (process_index==0):
                substr=start_str[0]+"To"+end_str[0]+"F.png"
            else:
                substr=start_str[0]+"To"+end_str[0]+".png"
            matching_files1=[]
            matching_files2=[]
            matching_files3=[]
            matching_files4=[]
            if (path.exists(input_folder1)):
                matching_files1 = [f for f in listdir(input_folder1) if isfile(join(input_folder1, f)) and f.endswith(substr)]
            if (path.exists(input_folder2)):
                matching_files2 = [f for f in listdir(input_folder2) if isfile(join(input_folder2, f)) and f.endswith(substr)]
            if (path.exists(input_folder3)):
                matching_files3 = [f for f in listdir(input_folder3) if isfile(join(input_folder3, f)) and f.endswith(substr)]
            if (path.exists(input_folder4)):
                matching_files4 = [f for f in listdir(input_folder4) if isfile(join(input_folder4, f)) and f.endswith(substr)]
            found=0
            
            el1=""
            if (len(matching_files1)>0):
                filename2=input_folder1+"/"+matching_files1[0]
                el1=matching_files1[0]
                found=1
            elif (len(matching_files2)>0):
                filename2=input_folder2+"/"+matching_files2[0]
                el1=matching_files2[0]
                found=1
            elif (len(matching_files3)>0):
                filename2=input_folder3+"/"+matching_files3[0]
                el1=matching_files3[0]
                found=1
            elif (len(matching_files4)>0):
                filename2=input_folder4+"/"+matching_files4[0]
                el1=matching_files4[0]
                found=1
            
            if (found==1):
                count+=1
                filename1=input_folder+"/"+el
                difflist=process_images(filename1, filename2,1)        
                strlist= ', '.join(map(str,difflist))
                str_combined=el+","+el1+','+strlist
                print(str_combined, file = file_to_write)
                print(count, strlist)
                
        if (count==133):
            print ("Ok " + str(user_index) + "  " + str(process_index))
        else:
            print ("Not Ok" + str(user_index) + "  " + str(process_index))
        
        file_to_write.close() 



        


        
        

