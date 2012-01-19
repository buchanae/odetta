from itertools import combinations

from mrjob.job import MRJob
from mrjob.protocol import JSONProtocol

from utils import ID_base


class Combiner(MRJob):

    """
    TODO update
    """

    INPUT_PROTOCOL = JSONProtocol

    def mapper(self, key, alignment):
        """Use alignment ID base as key, for grouping."""

        yield ID_base(alignment['ID']), alignment

    def reducer(self, key, alignments):
        """Filter and emit valid alignments individually."""

        for x, y in combinations(alignments, 2):
            if x['ID'] != y['ID']:
                yield None, (x, y)


if __name__ == '__main__':
    Combiner.run()
