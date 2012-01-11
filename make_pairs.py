from itertools import combinations

from mrjob.job import MRJob

from alignment import ID_base


class MakePairs(MRJob):

    """
    TODO update

    For example, given...

      A = Foo\1
      B = Foo\2
      C = Bar\1

    ...A + B make a complete pair.  C is an incomplete pair.
    """

    def mapper(self, key, alignment):
        """Use alignment ID base as key, for grouping."""

        yield ID_base(alignment['ID']), alignment

    def reducer(self, ID_base, alignments):
        """Filter and emit valid alignments individually."""

        for x, y in combinations(alignments, 2):
            if x['ID'] != y['ID']:
                yield None, (x, y)


if __name__ == '__main__':
    MakePairs.run()
