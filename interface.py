import numpy as np 
import subprocess
import click
import time
import pandas as pd 
import csv
import pickle
import random
#import database
title=[]
filename='data/Title.txt'
with open(filename, 'r') as f:
    l=f.readlines()
    for i in range(5000):
        title.append(str(l[i]))

db= pd.read_csv('data/Corpus.csv')
urls = db["url"].tolist()


with open("clusters.txt", "rb") as fp:
    ldata=pickle.load(fp) #[[labels],[centroids,labels]]
print(ldata[1])
dmat=np.load('Dmat.npy')
cent=[]
dcentsum=[]
for i in ldata[1]:
    cent.append(i)
for c in cent:
    dsum=0
    for a in cent:
        dsum+=(dmat[c[0]][a[0]])**2
    dcentsum.append(dsum)
sort_index = np.argsort(dcentsum) 
labelsrec=[]
for i in range(10):
    labelsrec.append(cent[sort_index[len(sort_index)-i-1]][1])
# print(labelsrec)
random.shuffle(labelsrec)
# print(labelsrec)
#user table
an_array = np.zeros((1000,5000))
# an_array[:] = np.NaN

lbatc=[]
for i in range(len(cent)):
    q=0
    cluster=[]
    for j in ldata[0]:
        if i==j:
            cluster.append(q)
        q+=1
    lbatc.append([i,cluster])
# print(lbatc)
click.clear()
def update(aid,t,uid):
    an_array[aid][uid]=t
def title(aid):
    tit=title[aid]
    return tit
def url(aid):Hindu_
    link=links[aid]
    return link
def rec(i):
    ls=[]
    if i==0:
        for i in range(10):
            # print(random.choice(lbatc[labelsrec[i]][1]))
            ind=random.choice(lbatc[labelsrec[i]][1])
            # print(i,' :',title(ind))
            ls.append(ind)

   else:


    
    return ls
ext=False
aid=0
history=[]
ten=rec(aid)
uid=0
click.clear()
while ext==False:
    t0=time.time()
    for i in range(len(ten)):
        print(i,title(ten[i]))
    select=int(input("which one ?"))
    print(str(url(ten[select])))
    subprocess.call(['firefox',str(url(ten[select]))], shell=False)
    aid=ten[select]
    tf=time.time()
    # update(history[len(history)],tf-t0,uid)
    # history.append(aid)
    click.clear()
click.clear()






