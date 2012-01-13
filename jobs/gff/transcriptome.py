from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

from base import GFFJob


class Transcriptome(GFFJob):

    """
    """

    def configure_options(self):
        """Define command-line options."""

        super(Transcriptome, self).configure_options()
        #TODO genome fasta file path
        # how best to distribute this file to workers?
        # will this error if not passed?
        # TODO need to use add_file_option
        self.add_passthrough_option('--genome')

    def mapper(self, key, value):
        """TODO"""

        f = self.parse_line(value)
        if f.type == 'exon':
            yield f.attributes['Parent'], f

    def reducer_init(self):
        self.genome = {}
        for record in SeqIO.parse(genome_path, 'fasta'):
            self.genome[record.id] = record

    def reducer(self, mRNA_ID, exons):
        """TODO"""

        seq = Seq('')
        for exon in sorted(exons, key=lambda f: f.start):
            seq += self.genome[exon.seqid].seq[exon.start - 1:exon.end]

        yield None, SeqRecord(id=mRNA_ID, seq=seq).format('fasta')


if __name__ == '__main__':
    Transcriptome.run()
