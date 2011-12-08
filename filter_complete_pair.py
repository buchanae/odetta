from mrjob.job import MRJob

from alignment import Alignment


class FilterCompletePair(MRJob):

    """
    TODO
    """

    DEFAULT_PROTOCOL = 'pickle'
    DEFAULT_OUTPUT_PROTOCOL = 'raw_value'

    def configure_options(self):
        """
        TODO
        """
        super(FilterCompletePair, self).configure_option()
        # TODO
        self.add_passthrough_option('--invert')

    def mapper(self, key, line):
        """
        TODO
        """
        a = Alignment.from_SAM(line)       
        yield a.base_id, a

    def reducer(self, base_id, alignments):
        """
        TODO
        """
        ids = set()

        for a in alignments:
            ids.add(a.pair_id)

        if len(ids) == 1:
            for a in alignments:
                # TODO can yield only key or value and not both?
                yield a


if __name__ == '__main__':
    FilterCompletePair.run()
