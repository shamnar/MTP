#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 27 16:00:32 2020

@author: shamnarpgmail.com
"""


from scipy.integrate import cumtrapz
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

from PIL import Image
from scipy.signal import find_peaks
import scipy.signal

import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib import transforms

import cv2
import math
import imutils

dict_strokes = { 1: "slope_left_bottom", 
                 2: "slope_right_bottom", 
                 3: "horizontal", 
                 4: "vertical",
                 5: "curve_left_open",
                 6: "curve_right_open",
                 7: "undefined"}


def getOmegaWithTime(filename, startTime, endTime):
    omegaList = []
    with open (filename) as inFile:
        for line in inFile:
            words = line.strip('\r\n').split(',')
            
            if len(words) != 4:
                continue
            if len(words[0]) != 13:
                continue
            hour = int(datetime.fromtimestamp(int(words[0])/1000).strftime('%H')) #for IST Data
            minute = int(datetime.fromtimestamp(int(words[0])/1000).strftime('%M')) #for IST Data
            second = int(datetime.fromtimestamp(int(words[0])/1000).strftime('%S')) #for IST Data
            
            miliSec = int(words[0])%1000 #for IST Data
            timeInMiliSec = (hour*60*60+minute*60+second)*1000+miliSec #for IST Data
            if startTime < timeInMiliSec < endTime:
                dataColumn = []
                dataColumn.append(float(words[0]))
                dataColumn.append(float(words[1]))
                dataColumn.append(float(words[2]))
                dataColumn.append(float(words[3]))
                omegaList.append(dataColumn)
                
    return np.array(omegaList)

def getAcc(filename, startTime, endTime):
    accList = []

    with open (filename) as inFile:
        for line in inFile:
            words = line.strip('\r\n').split(',')
            
            if len(words) != 4:
                continue
            if len(words[0]) != 13:
                continue
            hour = int(datetime.fromtimestamp(int(words[0])/1000).strftime('%H')) #for IST Data
            minute = int(datetime.fromtimestamp(int(words[0])/1000).strftime('%M')) #for IST Data
            second = int(datetime.fromtimestamp(int(words[0])/1000).strftime('%S')) #for IST Data
            
            miliSec = int(words[0])%1000 #for IST Data
            timeInMiliSec = (hour*60*60+minute*60+second)*1000+miliSec #for IST Data
            if startTime < timeInMiliSec < endTime:
                dataColumn = []
                dataColumn.append(float(words[0]))
                dataColumn.append(float(words[1]))
                dataColumn.append(float(words[2]))
                dataColumn.append(float(words[3]))
                accList.append(dataColumn)
        return np.array(accList)


def getOmega(filename, startTime, endTime):
    omegaList = []
    with open (filename) as inFile:
        for line in inFile:
            words = line.strip('\r\n').split(',')
            
            if len(words) != 4:
                continue
            if len(words[0]) != 13:
                continue
            hour = int(datetime.fromtimestamp(int(words[0])/1000).strftime('%H')) #for IST Data
            minute = int(datetime.fromtimestamp(int(words[0])/1000).strftime('%M')) #for IST Data
            second = int(datetime.fromtimestamp(int(words[0])/1000).strftime('%S')) #for IST Data
            
            miliSec = int(words[0])%1000 #for IST Data
            timeInMiliSec = (hour*60*60+minute*60+second)*1000+miliSec #for IST Data
            if startTime < timeInMiliSec < endTime:
                dataColumn = []
                dataColumn.append(float(words[1]))
                dataColumn.append(float(words[2]))
                dataColumn.append(float(words[3]))
                omegaList.append(dataColumn)
                
    return np.array(omegaList)


def convert_to_ist(timeepoch):
    hour = int(datetime.fromtimestamp(int(timeepoch)/1000).strftime('%H')) #for IST Data
    minute = int(datetime.fromtimestamp(int(timeepoch)/1000).strftime('%M')) #for IST Data
    second = int(datetime.fromtimestamp(int(timeepoch)/1000).strftime('%S')) #for IST Data
    miliSec = int(timeepoch)%1000 #for IST Data
    timeInMiliSec = (hour*60*60+minute*60+second)*1000+miliSec #for IST Data
    return (timeInMiliSec)

def gyroAngleComputeFun(omega,rate):

	angleList = []
	currentPitch = 0.
	currentRoll = 0.
	currentYaw = 0.
	startFlag = True

	
	for i in range(len(omega)):
	
		if startFlag:
			startFlag = False
			continue
		dataColumn = []

		deltaTime = 1./rate

		deltaRoll = omega[i][0]*deltaTime
		currentRoll += deltaRoll
		
		deltaPitch = omega[i][1]*deltaTime
		currentPitch += deltaPitch

		deltaYaw = omega[i][2]*deltaTime
		currentYaw += deltaYaw

		dataColumn.append(currentRoll)
		dataColumn.append(currentPitch)
		dataColumn.append(currentYaw)
		
		angleList.append(dataColumn)

	return np.array(angleList)






def classify_line(x,y):
    window_size=3
    if (len(x)>20):
        window_size=5
    
    x1=x[:window_size]
    y1=y[:window_size]
    
    x2=x[-window_size:]
    y2=y[-window_size:]
    
    x1_min=np.amin(x1)
    x1_max=np.amax(x1)
    
    x2_min=np.amin(x2)
    x2_max=np.amax(x2)
    
    y1_min=np.amin(y1)
    y1_max=np.amax(y1)
    
    y2_min=np.amin(y2)
    y2_max=np.amax(y2)
    
    horizontal_overlap=False
    vertical_overlap=False
    
    if (x2_min<x1_min<x2_max):
        horizontal_overlap=True
    elif (x1_min<x2_min<x1_max):
        horizontal_overlap=True

    if (y2_min<y1_min<=y2_max):
        vertical_overlap=True
    elif (y1_min<y2_min<y1_max):
        vertical_overlap=True
        
    if (horizontal_overlap==True):
        return 4
    elif (vertical_overlap==True):
        return 3
    
    if (x1_min < x2_min and y1_min < y2_min):
        return 1
    
    if (x1_min < x2_min and y1_min> y2_min):
        return 2
    
    return 7


def classify_curve(x,y):
    window_size=3
    if (len(x)>20):
        window_size=5
    
    if (window_size==3):
        minus=1
        plus=2
    else:
        minus=2
        plus=3
    
    mid = int(len(x)/2)
    
    x1=x[:window_size]
    y1=y[:window_size]
    
    istart=mid-minus
    iend = mid+plus
    
    
    x2=x[istart:iend]
    y2=y[istart:iend]
    
    x1_min=np.amin(x1)
    x1_max=np.amax(x1)
    
    x2_min=np.amin(x2)
    x2_max=np.amax(x2)
    
    y1_min=np.amin(y1)
    y1_max=np.amax(y1)
    
    y2_min=np.amin(y2)
    y2_max=np.amax(y2)
    
    if (x1_min < x2_min):
        return 5
    
    if (x1_min > x2_min):
        return 6
    
    return 7


def step_creator(vals, window_size):
    half_size=math.ceil(window_size/2)
    res= np.zeros(len(vals))
    for i in range(len(vals)+1-window_size):
        win=vals[i:i+window_size]
        if(np.count_nonzero(win)>=half_size):
            res[i]=1
        else:
            res[i]=0
    return (res)



def stroke_detect(omg, acc, pos):
    threshold=0.0025
    y=omg[:,1]
    x=np.arange(len(y))
    y = scipy.signal.savgol_filter(y, 51, 3) 
    y_dot=np.gradient(y)
    y_dot = scipy.signal.savgol_filter(y_dot, 51, 3) 
    y_dot[abs(y_dot) < threshold] = 0
    nz_index = np.where(y_dot !=0)
    imin=np.amin(nz_index)
    imax=np.amax(nz_index)
    y_s=step_creator(y_dot,5)
    cs=0
    flag=0
    lst_stroke=[]
    count=0
    for i in range(len(y_s)):
        el=int(y_s[i])
        print (el)

        if el==1 and cs==0:
            cs=1
            count=1
            continue
        elif el==0 and cs==0:
            continue
        elif (el==1 and cs==1):
            count=count+1
            if (count==5):
                st_index=i-5
                flag=1
            continue
        
        elif(el==0 and cs==1):
            if (flag==1):
                temp=[st_index, i]
                lst_stroke.append(temp)
            cs=0
            flag=0
            count=0
            
    return (lst_stroke)
                
                
                
        
            
            
    


def stroke_classify(index1, index2, pos):
    threshold = 0.9
    #get the data from the time period
    theta = math.radians(30)
    x=pos[:,1]
    y=pos[:,2]
    
    x=x[index1:index2]
    y=y[index1:index2]

    
    x=x-np.amin(x)
    y=y-np.amin(y)
    
    plt.figure()
    plt.plot(x,y)
    plt.show()
    
    
    results = {}

    coeffs = np.polyfit(x, y, 1)
    
    print (coeffs[0])

     # Polynomial Coefficients
    results['polynomial'] = coeffs.tolist()

    # r-squared
    p = np.poly1d(coeffs)
    # fit values, and mean
    yhat = p(x)                         # or [p(z) for z in x]
    ybar = np.sum(y)/len(y)          # or sum(y)/len(y)
    ssreg = np.sum((yhat-ybar)**2)   # or sum([ (yihat - ybar)**2 for yihat in yhat])
    sstot = np.sum((y - ybar)**2)    # or sum([ (yi - ybar)**2 for yi in y])
    r2 = (ssreg / sstot)
    
    
    print (r2)
    stroke_num = 0
    if (r2>threshold):
        stroke_num=classify_line(x,y)
    else:
        stroke_num=classify_curve(x,y)
        
    print (dict_strokes[stroke_num])


letter_start=["1569573927603","1569573939005","1569573950141","1569573957990","1569573968967"]
letter_end=["1569573936014","1569573947322","1569573955442","1569573964952","1569573976609"]
letter_act_start=["1569573931424","1569573942758","1569573952600","1569573960900","1569573970000"]
letter_act_end=["1569573933187","1569573944895","1569573953850","1569573963450","1569573974700"]

s=[[[190,200],[225,250],[300,310]],
   [[190,200],[225,250],[300,310]]
   ]

current_index=1
t_start=convert_to_ist(int(letter_start[current_index]))
t_end=convert_to_ist(int(letter_end[current_index]))
t_start1=convert_to_ist(int(letter_act_start[current_index]))
t_end1=convert_to_ist(int(letter_act_end[current_index]))




omg=getOmega("GYRO_09272019.csv",t_start, t_end)
pos = gyroAngleComputeFun(omg,50)
omg=getOmegaWithTime("GYRO_09272019.csv",t_start, t_end)
acc=getAcc("ACC_09272019.csv",t_start, t_end)


strk = stroke_detect(omg, acc, pos)
print (strk)

strokes=strk

plt.figure()

i=0
for el in strokes:
    x=pos[:,1]
    y=pos[:,2]
    
    x1=x[el[0]:el[1]]
    y1=y[el[0]:el[1]]
    plt.plot(x1,y1)
    i=(i+1)%3
    

plt.show

current_s=strokes[0]
t1=current_s[0]
t2=current_s[1]
stroke_classify(t1, t2, pos)

current_s=strokes[1]
t1=current_s[0]
t2=current_s[1]
stroke_classify(t1, t2, pos)

current_s=strokes[2]
t1=current_s[0]
t2=current_s[1]
stroke_classify(t1, t2, pos)
