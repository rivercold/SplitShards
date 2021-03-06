#!/opt/python27/bin/python
import string
import sys, os
import argparse

# !/opt/python27/bin/python

__author__ = 'zhuyund'

import argparse
import os
import jobWriter

parser = argparse.ArgumentParser()
parser.add_argument("dv_dir")
parser.add_argument("kmeans_dir")
parser.add_argument("n_clusters")
parser.add_argument("n_shardmap_files", type=int)
parser.add_argument("output_file_path", help="write condor jobs into here")
parser.add_argument("qw")
parser.add_argument("--ref_threshold", "-r", type=float, help="ignore terms with ref > threshold", default=1.0)
parser.add_argument("--constant", "-c", type=int, default=0, help="1 = use constant weight")
parser.add_argument("--dataset", "-d", default="cwb", help="cwb gov2")
args = parser.parse_args()

executable = '/bos/tmp11/zhuyund/partition/Inference-qweight/qweightInference.sh'

log_file = "/tmp/zhuyund_infernce.log"
log_dir = "/bos/usr0/zhuyund/partition/SplitShards/log/"
err_file = log_dir + "inference.err"
out_file = log_dir + "inference.out"

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

if not os.path.exists(args.kmeans_dir + "/inference"):
    os.makedirs(args.kmeans_dir + "/inference")

job_file = open(args.output_file_path, "w")
d = ""
#if args.dataset == "gov2":
#    d = "_gov2"

for i in range(1, args.n_shardmap_files + 1):
    #"/bos/usr0/zhuyund/partition/Clustering-qweight/data/aol-first2.int_df{7} " \
    #"/bos/usr0/zhuyund/partition/Clustering-qweight/gov2_inlink.int_df_less{7} " \
    arguments = "{0}/{1}.dat  {2}/centroids/ {2}/inference/{1}.inference {3} {5} 1 1 field " \
                "/bos/usr0/zhuyund/partition/Clustering-qweight/gov2.all " \
                "{4} {6}".format(args.dv_dir,
                                 i,
                                 args.kmeans_dir,
                                 args.n_clusters,
                                 args.ref_threshold,
                                 args.qw,
                                 args.constant, d)

    job = jobWriter.jobGenerator(executable, arguments, log_file, err_file, out_file)

    job_file.write(job)

job_file.close()
