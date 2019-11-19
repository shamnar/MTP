#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 11:57:00 2019

@author: user
"""
import cv2
import numpy as np
import sys
from os import listdir
from os.path import isfile, join

##############################################################################
#All user changing variavle goes here
grid_size=4

in_img_folder = "/home/user/Documents/MTP/Images/RSet"
out_img_folder = in_img_folder + "/output"
out_cord_folder =  in_img_folder + "/coordinates"
##############################################################################

def has_image(arr):
    if (np.count_nonzero(arr))==(grid_size*grid_size):
        return False
    else:
        return True

def has_image_bin(arr):
    if (np.count_nonzero(arr))==(grid_size*grid_size):
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

def find_euler_number(points):
    return (2-len(points))
    

def find_top_most_point(points):
    return (min(points, key=lambda x: x[1]))

def find_bottom_most_point(points):
    return (max(points, key=lambda x: x[1]))

def find_left_most_point(points):
    return (min(points, key=lambda x: x[0]))

def find_right_most_point(points):
    return (max(points, key=lambda x: x[0]))
    
def is_left(point1, point2):
    if (point1[0]>point2[0]):
        return True
    else:
        return False
    
def is_right(point1, point2):
    if (point1[0]<point2[0]):
        return True
    else:
        return False
    
def is_top(point1, point2):
    if (point1[1]>point2[1]):
        return True
    else:
        return False
    
def is_bottom(point1, point2):
    if (point1[1]<point2[1]):
        return True
    else:
        return False
    
def find_hole_positions(points):
    if (len(points)==1):
        return ([100])
    hps=[]
    hp = 0
    tl = points[0][0]
    b = find_bottom_most_point(points[0])
    mid = [0,int((tl[1] + b[1]) /2)]
    for i in range(1,len(points)):
        hp = 0
        t= find_top_most_point(points[i])
        b = find_bottom_most_point(points[i])
        l = find_left_most_point(points[i])
        r = find_right_most_point(points[i])
        if (is_left(tl, l)==True):
            if (is_top(mid,t)==True):
                hp= -1
            else:
                hp= -2
        elif (is_right(tl,r)==True):
            if (is_top(mid,t)==True):
                hp= +1
            else:
                hp= +2
        else:
            hp=100
        hps.append(hp)
    return (hps)

def is_line_horizontal(line):
    if (line[1]==line[3]):
        return True
    else:
        return False

def find_edge_ratio(box):
    vlen=0
    hlen=0
    ratio=0.0
    for line in box:
        if (is_line_horizontal(line)==True):
            hlen+=abs(line[0]-line[2])
        else:
            vlen+=abs(line[1]-line[3])

    if (float(vlen/hlen)>0.8 and float(vlen/hlen)<1.2):
        return (1)
    elif (float(vlen/hlen)<0.8):
        return (0.5)
    else:
        return 2



def find_vdc(box):
    vc=0
    for i in range(0,len(box)-2):
        line1=box[i]
        line2=box[i+1]
        line3=box[i+2]
        
        p1x=line1[0]
        p1y=line1[1]
        p2x=line1[2]
        p2y=line1[3]

        p3x=line2[0]
        p3y=line2[1]
        p4x=line2[2]
        p4y=line2[3]

        p5x=line3[0]
        p5y=line3[1]
        p6x=line3[2]
        p6y=line3[3]

        if (is_line_horizontal(line1)==False and is_line_horizontal(line2)==True and is_line_horizontal(line3)==False):
            t1=find_top_most_point([[p1x,p1y],[p2x,p2y]])
            t2=find_top_most_point([[p3x,p3y],[p4x,p4y]])
            t3=find_top_most_point([[p5x,p5y],[p6x,p6y]])

            b1=find_bottom_most_point([[p1x,p1y],[p2x,p2y]])
            b2=find_bottom_most_point([[p3x,p3y],[p4x,p4y]])
            b3=find_bottom_most_point([[p5x,p5y],[p6x,p6y]])
            if (t1==t2 and t2==t3):
                vc+=1
            elif (b1==b2 and b2==b3):
                vc+=1
            else:
                continue
    
    return (vc)

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
            if (([ci_start,ri,ci_end,ri] in points) == False):
                points.append([ci_start,ri,ci_end,ri])
            vflag[ri,ci]=1
        elif (num==5 or num==10):
            if (([ci,ri_start,ci,ri_end] in points) == False):
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
            if (([ci_start,ri,ci,ri] in points) == False):
                points.append([ci_start,ri,ci,ri])
            if (([ci,ri,ci,ri_end] in points) == False):                
                points.append([ci,ri,ci,ri_end])

            wpoints[index].append([ci,ri])
            vflag[ri,ci]=1
            if (direction==0):#change direction from (left-->right) to (top-->bottom)
                direction=2

        elif(num==8): #image is there only in left top win
            if (([ci,ri_start,ci,ri] in points) == False):
                points.append([ci,ri_start,ci,ri])
            if (([ci_start,ri,ci,ri] in points) == False):
                points.append([ci_start,ri,ci,ri])
            wpoints[index].append([ci,ri])
            vflag[ri,ci]=1
            if (direction==2):
                direction=1

        elif (num==11):
            if (([ci,ri_start,ci,ri] in points) == False):
                points.append([ci,ri_start,ci,ri])
            if (([ci,ri,ci_end,ri] in points) == False):
                points.append([ci,ri,ci_end,ri])
            wpoints[index].append([ci,ri])
            vflag[ri,ci]=1
            if (direction==2):
                direction=0

        elif(num==14):
            if (([ci,ri,ci,ri_end] in points) == False):
                points.append([ci,ri,ci,ri_end])
            if (([ci,ri,ci_end,ri] in points) == False):
                points.append([ci,ri,ci_end,ri])
            wpoints[index].append([ci,ri])
            vflag[ri,ci]=1
            if (direction==1):
                direction=2

        elif (num==4):
            if (([ci,ri_start,ci,ri] in points) == False):            
                points.append([ci,ri_start,ci,ri])
            if (([ci,ri,ci_end,ri] in points) == False):            
                points.append([ci,ri,ci_end,ri])
            wpoints[index].append([ci,ri])
            vflag[ri,ci]=1
            if (direction==1):
                direction=3

        elif (num==13):
            if (([ci_start,ri,ci,ri] in points) == False):            
                points.append([ci_start,ri,ci,ri])
            if (([ci,ri,ci,ri_end] in points) == False):            
                points.append([ci,ri,ci,ri_end])
            wpoints[index].append([ci,ri])
            vflag[ri,ci]=1
            if (direction==3):
                direction=1

        elif (num==1):
            if (([ci,ri,ci_end,ri] in points) == False):            
                points.append([ci,ri,ci_end,ri])
            if (([ci,ri,ci,ri_end] in points) == False):                        
                points.append([ci,ri,ci,ri_end])
            wpoints[index].append([ci,ri])
            vflag[ri,ci]=1
            if (direction==3):
                direction=0

        elif (num==7):
            if (([ci_start,ri,ci,ri] in points) == False):            
                points.append([ci_start,ri,ci,ri])
            if (([ci,ri_start,ci,ri] in points) == False):            
                points.append([ci,ri_start,ci,ri])
            wpoints[index].append([ci,ri])
            vflag[ri,ci]=1
            if (direction==0):
                direction=3

        elif (num==9):            
            wpoints[index].append([ci,ri])
            vflag[ri,ci]=1
            if (direction==2):
                if (([ci,ri_start,ci,ri] in points) == False):            
                    points.append([ci,ri_start,ci,ri])
                if (([ci,ri,ci_end,ri] in points) == False):            
                    points.append([ci,ri,ci_end,ri])
                direction=0
            elif (direction==3):
                if (([ci_start,ri,ci,ri] in points) == False):                            
                    points.append([ci_start,ri,ci,ri])
                if (([ci,ri,ci,ri_end] in points) == False):            
                    points.append([ci,ri,ci,ri_end])
                direction=1
            else:
                sys.exit(0)

        elif (num==6):
            wpoints[index].append([ci,ri])
            vflag[ri,ci]=1
            if (direction==1):
                if (([ci,ri,ci_end,ri] in points) == False):                            
                    points.append([ci,ri,ci_end,ri])
                if (([ci,ri,ci,ri_end] in points) == False):                            
                    points.append([ci,ri,ci,ri_end])
                direction=2
            elif (direction==0):
                if (([ci_start,ri,ci,ri] in points) == False):                            
                    points.append([ci_start,ri,ci,ri])
                if (([ci,ri_start,ci,ri] in points) == False):                            
                    points.append([ci,ri_start,ci,ri])
                direction=3
            else:
                sys.exit(0)

        else:
            sys.exit(0)
        [ri_start,ri,ri_end,ci_start,ci,ci_end]=update_window_pos(direction, ri,ci, grid_size)
        [ltwin,rtwin,lbwin,rbwin]=update_window(ri_start,ri,ri_end,ci_start,ci,ci_end)
    return


#arg1= sys.argv[1]
#fname="../new_testset/"
#fname=fname+arg1+".png"
    
onlyfiles = [f for f in listdir(in_img_folder) if isfile(join(in_img_folder, f)) and f.endswith(".png")]
print (len(onlyfiles))
for i in range(len(onlyfiles)):
#for i in range(1):
    fname = onlyfiles[i]
    fname_mod = fname[0:-4]
    print (str(i) + ": processing " + fname + " file")
    fname = fname.strip('\n')
    img=cv2.imread(in_img_folder + "/"+fname,0)
    if (img is not None):
        print ("read sucesss")
    else:
        print ("error in reading")
        break
    img = cv2.resize(img,(int(128),int(128)))
    (thresh, img_margin) = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)  
    [rowlen, collen]=img_margin.shape
    vflag=np.full((rowlen, collen), 0)
    vflag[0]=1
    vflag[rowlen-1]=1

    crow_index=0
    points=list()
    wpoints=list()
    outer_index=0
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
                    if (([ci1,ri1,ci2,ri1] in points) == False):
                        points.append([ci1,ri1,ci2,ri1])
                    if (([ci1,ri1,ci1,ri2] in points) == False):
                        points.append([ci1,ri1,ci1,ri2])
                    wpoints.append([])
                    wpoints[count].append([ci1,ri1])
                    start_marking(ri1,ci1,direction,grid_size, count)
                    outer_index =  len(points)
                    count+=1
                elif (num==14 and vflag[ri1,ci1]!=1):
                    vflag[ri1,ci1]=1
                    direction=2
                    img_pos=2
                    if (([ci1,ri1,ci2,ri1] in points) == False):
                        points.append([ci1,ri1,ci2,ri1])
                    if (([ci1,ri1,ci1,ri2] in points) == False):
                        points.append([ci1,ri1,ci1,ri2])
                    wpoints.append([])
                    wpoints[count].append([ci1,ri1])
                    start_marking(ri1,ci1,direction,grid_size, count)
                    count+=1
            ccol_index=ci1
        crow_index=ri1

    for el in points:
        img_margin = cv2.line(img_margin, (el[0],el[1]), (el[2],el[3]), (100,0,0), 1) 

#oname="output_img/"+arg1+".png"
    oname_img = out_img_folder + "/"+ fname
    oname_cord= out_cord_folder +"/"+ fname_mod + ".txt"
    cv2.imwrite(oname_img, img_margin)
    file_to_write = open(oname_cord, 'w') 
    for el in wpoints:
        print(el, file = file_to_write)
    file_to_write.close() 
    print ("write coordinates over")
    outer_box=points[0:outer_index]
    en = find_euler_number(wpoints)
    hp = find_hole_positions(wpoints)
    er = find_edge_ratio(outer_box)
    vdc =  find_vdc(outer_box)
    print ("euler number is " + str(en))
    print ("hole positions")
    print (hp)
    print ("edge ratio is " + str(er))
    print ("vdc is " + str(vdc))



