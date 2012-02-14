import argparse
import json
import math

from odetta.gff.feature import Feature
from odetta.gff.tree import build_tree, flatten_tree


parser = argparse.ArgumentParser(description='TODO')
parser.add_argument('gff')
parser.add_argument('--counts', help='TODO')

parser.add_argument('--min-length', type=float, default=float('-inf'),
    help='TODO')
parser.add_argument('--max-length', type=float, default=float('inf'),
    help='TODO')

#TODO using coverage args should require --counts
parser.add_argument('--min-coverage', type=float, default=float('-inf'),
    help='TODO')
parser.add_argument('--max-coverage', type=float, default=float('inf'),
    help='TODO')

parser.add_argument('--min-exons', type=float, default=float('-inf'),
    help='TODO')
parser.add_argument('--max-exons', type=float, default=float('inf'),
    help='TODO')




class Counts(object):

    @classmethod
    def from_file(cls, path):
        counts = {}
        for line in open(path):
            ID, counts_json = line.strip().split('\t')
            counts[ID] = json.loads(counts_json)
        
    def __init__(self, counts):
        self.counts = counts

    @property
    def total(self):
        total = 0
        for ref_counts in self.counts.values():
            total += sum(ref_counts.values())
        return total

    def coverage(self, feature):

        try:
            hits = sum(counts[feature.ID].values())
        except KeyError:
            hits = 0
        
        # coverage is RPKM, reads per kilobase of reference per million mapped reads
        # http://www.clcbio.com/manual/genomics/Definition_RPKM.html
        try:
            return (math.pow(10, 9) * hits) / (self.total * feature.length)
        except ZeroDivisionError:
            return 0
                    
    
if __name__ == '__main__':
    args = parser.parse_args()

    chromosomes, genes, transcripts = build_tree(Feature.from_file(args.gff))

    # TODO would be nice to split filters out into predicate functions
    for transcript in transcripts.values():

        exons = len([x for x in transcript.children if x.type == 'exon'])

        if args.counts:
            counts = Counts.from_file(args.counts)
            coverage = counts.coverage(transcript)
        else:
            coverage = 0

        if transcript.length < args.min_length or transcript.length > args.max_length \
        or exons < args.min_exons or exons > args.max_exons \
        or coverage < args.min_coverage or coverage > args.max_coverage:

            del transcript.parent.children[transcript.ID]


    for gene in genes.values():
        if len(gene.children) == 0:
            del gene.parent.children[gene.ID]


    flat = flatten_tree(chromosomes)
    print '\n'.join([str(f) for f in flat])
