from mrjob.job import MRJob
from mrjob.protocol import JSONProtocol


class UnambiguousFilter(MRJob):

    """
    TODO
    """

    INPUT_PROTOCOL = JSONProtocol

    def configure_options(self):
        """Define command-line options."""

        super(UnambiguousFilter, self).configure_options()
        self.add_passthrough_option('--invert', action='store_true', help="TODO.")

    def mapper(self, key, pair):
        """
        TODO
        """

        yield sorted([pair[0]['ID'], pair[1]['ID']]), pair

    def reducer(self, key, pairs):
        """
        TODO
        """

        refs = set()
        pairs = list(pairs)

        for pair in pairs:
            refs.add(pair[0]['reference'])
            refs.add(pair[1]['reference'])

        if (self.options.invert and len(refs) > 1) or \
           (not self.options.invert and len(refs) == 1):

            for p in pairs:
                yield None, p


if __name__ == '__main__':
    UnambiguousFilter.run()
