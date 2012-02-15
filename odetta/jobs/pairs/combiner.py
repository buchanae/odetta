from itertools import combinations

from mrjob.job import MRJob
from mrjob.protocol import JSONProtocol

from odetta.jobs.pairs.unambiguous_filter import UnambiguousFilter
from odetta.utils import pair_key


class Combiner(MRJob):

    """
    TODO update
    """

    INPUT_PROTOCOL = JSONProtocol

    def configure_options(self):
        """Define command-line options."""

        super(Combiner, self).configure_options()

        self.add_passthrough_option('--unambiguous-only', action='store_true', 
                                    help="TODO.")

    def mapper(self, key, alignment):
        """Use alignment ID base as key, for grouping."""

        yield pair_key(alignment['ID']), alignment

    def reducer(self, key, alignments):
        """Filter and emit valid alignments individually."""

        valid = []

        for x, y in combinations(alignments, 2):
            if x['ID'] != y['ID'] and \
               x['reference'] == y['reference'] and \
               x['strand'] != y['strand']:

                valid.append((x, y))

        if self.options.unambiguous_only:
            for key, pair in UnambiguousFilter().reducer(key, valid):
                yield None, pair
        else:
            for pair in valid:
                yield None, pair


if __name__ == '__main__':
    Combiner.run()
