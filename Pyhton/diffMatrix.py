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
###################Image folder ##########################################
input_folder1="/home/user/Documents/MTP/Images/MyEnData/Trajectory"
##########################################################################

def euclidian_distance(list1, list2):
    """Distance between two vectors."""
    squares = [(p-q) ** 2 for p, q in zip(list1, list2)]
    return sum(squares) ** .5

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

img=cv2.imread(input_folder1 + "/1.png",0)

if (img is not None):
    success=True
else:
    success=False

if (not success):
    print ("Image reading Error")
    sys.exit()

#extract image portion and remove unwanted parts
processed_img=draw_box(img)
l1 = np.arange(4).reshape(2,2)
print (l1)
l2 = np.arange(4,8,1).reshape(2,2)
print (l2)
dist = np.linalg.norm(l1-l2)
print (dist)

'''
diff = euclidian_distance(l1,l2)
print (diff)

diff = euclidian_distance(l3,l4)
print (diff)
'''

#add 10 lines of margin
[row,col]=processed_img.shape


print (row,col)
print (type(processed_img))
        


        
        

