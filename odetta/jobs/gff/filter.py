import argparse
from collections import OrderedDict
import json
import math

from odetta.gff.feature import Feature


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


def build_tree(features):
    chromosomes = OrderedDict()
    genes = OrderedDict()
    transcripts = OrderedDict()

    for feature in features:

        if feature.type == 'chromosome':
            feature.children = OrderedDict()
            chromosomes[feature.ID] = feature

        elif feature.type == 'gene':
            feature.children = OrderedDict()
            genes[feature.ID] = feature
            feature.parent = chromosomes[feature.seqid]
            feature.parent.children[feature.ID] = feature

        elif feature.type in ['mRNA', 'noncoding_transcript']:
            feature.children = []
            feature.parent = genes[feature.attributes['Parent']]
            feature.parent.children[feature.ID] = feature
            transcripts[feature.ID] = feature

        elif feature.type in ['five_prime_UTR', 'three_prime_UTR', 'exon']:
            feature.parent = transcripts[feature.attributes['Parent']]
            feature.parent.children.append(feature)

        elif feature.type == 'CDS':
            feature.parent = transcripts[feature.attributes['Parent'][0]]
            feature.parent.children.append(feature)

        elif feature.type == 'protein':
            feature.parent = transcripts[feature.attributes['Derives_from']]
            feature.parent.children.append(feature)

    return chromosomes, genes, transcripts


def filter_by_transcript_length(transcripts, minimum, maximum):

    for transcript in transcripts:
        if transcript.length < minimum or transcript.length > maximum:
            del transcript.parent.children[transcript.ID]


def filter_mRNA_by_exon_count(transcripts, minimum, maximum):

    for transcript in transcripts:
        if transcript.type == 'mRNA':
            num = len([x for x in transcript.children if x.type == 'exon'])
            if num < minimum or num > maximum:
                del transcript.parent.children[transcript.ID]


def filter_by_transcript_coverage(transcripts, counts, minimum, maximum):

    for transcript in transcripts:
        coverage = counts.coverage(transcript)
        if coverage < minimum or coverage > maximum:
            del transcript.parent.children[transcript.ID]


def filter_gene_no_children(genes):

    for gene in genes:
        if len(gene.children) == 0:
            del gene.parent.children[gene.ID]


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


def flatten_tree(chromosomes):
    flat = []
    for chromosome in chromosomes.values():
        flat.append(chromosome)
        for gene in chromosome.children.values():
            flat.append(gene)
            for transcript in gene.children.values():
                flat.append(transcript)
                for part in transcript.children:
                    flat.append(part)
    return flat
                    
    
if __name__ == '__main__':
    args = parser.parse_args()

    chromosomes, genes, transcripts = build_tree(Feature.from_file(args.gff))

    filter_by_transcript_length(transcripts.values(), args.min_length, args.max_length)
    filter_mRNA_by_exon_count(transcripts.values(), args.min_exons, args.max_exons)
    filter_gene_no_children(genes.values())

    if args.counts:
        counts = Counts.from_file(args.counts)
        filter_by_transcript_coverage(transcripts.values(), counts, 
                                      args.min_coverage, args.max_coverage)

    flat = flatten_tree(chromosomes)
    print '\n'.join([str(f) for f in flat])
