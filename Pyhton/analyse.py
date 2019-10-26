# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 


import time
import sys


currrent_num=0
currrent_sub=0
#####################################################################
list_num = ["ZERO", "ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE"]
list_sub = ["AIR_PAP","WB_AIR","WB_PAP"]
list_title=[["AIR_X_vs_PAP_X","AIR_X_vs_PAP_Y","AIR_X_vs_PAP_Z",
             "AIR_Y_vs_PAP_X","AIR_Y_vs_PAP_Y","AIR_Y_vs_PAP_Z",
             "AIR_Z_vs_PAP_X","AIR_Z_vs_PAP_Y","AIR_Z_vs_PAP_Z"],
            ["WB_X_vs_AIR_X","WB_X_vs_AIR_Y","WB_X_vs_AIR_Z",
             "WB_Y_vs_AIR_X","WB_Y_vs_AIR_Y","WB_Y_vs_AIR_Z",
             "WB_Z_vs_AIR_X","WB_Z_vs_AIR_Y","WB_Z_vs_AIR_Z"],
            ["WB_X_vs_PAP_X","WB_X_vs_PAP_Y","WB_X_vs_PAP_Z",
             "WB_Y_vs_PAP_X","WB_Y_vs_PAP_Y","WB_Y_vs_PAP_Z",
             "WB_Z_vs_PAP_X","WB_Z_vs_PAP_Y","WB_Z_vs_PAP_Z"]]
            
list_wb_time=[["22:04:38", "22:04:43"],
             ["22:04:45", "22:04:50"],
             ["22:04:53", "22:04:58"],
             ["22:05:00", "22:05:05"],
             ["22:05:18", "22:05:25"],
             ["22:05:27", "22:05:32"],
             ["22:05:34", "22:05:37"],
             ["22:05:40", "22:05:44"],
             ["22:05:46", "22:05:50"],
             ["22:06:03", "22:06:08"]]

list_paper_time=[["22:22:19", "22:22:25"],
             ["22:22:29", "22:22:34"],
             ["22:22:37", "22:22:43"],
             ["22:23:06", "22:23:11"],
             ["22:23:16", "22:23:22"],
             ["22:23:27", "22:23:33"],
             ["22:23:37", "22:23:41"],
             ["22:23:44", "22:23:49"],
             ["22:23:55", "22:24:01"],
             ["22:24:03", "22:24:08"]]

list_air_time=[["22:26:07", "22:26:12"],
             ["22:26:15", "22:26:20"],
             ["22:26:24", "22:26:29"],
             ["22:26:33", "22:26:38"],
             ["22:26:41", "22:26:46"],
             ["22:26:48", "22:26:54"],
             ["22:26:56", "22:27:01"],
             ["22:27:04", "22:27:08"],
             ["22:27:11", "22:27:16"],
             ["22:27:18", "22:27:23"]]


#####################################################################
PW_DIR="/home/user/Documents/MTP/ExperimentData/SensorData/"
FILE_NAME="GYRO_08232019"

FIG_DIR="/home/user/Documents/MTP/Images/Python/"
#####################################################################

WB_START    = '23.08.2019 22:04:38'
WB_END      = '23.08.2019 22:04:43'

PAPER_START = '23.08.2019 22:22:19'
PAPER_END   = '23.08.2019 22:22:25'

AIR_START   = '23.08.2019 22:26:07'
AIR_END     = '23.08.2019 22:26:12'

#####################################################################

def get_epoch_time(normal_time):
    pattern = '%d.%m.%Y %H:%M:%S'
    epoch = int(time.mktime(time.strptime(normal_time, pattern)))
    epoch = epoch * 1000
    return (epoch)
            
def main():
    
    num=0;
    sub=0
    for x in sys.argv:
        if (x.find("-num=")==0):
            num=x[5:]
            if (int(num)>=0 and int(num)<=9):
                currrent_num=int(num)
            else:
                print ("Error in argument num")
                sys.exit(1)
    
        if (x.find("-type=")==0):
                sub=x[6:]
                if (int(sub)==0 or int(sub)==1 or int(sub)==2):
                    currrent_sub=int(sub)
                else:
                    print ("Error in argument sub")
                    sys.exit(1)
                    
    print ("Generating graph for digit " + list_num[currrent_num] + " for type " + list_sub[currrent_sub])
    fname=PW_DIR+FILE_NAME+".csv"
    data = pd.read_csv(fname, sep="^\s+|\s*,\s*|\s+$", names=['time','x','y','z'],engine = 'python')
    
    WB_START = "23.08.2019 " + list_wb_time[currrent_num][0]
    WB_END = "23.08.2019 " + list_wb_time[currrent_num][1]
    
    PAPER_START = "23.08.2019 " + list_paper_time[currrent_num][0]
    PAPER_END = "23.08.2019 " + list_paper_time[currrent_num][1]
    
    AIR_START = "23.08.2019 " + list_air_time[currrent_num][0]
    AIR_END = "23.08.2019 " + list_air_time[currrent_num][1]
    
    
    
    
    
    e1=get_epoch_time(WB_START)
    e2=get_epoch_time(WB_END)
    e3=get_epoch_time(PAPER_START)
    e4=get_epoch_time(PAPER_END)
    e5=get_epoch_time(AIR_START)
    e6=get_epoch_time(AIR_END)
    
    wb_data = data[(data['time'] >= e1) & (data['time'] <= e2)] 
    wb_data = wb_data[['x','y','z']]

    paper_data=data[(data['time'] >= e3) & (data['time'] <= e4)] 
    paper_data = paper_data[['x','y','z']]
    
    air_data=data[(data['time'] >= e5) & (data['time'] <= e6)] 
    air_data = air_data[['x','y','z']]
    
    [row_wb, col_wb] = (wb_data.shape)
    [row_paper, col_paper] = (paper_data.shape)
    [row_air, col_air] = (air_data.shape)
    
    max_row = max(row_air, row_paper, row_wb)
    
    if (row_wb!=max_row):
        zeros_to_add=max_row-row_wb
        z = np.zeros([zeros_to_add, 3]) 
        z_d = pd.DataFrame({'x': z[:,0], 'y': z[:, 1], 'z': z[:, 2]})
        wb_data = wb_data.append(z_d , ignore_index=True)

    if (row_paper!=max_row):
        zeros_to_add=max_row-row_paper
        z = np.zeros([zeros_to_add, 3]) 
        z_d = pd.DataFrame({'x': z[:,0], 'y': z[:, 1], 'z': z[:, 2]})
        paper_data = paper_data.append(z_d , ignore_index=True)

    if (row_air!=max_row):
        zeros_to_add=max_row-row_air
        z = np.zeros([zeros_to_add, 3]) 
        z_d = pd.DataFrame({'x': z[:,0], 'y': z[:, 1], 'z': z[:, 2]})
        air_data = air_data.append(z_d , ignore_index=True)
        
    x=list(range(0, max_row))
    out_folder_name=FIG_DIR+list_num[currrent_num]+"/"+list_sub[currrent_sub]+"/"
    
    first_data=wb_data
    second_data=paper_data
    
    if (currrent_sub==0): #AIR_PAP
        first_data=air_data
        second_data=paper_data
    elif (currrent_sub==1):#WB_AIR
        first_data=wb_data
        second_data=air_data
    else:
        first_data=wb_data
        second_data=paper_data

    fig_num=1
    plt.figure(fig_num)
    title=list_title[currrent_sub][fig_num-1]
    y1=first_data['x']
    plt.plot(x,y1, color='green', linewidth = 2);
    y2=second_data['x']
    plt.plot(x,y2, color='blue', linewidth = 2);
    plt.title(title)
    plt.grid(True)
    fname=out_folder_name+title+".png"
    plt.savefig(fname)
    plt.show()
    
    fig_num+=1
    plt.figure(fig_num)
    title=list_title[currrent_sub][fig_num-1]
    y1=first_data['x']
    plt.plot(x,y1, color='green', linewidth = 2);
    y2=second_data['y']
    plt.plot(x,y2, color='blue', linewidth = 2);
    plt.title(title)
    plt.grid(True)
    fname=out_folder_name+title+".png"
    plt.savefig(fname)
    plt.show()
    
    fig_num+=1
    plt.figure(fig_num)
    title=list_title[currrent_sub][fig_num-1]
    y1=first_data['x']
    plt.plot(x,y1, color='green', linewidth = 2);
    y2=second_data['z']
    plt.plot(x,y2, color='blue', linewidth = 2);
    plt.title(title)
    plt.grid(True)
    fname=out_folder_name+title+".png"
    plt.savefig(fname)
    plt.show()
    
    fig_num+=1
    plt.figure(fig_num)
    title=list_title[currrent_sub][fig_num-1]
    y1=first_data['y']
    plt.plot(x,y1, color='green', linewidth = 2);
    y2=second_data['x']
    plt.plot(x,y2, color='blue', linewidth = 2);
    plt.title(title)
    plt.grid(True)
    fname=out_folder_name+title+".png"
    plt.savefig(fname)
    plt.show()
    
    fig_num+=1
    plt.figure(fig_num)
    title=list_title[currrent_sub][fig_num-1]
    y1=first_data['y']
    plt.plot(x,y1, color='green', linewidth = 2);
    y2=second_data['y']
    plt.plot(x,y2, color='blue', linewidth = 2);
    plt.title(title)
    plt.grid(True)
    fname=out_folder_name+title+".png"
    plt.savefig(fname)
    plt.show()
    
    fig_num+=1
    plt.figure(fig_num)
    title=list_title[currrent_sub][fig_num-1]
    y1=first_data['y']
    plt.plot(x,y1, color='green', linewidth = 2);
    y2=second_data['z']
    plt.plot(x,y2, color='blue', linewidth = 2);
    plt.title(title)
    plt.grid(True)
    fname=out_folder_name+title+".png"
    plt.savefig(fname)
    plt.show()
    
    fig_num+=1
    plt.figure(fig_num)
    title=list_title[currrent_sub][fig_num-1]
    y1=first_data['z']
    plt.plot(x,y1, color='green', linewidth = 2);
    y2=second_data['x']
    plt.plot(x,y2, color='blue', linewidth = 2);
    plt.title(title)
    plt.grid(True)
    fname=out_folder_name+title+".png"
    plt.savefig(fname)
    plt.show()
    
    fig_num+=1
    plt.figure(fig_num)
    title=list_title[currrent_sub][fig_num-1]
    y1=first_data['z']
    plt.plot(x,y1, color='green', linewidth = 2);
    y2=second_data['y']
    plt.plot(x,y2, color='blue', linewidth = 2);
    plt.title(title)
    plt.grid(True)
    fname=out_folder_name+title+".png"
    plt.savefig(fname)
    plt.show()
    
    fig_num+=1
    plt.figure(fig_num)
    title=list_title[currrent_sub][fig_num-1]
    y1=first_data['z']
    plt.plot(x,y1, color='green', linewidth = 2);
    y2=second_data['z']
    plt.plot(x,y2, color='blue', linewidth = 2);
    plt.title(title)
    plt.grid(True)
    fname=out_folder_name+title+".png"
    plt.savefig(fname)
    plt.show()   
    
main()

