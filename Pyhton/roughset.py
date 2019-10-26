#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 11:57:00 2019

@author: user
"""
import cv2
import numpy as np
import sys

def has_image(arr):
    if (np.count_nonzero(arr))==25:
        return False
    else:
        return True

def has_image_bin(arr):
    if (np.count_nonzero(arr))==25:
        return 0
    else:
        return 1

def binary_to_decimal(digit3, digit2, digit1, digit0):
    return((digit3*8)+(digit2*4)+(digit1*2)+(digit0))

def convert_win_to_number(ltwin, rtwin, lbwin, rbwin):
    dig3=has_image_bin(ltwin)
    dig2=has_image_bin(rtwin)
    dig1=has_image_bin(lbwin)
    dig0=has_image_bin(rbwin)
    num=binary_to_decimal(dig3,dig2,dig1,dig0)
    return(num)

def update_window_pos(direction, ri,ci, grid_size):
    if (direction==0): #left to right
        ri_start=ri-grid_size
        ri_end=ri+grid_size
        ci_start=ci
        ci=ci+grid_size
        ci_end=ci+grid_size
    elif (direction==1):#right to left
        ri_start=ri-grid_size
        ri_end=ri+grid_size
        ci_end=ci
        ci=ci-grid_size
        ci_start=ci-grid_size
    elif (direction==2):#top to bottom
        ci_start=ci-grid_size
        ci_end=ci+grid_size
        ri_start=ri
        ri=ri+grid_size
        ri_end=ri+grid_size
    elif (direction==3):#bottom to top
        ci_start=ci-grid_size
        ci_end=ci+grid_size
        ri_end=ri
        ri=ri-grid_size
        ri_start=ri-grid_size

    return ([ri_start,ri,ri_end,ci_start,ci,ci_end])

def update_window(ri_start,ri,ri_end,ci_start,ci,ci_end):
    ltwin=img_margin[ri_start:ri,ci_start:ci]
    rtwin=img_margin[ri_start:ri, ci:ci_end]
    lbwin=img_margin[ri:ri_end,ci_start:ci]
    rbwin=img_margin[ri:ri_end, ci:ci_end]
    return([ltwin,rtwin,lbwin,rbwin])



def start_marking(ri, ci, direction, grid_size, index):
    ri_begin=ri
    ci_begin=ci
    [ri_start,ri,ri_end,ci_start,ci,ci_end]=update_window_pos(direction, ri,ci, grid_size)
    [ltwin,rtwin,lbwin,rbwin]=update_window(ri_start,ri,ri_end,ci_start,ci,ci_end)
    loopcount=-1
    while (not(ri_begin==ri and ci_begin==ci)):
        loopcount+=1
        num=convert_win_to_number(ltwin,rtwin,lbwin,rbwin)  
        if (num==12 or num==3): #image in 2 boxes
            points.append([ci_start,ri,ci_end,ri])
            vflag[ri,ci]=1
        elif (num==5 or num==10):
            points.append([ci,ri_start,ci,ri_end])
            vflag[ri,ci]=1

        elif (num==0): #if no image change direction if neccessary
            if (direction==0):
                direction=0
            elif (direction==1):
                direction=1
            elif (direction==2):
                direction=1
            elif (direction==3):
                direction=0

            vflag[ri,ci]=1

        elif (num==2): #image is there only in left bottom win
            points.append([ci_start,ri,ci,ri])
            points.append([ci,ri,ci,ri_end])
            wpoints[index].append([ci,ri])
            vflag[ri,ci]=1
            if (direction==0):#change direction from (left-->right) to (top-->bottom)
                direction=2

        elif(num==8): #image is there only in left top win
            points.append([ci,ri_start,ci,ri])
            points.append([ci,ri,ci_start,ri])
            wpoints[index].append([ci,ri])
            vflag[ri,ci]=1
            if (direction==2):
                direction=1

        elif (num==11):
            points.append([ci,ri_start,ci,ri])
            points.append([ci,ri,ci_end,ri])
            wpoints[index].append([ci,ri])
            vflag[ri,ci]=1
            if (direction==2):
                direction=0

        elif(num==14):
            points.append([ci,ri,ci,ri_end])
            points.append([ci,ri,ci_end,ri])
            wpoints[index].append([ci,ri])
            vflag[ri,ci]=1
            if (direction==1):
                direction=2

        elif (num==4):
            points.append([ci,ri_start,ci,ri])
            points.append([ci,ri,ci_end,ri])
            wpoints[index].append([ci,ri])
            vflag[ri,ci]=1
            if (direction==1):
                direction=3

        elif (num==13):
            points.append([ci_start,ri,ci,ri])
            points.append([ci,ri,ci,ri_end])
            wpoints[index].append([ci,ri])
            vflag[ri,ci]=1
            if (direction==3):
                direction=1

        elif (num==1):
            points.append([ci,ri,ci_end,ri])
            points.append([ci,ri,ci,ri_end])
            wpoints[index].append([ci,ri])
            vflag[ri,ci]=1
            if (direction==3):
                direction=0

        elif (num==7):
            points.append([ci_start,ri,ci,ri])
            points.append([ci,ri,ci,ri_start])
            wpoints[index].append([ci,ri])
            vflag[ri,ci]=1
            if (direction==0):
                direction=3

        elif (num==9):
            
            wpoints[index].append([ci,ri])
            vflag[ri,ci]=1
            if (direction==2):
                points.append([ci,ri_start,ci,ri])
                points.append([ci,ri,ci_end,ri])
                direction=0
            elif (direction==3):
                points.append([ci_start,ri,ci,ri])
                points.append([ci,ri,ci,ri_end])
                direction=1
            else:
                sys.exit(0)

        elif (num==6):
            wpoints[index].append([ci,ri])
            vflag[ri,ci]=1
            if (direction==1):
                points.append([ci,ri,ci_end,ri])
                points.append([ci,ri,ci,ri_end])
                direction=2
            elif (direction==0):
                points.append([ci_start,ri,ci,ri])
                points.append([ci,ri,ci,ri_start])
                direction=3
            else:
                sys.exit(0)

        else:
            sys.exit(0)
        [ri_start,ri,ri_end,ci_start,ci,ci_end]=update_window_pos(direction, ri,ci, grid_size)
        [ltwin,rtwin,lbwin,rbwin]=update_window(ri_start,ri,ri_end,ci_start,ci,ci_end)
    return

arg1= sys.argv[1]
fname="../new_testset/"
fname=fname+arg1+".png"
img=cv2.imread(fname,0)
img=cv2.resize(img,(128,128), interpolation = cv2.INTER_AREA)
(thresh, img_bw) = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)  
#add 10 pixel border-- start
img=img_bw

img_margin= np.full((150, 150), 255)
vflag=np.full((150, 150), 0)
vflag[0]=1
vflag[149]=1

x_offset=10
y_offset=10
img_margin[x_offset:img.shape[0]+x_offset,y_offset:img.shape[1]+y_offset] = img
#add 10 pixel border--end

[rowlen, collen]=img_margin.shape
grid_size=5
crow_index=0
points=list()
wpoints=list()
count=0

while (crow_index<rowlen-grid_size):
    ccol_index=0
    while(ccol_index<collen-grid_size):
        ri1=crow_index+grid_size
        ci1=ccol_index+grid_size
        ri2=ri1+grid_size
        ci2=ci1+grid_size
        ltwin=img_margin[crow_index:ri1,ccol_index:ci1]
        rtwin=img_margin[crow_index:ri1, ci1:ci2]
        lbwin=img_margin[ri1:ri2,ccol_index:ci1]
        rbwin=img_margin[ri1:ri2, ci1:ci2]
        num=convert_win_to_number(ltwin,rtwin,lbwin,rbwin)
        if (num==0 or num==15):
            vflag[ri1,ci1]=1
        elif (num>0):
            if (num==1 and vflag[ri1,ci1]!=1):
                vflag[ri1,ci1]=1
                direction=0
                img_pos=1
                points.append([ci1,ri1,ci2,ri1])
                points.append([ci1,ri1,ci1,ri2])
                wpoints.append([])
                wpoints[count].append([ci1,ri1])
                start_marking(ri1,ci1,direction,grid_size, count)
                count+=1
            elif (num==14 and vflag[ri1,ci1]!=1):
                vflag[ri1,ci1]=1
                direction=2
                img_pos=2
                points.append([ci1,ri1,ci2,ri1])
                points.append([ci1,ri1,ci1,ri2])
                wpoints.append([])
                wpoints[count].append([ci1,ri1])
                start_marking(ri1,ci1,direction,grid_size, count)
                count+=1
        ccol_index=ci1
    crow_index=ri1

for el in points:
    img_margin = cv2.line(img_margin, (el[0],el[1]), (el[2],el[3]), (100,0,0), 1) 

oname="output_img/"+arg1+".png"
cv2.imwrite(oname, img_margin) 
for el in wpoints:
    print (el)


