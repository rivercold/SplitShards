#!/opt/python27/bin/python

import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("infer_dir", help="director containing inference results")
parser.add_argument("extid_dir", help="extid files")
parser.add_argument("shardNum", type=int)
parser.add_argument("outputDir", help="output director")
parser.add_argument("n_files", type=int, help="number of splitted files")
args = parser.parse_args()


shardMap = [list() for i in range(0, args.shardNum)]

nlines = 0

for i in range(1, args.n_files + 1):

    inferFilePath = args.infer_dir + "/" + str(i) + '.inference'
    extidFilePath = args.extid_dir + "/" + str(i) + '.extid'

    inferFile = open(inferFilePath, 'r')
    extidFile = open(extidFilePath, 'r')

    prev_extid = ""
    for line in inferFile:
        nlines += 1
        items = [int(item) for item in line.split(':')]
        shardID = items[1]

        extid = extidFile.readline().strip()
        if not extid:
            print nlines
            print "???"
            break
        if extid == prev_extid:
            print extid
            continue
        prev_extid = extid
        shardMap[shardID - 1].append(extid)

    inferFile.close()
    extidFile.close()
    print nlines

if not os.path.exists(args.outputDir):
    os.makedirs(args.outputDir)

for i in range(0, args.shardNum):
    outFile = open(args.outputDir+'/'+str(i + 1), 'w')
    for extid in shardMap[i]:
        if extid:
            outFile.write(extid + "\n")

extidFile.close()
outFile.close()


