#!/opt/python27/bin/python

import os
import time
import argparse
import random

parser = argparse.ArgumentParser()
parser.add_argument("name", help="run name. eg. cw-s1c1")
parser.add_argument("shard", help="shard to split. eg. 1")
parser.add_argument("n_clusters")
parser.add_argument("iter_count")
args = parser.parse_args()
print args

baseDir = '/bos/usr0/zhuyund/partition/SplitShards/output/' + args.name

# corresponding to different sampling trials
datFile = baseDir+'/sampled.dat'

lamda = '0.1'
minVocabSeed = '100'

trialDir = baseDir + '/kmeans/'
centroidDir = trialDir+'centroids/'

if not os.path.exists(trialDir):
    print trialDir
    os.makedirs(trialDir)

if not os.path.exists(centroidDir):
    print centroidDir
    os.makedirs(centroidDir)


logFile = trialDir+'log'
cmd = "/bos/tmp11/zhuyund/partition/Clustering-field/kmeans "\
      +datFile+" "+args.n_clusters+" "+lamda+" "+args.iter_count\
      +" "+centroidDir+" "+minVocabSeed+" " + '1 ' + '1 '

cmd += " " + "selectSeed" + " >& " + logFile
r = random.random() * 60
time.sleep(int(r))
os.system(cmd)



