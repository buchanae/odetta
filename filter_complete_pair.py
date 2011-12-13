from mrjob.job import MRJob

from alignment import ID_base, parse_SAM


class FilterCompletePair(MRJob):

    """
    TODO
    """

    def configure_options(self):
        """
        TODO
        """
        super(FilterCompletePair, self).configure_options()
        # TODO
        self.add_passthrough_option('--invert')

    def mapper(self, key, line):
        """
        TODO
        """
        a = parse_SAM(line)
        yield ID_base(a['ID']), a

    def reducer(self, ID_base, alignments):
        """
        TODO
        """
        alignments = list(alignments)
        IDs = set()

        for a in alignments:
            IDs.add(a['ID'])

        if len(IDs) == 1:
            for a in alignments:
                yield a['ID'], a


if __name__ == '__main__':
    FilterCompletePair.run()
