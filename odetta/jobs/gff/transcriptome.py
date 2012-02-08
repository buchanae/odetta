import string

from mrjob.job import MRJob
from mrjob.protocol import PickleProtocol, RawValueProtocol
from pyfasta import Fasta

from feature import Feature


complements = string.maketrans('ATCGN', 'TAGCN')


def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]


def reverse_complement(seq):
    return seq.translate(complements)[::-1]
    


class Transcriptome(MRJob):

    """TODO"""

    INTERNAL_PROTOCOL = PickleProtocol
    OUTPUT_PROTOCOL = RawValueProtocol

    def configure_options(self):
        """Define command-line options."""

        super(Transcriptome, self).configure_options()
        #TODO will this error if not passed?
        self.add_file_option('--genome', help='TODO')

    def mapper(self, key, line):
        """TODO"""

        try:
            f = Feature.from_string(line)

            if f.type == 'exon' or f.type == 'noncoding_transcript':
                for parent in f.parents:
                    yield (parent, f.type), f

        except Feature.ParseError:
            pass

    def reducer_init(self):
        self.genome = Fasta(self.options.genome)

    def reducer(self, (ID, feature_type), features):
        """TODO"""

        def genome_seq(feature):
            seq = self.genome[feature.seqid][feature.start - 1:feature.end]
            if feature.strand == '-':
                return reverse_complement(seq)
            else:
                return seq

        def yield_seq(seq):
            header = '>{}'.format(ID)
            yield None, '\n'.join([header] + list(chunks(seq, 70)))

        seq = ''
        if feature_type == 'noncoding_transcript':
            for feature in features:
                yield_seq(genome_seq(feature))
        else:
            reverse = features[0].strand == '-'
            for exon in sorted(features, key=lambda f: f.start, reverse=reverse):
                seq += genome_seq(exon)

            yield_seq(seq)


if __name__ == '__main__':
    Transcriptome.run()
