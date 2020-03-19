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
stylus_data_common="/Users/shamnarpgmail.com/Downloads/ExperimentData/proj/img/EnData/StylusData"
traj_common="/Users/shamnarpgmail.com/Downloads/ExperimentData/FreeFormResults"
methods=["MultiUserProcess","MultiUserProcess_GyroPen","MultiUserProcess_NaiveBaseline"]
types=["MyBenData","MyData","MyMathBenData","MyMathEngData"]
users=["u00","u01","u02","u03","u04","u05","u06","u07","u08","u09"]
out_common="/Users/shamnarpgmail.com/Downloads/ExperimentData/FreeFormResults/New/Output"

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
    print_flag=True
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
            #outf1="/home/user/Documents/MTP/Images/1FreeFormResults/Output/GridImages/Stylus/"
            #outf2="/home/user/Documents/MTP/Images/1FreeFormResults/Output/GridImages/Traj1/"
            outf1="/Users/shamnarpgmail.com/Downloads/ExperimentData/Output/Grid_080220/"
            outf2="/Users/shamnarpgmail.com/Downloads/ExperimentData/Output/Grid_080220/"
            extracted_filename1 = outf1 + extracted_filename1
            extracted_filename2 = outf2 + extracted_filename2
            if (size in print_windows):
                draw_grids(processed_img1, size, extracted_filename1)
                draw_grids(processed_img2, size, extracted_filename2)
            
    return (diff_list)
'''
index=3
list_folder=["MultiUserProcess_FreeForm","MultiUserProcess_GyroPen_FreeForm","MultiUserProcess_NaiveBaseline_FreeForm","stylusData_FreeForm"]
in_folder="/Users/shamnarpgmail.com/Downloads/ExperimentData/FreeFormResults/New/FreeFormResults"
out_folder="/Users/shamnarpgmail.com/Downloads/ExperimentData/FreeFormResults/New/FreeFormResults/Resized_Images"
input_folder = in_folder + "/" + list_folder[index]
out_folder=out_folder +  "/" + list_folder[index] + "/"
all_files = [f for f in listdir(input_folder) if isfile(join(input_folder, f)) and f.endswith(".png")]
for s in all_files:
    single_file = input_folder + "/" + s
    print (single_file)
    img_size=128
    if (index==3):
        img=cv2.imread(single_file,cv2.IMREAD_UNCHANGED)
        *_,alpha=cv2.split(img)
        img=cv2.bitwise_not(alpha)
    else:
        img=cv2.imread(single_file,0)

    img=draw_box(img)
    img = cv2.resize(img,(img_size,img_size))
    fname=get_only_filename(single_file)
    oimg_name=out_folder+fname + ".png"
    print (oimg_name)
    cv2.imwrite(oimg_name, img)
'''




for u in range(1):
    user_index = 0
    process_index=0
    input_folder = stylus_data_common
    temp_common="/Users/shamnarpgmail.com/Downloads/ExperimentData/FreeFormResults"
    input_folder1 = traj_common + "/" + methods[process_index]+"/"+users[user_index]+"/"+types[0]
    input_folder2 = traj_common + "/" + methods[process_index]+"/"+users[user_index]+"/"+types[1]
    input_folder3 = traj_common + "/" + methods[process_index]+"/"+users[user_index]+"/"+types[2]
    input_folder4 = traj_common + "/" + methods[process_index]+"/"+users[user_index]+"/"+types[3]
    #output_file = out_common + "/" + methods[process_index] + "/"+users[user_index] + ".csv"
    output_file = out_common  + "/"+methods[process_index] + ".csv"
    #file_to_write = open(output_file, 'w') 
    count=0

    onlyfiles = [f for f in listdir(input_folder) if isfile(join(input_folder, f)) and f.endswith("1569565744758_1569565751442.png")]
    for el in onlyfiles:
        start_str= el.split("_")
        end_str = start_str[1].split(".")
        substr=start_str[0]+"To"+end_str[0]+"F.png"
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
            img_size=128
            img=cv2.imread(filename1,cv2.IMREAD_UNCHANGED)
            *_,alpha=cv2.split(img)
            img=cv2.bitwise_not(alpha)
            img1=cv2.imread(filename2,0)

            outf="/Users/shamnarpgmail.com/Downloads/ExperimentData/Output/NoGrid_080220/"

            img=draw_box(img)
            img = cv2.resize(img,(img_size,img_size))
            fname=get_only_filename(filename1)
            oimg_name=outf+fname +".png"
            print (oimg_name)
            cv2.imwrite(oimg_name, img)

            img1=draw_box(img1)
            img1= cv2.resize(img1,(img_size,img_size))
            fname=get_only_filename(filename2)
            oimg_name=outf+fname +"_"+str(process_index) +".png"
            print (oimg_name)
            cv2.imwrite(oimg_name, img1)


            '''
            difflist=process_images(filename1, filename2,1)        
            strlist= ', '.join(map(str,difflist))
            str_combined=el+","+el1+','+strlist
            #print(str_combined, file = file_to_write)
            print(count,strlist)
    
    if (count==133):
        print ("Ok" + str(user_index))
    else:
        print ("Not Ok" + str(user_index))
    
    print ("Done")
    #file_to_write.close() 
'''




        


        
        

