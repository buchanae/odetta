from mrjob.job import MRJob
from mrjob.protocol import PickleProtocol, RawValueProtocol
from pyfasta import Fasta

from feature import Feature


def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]


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

            if f.type == 'exon':
                for parent in f.parents:
                    yield parent, f

        except Feature.ParseError:
            pass

    def reducer_init(self):
        self.genome = Fasta(self.options.genome)

    def reducer(self, mRNA_ID, exons):
        """TODO"""

        seq = ''
        for exon in sorted(exons, key=lambda f: f.start):
            seq += self.genome[exon.seqid][exon.start - 1:exon.end]

        header = '>{}'.format(mRNA_ID)
        yield None, '\n'.join([header] + list(chunks(seq, 70)))


if __name__ == '__main__':
    Transcriptome.run()
