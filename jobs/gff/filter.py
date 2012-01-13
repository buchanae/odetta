import json
import math

from mrjob.protocol import PickleProtocol

from base import GFFJob


class Filter(GFFJob):

    """TODO"""

    INTERNAL_PROTOCOL = PickleProtocol

    def configure_options(self):
        """Define command-line options."""

        super(Filter, self).configure_options()

        # START here, get add_file_option to work
        # TODO need to use add_file_option
        #self.add_file_option('counts', help='TODO')
        self.add_passthrough_option('--min-length', type=float, default=float('-inf'),
            help='TODO')
        self.add_passthrough_option('--max-length', type=float, default=float('inf'),
            help='TODO')
        self.add_passthrough_option('--min-coverage', type=float, default=float('-inf'),
            help='TODO')

    def mapper(self, key, value):
        """TODO"""

        f = self.parse_line(value)

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


if __name__ == '__main__':
    Filter.run()
