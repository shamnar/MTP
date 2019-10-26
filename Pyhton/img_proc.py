#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 11:57:00 2019

@author: user
"""
import cv2
import numpy as np


###################Image folder ##########################################
img_folder="/home/user/Documents/MTP/Images/AlphaNumericForProcessing/"
##########################################################################
#file_name=img_folder + "IMG_20190831_152951" + ".jpg"
def draw_box(filename,outname):
    img_gray=cv2.imread(filename,0) #1 for color 0 for gray    
    thresh, img_bw = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)
    i=0
    prev_count=0
    img_width=img_bw.shape[1]
    hline_start=hline_end=0
    max_hline_start=max_hline_end=0
    diff=0
    state=0 # start line found
    
    print (img_bw.shape)

    for row in img_bw:
        current_count=np.count_nonzero(row)
        if (current_count!=img_width and prev_count==img_width and state==0):
            hline_start=i
            state=1 #first line found
    
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
    i=0
    top=bottom=0
    for row in new_arr:
        current_count = np.count_nonzero(row)
        if (state==0 and current_count!=img_width):
            state=1
            top=i
            continue
        
        if (state==1 and current_count==img_width):
            state=2
            bottom=i-1
        
        if (state==2):
            break
    
        i=i+1
    print (new_arr.shape, top, bottom)
    cv2.rectangle(img_bw,(top,max_hline_start),(bottom,max_hline_end),(0,0,0),1)
    oname="img_bw_"+outname+".jpg"
    cv2.imwrite(oname, img_bw)
    
    #cv2.line(img_bw, (0, max_hline_start), (img_width, max_hline_start), (0,0,0), 1)
    #cv2.line(img_bw, (0, max_hline_end), (img_width, max_hline_end), (0,0,0), 1)
    #oname="img_bw_"+outname+".jpg"
    #cv2.imwrite(oname, img_bw)

#fname=img_folder + "IMG_20190831_152729" + ".jpg" #zero, not ok
#fname=img_folder + "IMG_20190831_152814" + ".jpg" #one, ok # not working vert
#fname=img_folder + "IMG_20190831_152903" + ".jpg" #two ok #almost ok
#fname=img_folder + "IMG_20190831_152951" + ".jpg" #three ok 
#fname=img_folder + "IMG_20190831_153029" + ".jpg" #four almost ok #vert not ok
#fname=img_folder + "IMG_20190831_153120" + ".jpg" #five ok
#fname=img_folder + "IMG_20190831_172919" + ".jpg" #six not hori not ok
#fname=img_folder + "IMG_20190831_173009" + ".jpg" #seven not ok
#fname=img_folder + "IMG_20190831_153419" + ".jpg" #eight not ok
fname=img_folder + "IMG_20190831_153459" + ".jpg" #nine ok

draw_box(fname,"nine")

