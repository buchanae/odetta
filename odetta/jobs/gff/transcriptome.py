from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from mrjob.job import MRJob
from mrjob.protocol import PickleProtocol, RawValueProtocol

from feature import Feature


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
        self.genome = {}
        for record in SeqIO.parse(self.options.genome, 'fasta'):
            self.genome[record.id] = record

    def reducer(self, mRNA_ID, exons):
        """TODO"""

        seq = Seq('')
        for exon in sorted(exons, key=lambda f: f.start):
            seq += self.genome[exon.seqid].seq[exon.start - 1:exon.end]

        yield None, SeqRecord(id=mRNA_ID, seq=seq, description='').format('fasta')


if __name__ == '__main__':
    Transcriptome.run()
