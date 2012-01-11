from mrjob.job import MRJob
from mrjob.protocol import JSONProtocol, RawValueProtocol


template = '{reference}\t{flanks}\t{a_length}\t{b_length}\t{intron_length}\t{a_start}\t{a_end}\t{b_start}\t{b_end}\t{sequence}\t{{read_count}}\t{{read_count}}\t{{read_IDs}}\t{strand}'

class PairsToSplats(MRJob):

    """
    TODO update
    Combine Splat alignments.  The opposite of SplitSplat.

    Reads JSON data and emits Splat strings.
    """

    INPUT_PROTOCOL = JSONProtocol
    OUTPUT_PROTOCOL = RawValueProtocol

    def mapper(self, key, pair):

        for x in pair:
            if x['type'] == 'splat':
                yield template.format(x), x['ID']


    def reducer(self, splat, IDs):
        """Combine and emit Splat strings."""

        IDs = list(IDs)
        yield None, splat.format(read_count=len(IDs), read_IDs=','.join(IDs))


if __name__ == '__main__':
    PairsToSplats.run()
