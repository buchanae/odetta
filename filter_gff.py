import argparse
from collections import defaultdict
import json
import math

import gff


def load(gff_path, counts_path):

    mRNAs = {}
    exons = defaultdict(list)

    for f in gff.reader(gff_path):
        if f.type == 'mRNA':
            mRNAs[f.attributes['ID']] = f
        elif f.type == 'exon':
            exons[f.attributes['Parent']].append(f)

    total = 0
    for line in open(counts_path):
        ref_name, counts_json = line.strip().split('\t')
        counts = json.loads(counts_json)
        total += counts['total']
        mRNAs[ref_name].counts = counts

    for ID, m in mRNAs.items():
        if ID in exons:
            m.exons = exons[ID]

        # TODO note about FPKM
        m.coverage = (math.pow(10, 9) * m.counts['total']) / (total * m.length)

    return mRNAs.values()

def make_predicate(min_length, max_length, min_coverage):
    def f(m):
        return m.length >= min_length and m.length <= max_length \
               and len(m.exons) > 1 and m.coverage >= min_coverage:
    return f


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="TODO.")

    parser.add_argument('gff', help='TODO')

    #TODO flags for different filters

    parser.add_argument('counts', help='TODO')
    parser.add_argument('--min-length', type=float, default=float('-inf'))
    parser.add_argument('--max-length', type=float, default=float('inf'))
    parser.add_argument('--min-coverage', type=float, default=float('-inf'))

    args = parser.parse_args()
    mRNAs = load(args.gff, args.counts)
    p = make_predicate(args.min_length, args.max_length, args.min_coverage)
    print filter(p, mRNAs)
