import argparse
from collections import Counter, defaultdict
import json
import math

from feature import Feature


def calc_coverage(hits, total, length):
    # coverage is RPKM, reads per kilobase of reference per million mapped reads
    # http://www.clcbio.com/manual/genomics/Definition_RPKM.html
    return (math.pow(10, 9) * hits) / (total * length)


parser = argparse.ArgumentParser(description='TODO')
#TODO need a way of gracefully failing if counts isn't passed
# maybe positional arguments can work in mrjob?
parser.add_argument('gff')
parser.add_argument('--counts', help='TODO')

parser.add_argument('--min-length', type=float, default=float('-inf'),
    help='TODO')
parser.add_argument('--max-length', type=float, default=float('inf'),
    help='TODO')

parser.add_argument('--min-coverage', type=float, default=float('-inf'),
    help='TODO')
parser.add_argument('--max-coverage', type=float, default=float('inf'),
    help='TODO')

parser.add_argument('--min-exons', type=float, default=float('-inf'),
    help='TODO')
parser.add_argument('--max-exons', type=float, default=float('inf'),
    help='TODO')


def load_counts(path):
    total = 0
    counts = {}

    for line in open(path):
        ref_name, counts_json = line.strip().split('\t')
        counts = json.loads(counts_json)
        total += sum(counts.values())
        counts[ref_name] = counts

def build_tree(path):
    chromosomes = {}
    genes = {}
    mRNAs = {}

    for feature in Feature.from_file(path):

        if feature.type == 'chromosome':
            feature.children = {}
            chromosomes[feature.ID] = feature

        elif feature.type == 'gene':
            feature.children = {}
            genes[feature.ID] = feature
            feature.parent = chromosomes[feature.seqid]
            feature.parent.children[feature.ID] = feature

        elif feature.type in ['mRNA', 'noncoding_transcript']:
            feature.children = []
            feature.parent = genes[feature.attributes['Parent']]
            feature.parent.children[feature.ID] = feature
            if feature.type == 'mRNA':
                mRNAs[feature.ID] = feature

        elif feature.type in ['five_prime_UTR', 'CDS', 'three_prime_UTR', 'exon']:
            feature.parent = mRNAs[feature.attributes['Parent']]
            feature.parent.children.append(feature)

        elif feature.type == 'protein':
            feature.parent = mRNAs[feature.attributes['Derives_from']]
            feature.parent.children.append(feature)

    return chromosomes, genes, mRNAs


def filter_by_mRNA_length(mRNAs, minimum, maximum):
    for mRNA in mRNAs:
        if mRNA.length < minimum or mRNA.length > maximum:
            del mRNA.parent.children[mRNA.ID]


def filter_by_exon_count(mRNAs, minimum, maximum):
    for mRNA in mRNAs:
        num = len([x for x in mRNA.children if x.type == 'exon'])
        if num < minimum or num > maximum:
            del mRNA.parent.children[mRNA.ID]


def filter_gene_no_children():
    for gene in genes:
        if len(genes.children) == 0:
            del gene.parent.children[gene.ID]

if __name__ == '__main__':
    args = parser.parse_args()
