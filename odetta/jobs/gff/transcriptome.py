import argparse
import string

from pyfasta import Fasta

from odetta.gff.feature import Feature
from odetta.gff.tree import build_tree


parser = argparse.ArgumentParser(description='TODO')
parser.add_argument('genome', help='TODO')
parser.add_argument('gff')

complements = string.maketrans('ATCGN', 'TAGCN')


def reverse_complement(seq):
    return seq.translate(complements)[::-1]


def genome_seq(genome, feature):
    seq = genome[feature.seqid][feature.start - 1:feature.end]
    if feature.strand == '-':
        return reverse_complement(seq)
    else:
        return seq


def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]


def fasta_rec(ID, seq):
    header = '>{}'.format(ID)
    return '\n'.join([header] + list(chunks(seq, 70)))


if __name__ == '__main__':
    args = parser.parse_args()

    genome = Fasta(args.genome)
    chromosomes, genes, transcripts = build_tree(Feature.from_file(args.gff))

    for transcript in transcripts.values():
        exons = [x for x in transcript.children if x.type == 'exon']

        # handle an ugly GFF case: a transcript might not have exons explicitly defined,
        # so we're assuming it's implied
        # TODO this would fit better in a "clean GFF" script
        if len(exons) == 0:
            exons = [transcript]

        reverse = transcript.strand == '-'

        seq = ''
        for exon in sorted(exons, key=lambda e: e.start, reverse=reverse):
            seq += genome_seq(genome, exon)

        print fasta_rec(transcript.ID, seq)
