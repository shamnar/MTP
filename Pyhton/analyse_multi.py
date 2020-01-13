import matplotlib.pyplot as plt 
import sys

fpath_common="/Users/shamnarpgmail.com/Downloads/ExperimentData/Output"
processes=["MultiUserProcess","MultiUserProcess_GyroPen","MultiUserProcess_NaiveBaseline"]
users=["u00","u01","u02","u03","u04","u05","u06","u07","u08","u09"]
win_sizes=[3,4,5,7,10,15,20,30,40,50]

data=[[],[],[]]
user_index=int(sys.argv[1])
idx=win_sizes.index(int(sys.argv[2]))

for pindex in range(3):
    fname=fpath_common+"/"+processes[pindex]+"/"+users[user_index]+".csv"
    f = open(fname, "r")
    i=0
    for x in f:
        x=x.rstrip()
        line = x.split(",")
        if (len(line)==12): 
            a= [int(line[i]) for i in range(2,12)]
            data[pindex].insert(i,a)
        else:
            data[pindex].insert(i,[500,500,500,500,500,500,500,500,500,500])
        i+=1
    f.close()
x=range(1,134)
data1=data[0]
data2=data[1]
data3=data[2]
x=range(1,134)
y1 = [item[idx] for item in data1]
y2 = [item[idx] for item in data2]
y3 = [item[idx] for item in data3]

plt.plot(x, y1, label = "multi", color='red') 
plt.plot(x, y2, label = "gyro", color='green') 
plt.plot(x, y3, label = "naive", color='blue') 
plt.show() 


