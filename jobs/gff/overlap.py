#TODO maybe make rtree optional and fall back on pyrtree?
import rtree

from base import GFFJob


class Overlap(GFFJob):
    """TODO"""

    # TODO not easy to distribute because every job needs a complete reference tree,
    # which could be costly to build.  can build once and distibute to all?
    # maybe could prebuilt, serialized rtree?
    JOBCONF = {'mapreduce.job.maps': '1'}

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

        f = self.parse_line(value)

        if f.type == 'mRNA':
            #TODO useful output
            #TODO calculate amount of overlap and allow filtering on that
            #[n.object for n in idx.intersection((left, bottom, right, top), objects=True)]
            yield f, list(self.idx.intersection((f.start, 0, f.end, 0)))


if __name__ == '__main__':
    Overlap.run()
