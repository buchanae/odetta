from mrjob.job import MRJob

from alignment import ID_base, parse_SAM


class FilterCompletePair(MRJob):

    """
    Filter alignments on whether they have a paired alignment.

    By default, keep incomplete pairs i.e. filter out complete pairs.
    --invert will do the opposite.

    For example, given...

      A = Foo\1
      B = Foo\2
      C = Bar\1

    ...A + B make a complete pair.  C is an incomplete pair.
    So C would be returned by default.  Given the --invert option,
    A and B would be returned.
    """

    def configure_options(self):
        """Define command-line options."""

        super(FilterCompletePair, self).configure_options()
        self.add_passthrough_option('--invert', action='store_true', 
            help="Invert the filter i.e. complete pairs, filter out incomplete pairs.")

    def mapper(self, key, line):
        """Parse SAM formatted line and group alignments by read ID base."""

        a = parse_SAM(line)
        yield ID_base(a['ID']), a

    def reducer(self, ID_base, alignments):
        """Filter and emit valid alignments individually."""

        alignments = list(alignments)
        IDs = set()

        for a in alignments:
            IDs.add(a['ID'])

        if (self.options.invert and len(IDs) > 1) or \
           (not self.options.invert and len(IDs) == 1):

            for a in alignments:
                yield a['ID'], a


if __name__ == '__main__':
    FilterCompletePair.run()
