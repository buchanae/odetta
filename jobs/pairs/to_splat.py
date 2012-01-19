"""
TODO update
Reads JSON pair data and emits Splat strings.
"""

from mrjob.job import MRJob
from mrjob.protocol import JSONProtocol, RawValueProtocol


splat_template = '{reference}\t{flanks}\t{a_length}\t{b_length}\t{intron_length}\t{a_start}\t{a_end}\t{b_start}\t{b_end}\t{sequence}\t{{read_count}}\t{{read_IDs}}\t{strand}'


class ToSplat(MRJob):

    """
    TODO update
    """

    INPUT_PROTOCOL = JSONProtocol
    OUTPUT_PROTOCOL = RawValueProtocol

    def mapper(self, key, pair):
        """TODO"""

        for x in pair:
            if x['type'] == 'splat':
                yield splat_template.format(**x), x['ID']


    def reducer(self, splat_partial, IDs):
        """Combine and emit Splat strings."""

        IDs = list(IDs)
        yield None, splat_partial.format(read_count=len(IDs), read_IDs=','.join(IDs))


if __name__ == '__main__':
    ToSplat.run()
