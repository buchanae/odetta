import json
import math

from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
import gff
import mrjob
#TODO maybe make rtree optional and fall back on pyrtree?
import rtree


class GFFJob(mrjob.job.MRJob):

    OUTPUT_PROTOCOL = mrjob.protocol.RawValueProtocol

    def mapper(self, key, line):
        """TODO"""

        try:
            yield key, gff.Feature.from_string(line)
        except gff.InvalidGFFString:
            pass

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
        self.add_passthrough_option('--genome', action='store', type=string)

    def mapper(self, key, value):
        """TODO"""

        key, f = super(Transcriptome, self).mapper(key, value)
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


class Filter(GFFJob):
    """TODO"""

    def configure_options(self):
        """Define command-line options."""

        super(Filter, self).configure_options()

        # TODO need to use add_file_option
        parser.add_argument('counts', help='TODO')
        parser.add_argument('--min-length', type=float, default=float('-inf'))
        parser.add_argument('--max-length', type=float, default=float('inf'))
        parser.add_argument('--min-coverage', type=float, default=float('-inf'))

    def mapper(self, key, value):
        """TODO"""

        key, f = super(Filter, self).mapper(key, value)

        if f.type == 'mRNA':
            yield f.attributes['ID'], f
        elif f.type == 'exon':
            yield f.attributes['Parent'], f

    def reducer_init(self):
        self.total = 0
        self.counts = {}

        for line in open(self.options.counts_path):
            ref_name, counts_json = line.strip().split('\t')
            ref_total, counts = json.loads(counts_json)
            self.total += ref_total
            self.counts[ref_name] = counts

    def reducer(self, ID, features):
        exons = 0
        mRNA = None

        for f in features:
            if f.type == 'exon':
                exons += 1
            else:
                mRNA = f

        # coverage is RPKM, reads per kilobase of reference per million mapped reads
        # http://www.clcbio.com/manual/genomics/Definition_RPKM.html
        hits = sum(self.counts[ID].values())
        coverage = (math.pow(10, 9) * hits) / (self.total * mRNA.length)

        if mRNA.length >= self.options.min_length and \
           mRNA.length <= self.options.max_length and \
           exons > 1 and coverage >= self.options.min_coverage:
              yield None, mRNA


 class Overlap(GFFJob):
    """TODO"""

    # TODO not easy to distribute because every job needs a complete reference tree,
    # which could be costly to build.  can build once and distibute to all?
    # maybe could prebuilt, serialized rtree?
    JOBCONF = {'mapreduce.job.maps': '1'}

    #TODO what output format?
    OUTPUT_PROTOCOL = mrjob.protocol.RawValueProtocol

    def configure_options(self):
        """Define command-line options."""

        super(Overlap, self).configure_options()
        #TODO reference gff path
        # will this error if not passed?
        # TODO check that file can be opened
        # TODO need to use add_file_option
        self.add_passthrough_option('--reference', action='store', type=string)

    def mapper_init(self):
        """TODO"""

        self.idx = rtree.index.Index()
        for i, f in enumerate(gff.reader(self.options.reference)):
            
            if f.type == 'mRNA':
                idx.insert(i, (f.start, 0, f.end, 0), obj=f)

    def mapper(self, key, value):
        """TODO"""

        key, f = super(Overlap, self).mapper(key, value)

        if f.type == 'mRNA':
            #TODO useful output
            #TODO calculate amount of overlap and allow filtering on that
            #[n.object for n in idx.intersection((left, bottom, right, top), objects=True)]
            yield f, list(self.idx.intersection((f.start, 0, f.end, 0)))
