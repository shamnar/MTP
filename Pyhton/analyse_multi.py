import matplotlib.pyplot as plt 
import operator

#import sys


def diff_list(list1, list2): 
    map_object = map(operator.sub, list1, list2)
    subtracted_list = list(map_object)
    return(subtracted_list)
    
def neg_count(list1):
    return(len(list(filter(lambda x: (x < 0), list1))))
    
def pos_neg_list_make(list1):
     return(list(map((lambda x: 0 if (x<0) else 1) , list1)))

fpath_common="/home/user/Documents/MTP/Images/1FreeFormResults/Output"
out_graph_folder=fpath_common+"/"+"Graph/"
processes=["MultiUserProcess","MultiUserProcess_GyroPen","MultiUserProcess_NaiveBaseline"]
users=["u00","u01","u02","u03","u04","u05","u06","u07","u08","u09"]
win_sizes=[3,4,5,7,10,15,20,30,40,50]

'''
user_index=int(sys.argv[1])
idx=win_sizes.index(int(sys.argv[2]))
print (user_index)
print (idx)
'''
for u in range(1):
    for i in range(10):
        if (i!=0 and i!=7):
            continue
        user_index=u
        idx=i
        data=[[],[],[]]
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
                    data[pindex].insert(i,[1000,1000,1000,1000,1000,1000,1000,1000,1000,1000])
                i+=1
            f.close()
            
        x=range(1,134)
        data1=data[0]
        data2=data[1]
        data3=data[2]
        y1 = [item[idx] for item in data1]
        y2 = [item[idx] for item in data2]
        y3 = [item[idx] for item in data3]
        y12=diff_list(y1,y2)
        y13=diff_list(y1,y3)
        y23=diff_list(y2,y3)
        y= [0] * 133
        pos_neg_list=pos_neg_list_make(y12)
        for el in pos_neg_list:
            print (el)
        print ("--")
        neg = neg_count(y12)
        #print (str(win_sizes[idx]) + ", "+ str(len(y12)-neg) + ", "+ str(neg))
        
        
        '''
        plt.figure()
        neg = neg_count(y12)
        plt.plot(x, y12, label = "multi", color='green') 
        plt.plot(x, y, label = "multi", color='red') 
        plt.title("Pos Count = "+str(len(y12)-neg) + "  Neg Count " + str(neg))
        oname=out_graph_folder+"diff_multi_gyro"+users[user_index]+"_"+str(win_sizes[idx])
        plt.savefig(oname)
        
        plt.figure()
        plt.plot(x, y13, label = "gyro", color='green') 
        plt.plot(x, y, label = "multi", color='red') 
        oname=out_graph_folder+"diff_multi_naive"+users[user_index]+"_"+str(win_sizes[idx])
        plt.savefig(oname)

        plt.figure()
        plt.plot(x, y23, label = "naive", color='green') 
        plt.plot(x, y, label = "multi", color='red') 
        oname=out_graph_folder+"diff_gyro_naive"+users[user_index]+"_"+str(win_sizes[idx])
        plt.savefig(oname)
        '''