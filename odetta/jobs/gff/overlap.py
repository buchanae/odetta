from itertools import ifilter

from mrjob.job import MRJob
from mrjob.protocol import RawValueProtocol
#TODO maybe make rtree optional and fall back on pyrtree?
import rtree

from odetta.gff.feature import Feature


def calc_overlap(a, b):
    """TODO"""

    if b.end < a.start or b.start > a.end: return 0
    start = a.start if a.start > b.start else b.start
    end = a.end if a.end < b.end else b.end
    return (end - start + 1) / b.length


class Overlap(MRJob):

    """TODO"""

    OUTPUT_PROTOCOL = RawValueProtocol

    def configure_options(self):
        """Define command-line options."""

        super(Overlap, self).configure_options()
        # TODO check that file can be opened

        # TODO self.add_file_option('--rtree', help='TODO')

        self.add_file_option('--reference', help='TODO')

        #TODO unit tests for these options
        self.add_passthrough_option('--min-overlap', type=float, default=float('-inf'),
            help='TODO')
        self.add_passthrough_option('--max-overlap', type=float, default=float('inf'),
            help='TODO')

        self.add_passthrough_option('--min-overlap-count', type=float, 
            default=float('-inf'), help='TODO')
        self.add_passthrough_option('--max-overlap-count', type=float, 
            default=float('inf'), help='TODO')


    def mapper_init(self):
        """TODO"""

        self.refs = []
        r = ifilter(lambda x: x.type == 'mRNA', Feature.from_file(self.options.reference))
        def generator_function():
            for i, f in enumerate(r):
                if f.type == 'mRNA':

                    try:
                        ref_i = self.refs.index(f.seqid)
                    except ValueError:
                        ref_i = len(self.refs)
                        self.refs.append(f.seqid)

                    yield (i, (f.start, ref_i, f.end, ref_i), f)

        self.rtree = rtree.index.Index(generator_function())


    def search(self, f):
        """TODO"""

        try:
            ref_i = self.refs.index(f.seqid)
        except ValueError:
            return []

        o = self.rtree.intersection((f.start, ref_i, f.end, ref_i), objects=True)
        return [n.object for n in o]


    def mapper(self, key, line):
        """TODO"""

        try:
            f = Feature.from_string(line)

            if f.type == 'mRNA':
                overlaps = self.search(f)

                if len(overlaps) >= self.options.min_overlap_count and \
                   len(overlaps) <= self.options.max_overlap_count: 

                    for o in overlaps:
                        amt = calc_overlap(o, f)
                        if amt >= self.options.min_overlap and \
                           amt <= self.options.max_overlap:

                            f.attributes['Parent'] = o.ID
                            yield None, f

        except Feature.ParseError:
            pass



if __name__ == '__main__':
    Overlap.run()
