import json
import math

from mrjob.job import MRJob
from mrjob.protocol import PickleProtocol, RawValueProtocol

from feature import Feature


def calc_coverage(hits, total, length):
    # coverage is RPKM, reads per kilobase of reference per million mapped reads
    # http://www.clcbio.com/manual/genomics/Definition_RPKM.html
    return (math.pow(10, 9) * hits) / (total * length)


class Filter(MRJob):

    """TODO"""

    INTERNAL_PROTOCOL = PickleProtocol
    OUTPUT_PROTOCOL = RawValueProtocol

    def configure_options(self):
        """Define command-line options."""

        super(Filter, self).configure_options()

        #TODO need a way of gracefully failing if counts isn't passed
        # maybe positional arguments can work in mrjob?
        self.add_file_option('--counts', help='TODO')

        self.add_passthrough_option('--min-length', type=float, default=float('-inf'),
            help='TODO')
        self.add_passthrough_option('--max-length', type=float, default=float('inf'),
            help='TODO')

        self.add_passthrough_option('--min-coverage', type=float, default=float('-inf'),
            help='TODO')
        self.add_passthrough_option('--max-coverage', type=float, default=float('inf'),
            help='TODO')

        self.add_passthrough_option('--min-exons', type=float, default=float('-inf'),
            help='TODO')
        self.add_passthrough_option('--max-exons', type=float, default=float('inf'),
            help='TODO')

    def mapper(self, key, line):
        """TODO"""

        try:
            f = Feature.from_string(line)

            if f.type == 'mRNA':
                yield f.ID, f

            elif f.type == 'exon':
                for parent in f.parents:
                    yield parent, f

        except Feature.ParseError:
            pass

    def reducer_init(self):
        self.total = 0
        self.counts = {}

        if self.options.counts:
            for line in open(self.options.counts):
                ref_name, counts_json = line.strip().split('\t')
                ref_total, counts = json.loads(counts_json)
                # TODO could remove total from output and calc from sum(counts.values())
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

        hits = sum(self.counts[ID].values()) if ID in self.counts else 0

        try:
            coverage = calc_coverage(hits, self.total, mRNA.length)
        except ZeroDivisionError:
            coverage = 0

        if mRNA.length >= self.options.min_length and \
           mRNA.length <= self.options.max_length and \
           exons >= self.options.min_exons and \
           exons <= self.options.max_exons and \
           coverage >= self.options.min_coverage and \
           coverage <= self.options.max_coverage:

              yield None, mRNA


if __name__ == '__main__':
    Filter.run()
