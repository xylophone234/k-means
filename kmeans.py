from __future__ import division
import codecs
import random
import re
import math
import os
import json

'''
k-means cluster for news
'''

stopwords = set(codecs.open('stopwords.txt', 'r', 'utf-8').readlines())
wcss=0.0

def createVocab(path):
    # path='./data'
    vocabulary = set([])
    # stopwords=set(codecs.open('stopwords.txt','r','utf-8').readlines())
    for filename in os.listdir(path):
        vocabulary = vocabulary | set(
            codecs.open(path + '/' + filename, 'r', 'utf-8').read().split())
    return list(vocabulary - stopwords)



def prepareData(path):
    dataset = []
    numRe = re.compile('\d+')
    i=0
    for filename in os.listdir(path):
        content = codecs.open(path + '/' + filename, 'r', 'utf-8').read().split()
        content = [word for word in content if word not in stopwords]
        # y,num=filename.split('.')[0].replace(numRe,' ')
        y, num = numRe.subn('', filename.split('.')[0])
        x={word:content.count(word) for word in content}
        data = {'x':x,'y':y}
        dataset.append(data)
        i+=1
        # if i>50 :break
    return dataset


def cosDistence(vec1, vec2):
    sum = 0.0
    if(len(vec1.keys())==0 and len(vec2.keys())==0):return 0
    for key in vec1.keys():
        if key in vec2.keys():
            sum += vec1[key] * vec2[key]
    return 1 - sum

def normal(vec):
	sum=0.0
	for key in vec:
		sum+=vec[key]**2
	for key in vec:
		vec[key]=vec[key]/math.sqrt(sum)
	#return vec

def findNearest(vec,vecList,disfun):
	dis=[]
	for i in range(len(vecList)):
		d=disfun(vec,vecList[i])
		# print (vec)
		# print (vecList[i])
		# print ('d',d)
		dis.append(d)
		# print dis
	index=0
	for i in range(len(dis)):
		if(dis[i]<dis[index]):
			index=i
	return index,dis[index]

def calcCerter(cluster,oldcenter):
	''' calc cluster certer'''
	center={}
	for key in oldcenter:
		center[key]=0

	i=0
	for vec in cluster:
		i+=1
		# if i%100==0:print('i',i)
		for key in center:
			if key in vec.keys():
				center[key]+=vec[key]
			# else:
			# 	center[key]=vec[key]
	for key in center:
		center[key]=center[key]/len(cluster)
	return center

def errorCeter(oldcenter,newcenter):
	sum=0.0
	for  i in range(len(oldcenter)):
		d=cosDistence(oldcenter[i],newcenter[i])
		sum+=d
		# print('d',d,sum)
	return sum/len(oldcenter)

def reAssing(dataset,centers):
	wcss=0
	i=0
	for doc in dataset:
		doc['cluster'],dis=findNearest(doc['x'],centers,cosDistence)
		wcss+=dis
		i+=1
		# if i%100==0:print ('reassing',i)
	# print ([doc['cluster'] for doc in dataset])
	print ('wcss',wcss)

def reCenter(dataset,oldcenters,k):
	centers=[]
	for i in range(k):
		group=[doc['x'] for doc in dataset if doc['cluster']==i ]
		# print(len(group))
		center=calcCerter(group,oldcenters[i])
		normal(center)
		centers.append(center)
	return centers

def fc(co):
	recall={}
	for result in co:
		sum=0
		for lab in co[result]:
			sum+=co[result][lab]
		recall[result]=co[result][result]/sum
		print ('recall:',result,recall[result])
	ac={}
	col={}
	for result in co:
		col[result]=0;
	for result in co:
		for lab in co[result]:
			col[lab]+=co[result][lab]
	for result in co:
		ac[result]=co[result][result]/col[result]
		print ('ac:',result,ac[result])

	for result in co:
		print ('f1:',result,2*ac[result]*recall[result]/(ac[result]+recall[result]))
def result(dataset,k):
	
	cluster2lables=['0']*k
	for i in range(k):
		cluster=[doc['y'] for doc in dataset if doc['cluster']==i]
		lables=[(lab,cluster.count(lab)) for lab in set(cluster)]
		lables.sort(key=lambda x:x[1])
		cluster2lables[i]=lables[-1][0]
		# print lables
	res={'sports':{'sports':0,'auto':0,'business':0},
		'auto':{'sports':0,'auto':0,'business':0},
		'business':{'sports':0,'auto':0,'business':0}}
	
	for doc in dataset:
			res[doc['y']][cluster2lables[doc['cluster']]]+=1
		# else:
		# 	res[doc['y']]=[0,0,0]
		# 	res[doc['y']][doc['cluster']]+=1
	fc(res)
	return res

print ('loading dataset')
dataset=prepareData('data')
for doc in dataset:
		normal(doc['x'])
print('normal OK')
def main(k):
	print ('k=',k)
	oldcenters=[p['x'] for p in random.sample(dataset,k)]
	# print(len(oldcenters))
	reAssing(dataset,oldcenters)
	newcenters=reCenter(dataset,oldcenters,k)
	# print newcenters
	e=errorCeter(newcenters,oldcenters)
	while e>0.003:
		print ('e',e)
		# print dataset
		oldcenters=newcenters
		reAssing(dataset,oldcenters)
		newcenters=reCenter(dataset,oldcenters,k)
		# print newcenters
		e=errorCeter(newcenters,oldcenters)
	print(result(dataset,k))

if __name__ == '__main__':
	main(3)