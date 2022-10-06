import numpy as np
from matplotlib import pyplot as plt
import math
import os

def read(path):
    with open(path,'r')as f:
        row=f.readlines()

    data=[]
    for i in range(len(row)):
        temp=row[i]
        temp=np.array(temp.split()).astype(float)
        data.append(temp)
    return data

def draw(data,name):
    plt.clf()
    x=[]
    y=[]
    sensitivity=[]
    for i in range(1,len(data)):
        x.append(data[i][0])
        y.append(data[i][1])
        sensitivity.append(data[i][2])
    plt.scatter(x,y,c=sensitivity,cmap='seismic')
    plt.colorbar()
    plt.savefig(name+'.png')

#a和b是两个不同的待相加的数组/list
def pluse(kernel,phvel):
    result=np.zeros([len(phvel),3])
    finalsum=0
    for i in range(len(phvel)):
        vlo=phvel[i][0]
        vla=phvel[i][1]
        dv=(phvel[i][2]-3)/phvel[i][2]
        temp_sum=0
        for j in range(len(kernel)):
            klo=kernel[j][0]
            kla=kernel[j][1]
            k  =kernel[j][2]
            if k==float('nan'):
                k=0
            if vlo-klo<=0.25 and klo-vlo<0.25 and vla-kla<=0.25 and kla-vla<0.25:
                temp_sum=temp_sum+k*dv
        result[i][0]=vlo
        result[i][1]=vla
        result[i][2]=temp_sum

        finalsum=finalsum+temp_sum
    

    return finalsum,result

#把一定经纬度范围外的kernel置零,把接收点和震源处的nan置零
def zero(a,r):
    for i in range(len(a)):
        #if a[i][1]>30 or a[i][1]<26 or a[i][0]<97 or a[i][0]>107 or math.isnan(a[i][2]):
        if a[i][1]>1 or a[i][1]<-1  or math.isnan(a[i][2]):
            a[i][2]=0

def rotateAngle(slo,sla,rlo,rla):
    rlo=rlo-slo
    rla=rla-sla
    if rlo>0:
        theta=math.atan(rla/rlo)
    elif rlo<0:
        theta=math.atan(rla/rlo)+np.pi
    #即：震中和台站在同一位置
    elif abs(rlo)<1e-6:
        theta=0
    return theta

def rotate(kernel,slo,sla,rlo,rla,r):
    #旋转角度
    theta=rotateAngle(slo,sla,rlo,rla)
    for i in range(len(kernel)):
        x1=kernel[i][0]
        y1=kernel[i][1]
        kernel[i][0]=x1*math.cos(theta)-y1*math.sin(theta)+slo
        kernel[i][1]=x1*math.sin(theta)+y1*math.cos(theta)+sla
    return theta

kernel_filein=os.sys.argv[1]
slo =   float(os.sys.argv[2])
sla =   float(os.sys.argv[3])
rlo =   float(os.sys.argv[4])
rla =   float(os.sys.argv[5])
dist=   float(os.sys.argv[6])

arcdist=dist/6371*180/np.pi

kernel  =   read(kernel_filein)
phvel   =   read('./f_0.2218.phvel.txt')
zero(kernel,arcdist)
theta=rotate(kernel,slo,sla,rlo,rla,arcdist)
dlnA,result=pluse(kernel,phvel)
print("filein",kernel_filein,"\trotate theta:",math.degrees(theta),"\tdlnA=",dlnA)
#dlnA=0.41711637475541313
#draw(result,'result'+kernel_filein)
draw(kernel,'rotate_'+kernel_filein)
