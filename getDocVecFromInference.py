#!/opt/python27/bin/python
import argparse
import os, sys

class Field:
    def __init__(self):
        self.len = 0
        self.n_vocab = 0
        self.terms = []

    @staticmethod
    def to_string(field):
        s = str(field.n_vocab)
        s += ' ' + str(field.len)
        s += ' ' + ' '.join(field.terms)
        return s


def parse_datline(dat_line):
    items = dat_line.split()
    i = 0
    fields = []
    while i < len(items):
        field = Field()
        field.n_vocab = int(items[i])
        i += 1
        field.len = int(items[i])
        i += 1
        while i < len(items) and ':' in items[i]:
            field.terms.append(items[i])
            i += 1
        fields.append(field)
    return fields


def get_body(dat_line):
    fields = parse_datline(dat_line)
    return Field.to_string(fields[-1])


def get_whole(dat_line):
    fields = parse_datline(dat_line)
    vec = {}
    lenth = 0
    for field in fields:
        for term in field.terms:
            t, freq = [int(s) for s in term.split(':')]
            vec[t] = vec.get(t, 0) + freq
            lenth += freq
    #vec_sorted = sorted(vec)
    n_vocab = len(vec)
    s = str(n_vocab) + ' ' + str(lenth) + ' '
    s += ' '.join(['{0}:{1}'.format(t, vec[t]) for t in vec])
    return s


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("shard_file")
    parser.add_argument("partition_name")
    parser.add_argument("dat_dir")
    parser.add_argument("infer_dir")
    parser.add_argument("--dataset", "-d", default='cwb', help="gov2, cwa, cwb")
    parser.add_argument("--field", "-f",  type=int, default="2", help="0: fielded 1: body only 2:whole")
    args = parser.parse_args()

    if args.dataset != "cwb":
        print "Sorry! Do not have function for " + args.dataset
        exit(-1)

    shards = set()
    sizes = {}
    shard_dirs = {}
    out_files = {}
    output_lines = {}

    n_docs = 50220423
    split_size = 100000
    pref = "cw09catB"

    for line in open(args.shard_file):
        shard, n_splits, size = line.split()
        shard = int(shard)
        shards.add(shard)
        shard_dirs[shard] = "./output/" + args.partition_name + '/' + str(shard) + '/docvec/'
        if not os.path.exists(shard_dirs[shard]):
            os.makedirs(shard_dirs[shard])
        sizes[shard] = 0
        out_files[shard] = open(shard_dirs[shard] + '1.dat', 'w')
        output_lines[shard] = ""


    start = 1
    while start <= n_docs:
        end = start + split_size - 1
        if end > n_docs:
            end = n_docs
        infer_file = open("{0}/{1}_{2}-{3}.inference".format(args.infer_dir, pref, start, end))
        dat_file = open("{0}/{1}_{2}-{3}.dat".format(args.dat_dir, pref, start, end))
        print "{0}/{1}_{2}-{3}.dat".format(args.dat_dir, pref, start, end)
        for infer_line in infer_file:
            dat_line = dat_file.readline().strip()
            if not dat_line:
                infer_file.close()
                dat_file.close()
                continue
            intid, shard = [int(t) for t in infer_line.split(':')]
            if shard not in shards:
                continue
            if args.field == 0:
                output_lines[shard] += dat_line + '\n'
            if args.field == 1:
                output_lines[shard] += get_body(dat_line) + '\n'
            if args.field == 2:
                output_lines[shard] += get_whole(dat_line) + '\n'

            sizes[shard] += 1

            if sizes[shard] % 1000 == 0:
                out_files[shard].write(output_lines[shard])
                output_lines[shard] = ""
                if sizes[shard] % 100000 == 0:
                    out_files[shard].close()
                    out_files[shard] = open(shard_dirs[shard] + str(sizes[shard]/split_size + 1) + '.dat', 'w')
        start = end + 1

    for shard in shards:
        if output_lines[shard]:
            out_files[shard].write(output_lines[shard])
            out_files[shard].close()

main()
