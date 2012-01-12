"""
TODO update
Reads JSON data and emits Splat strings.
"""

import mrjob


splat_template = '{reference}\t{flanks}\t{a_length}\t{b_length}\t{intron_length}\t{a_start}\t{a_end}\t{b_start}\t{b_end}\t{sequence}\t{{read_count}}\t{{read_count}}\t{{read_IDs}}\t{strand}'


class SplatFormat(mrjob.job.MRJob):

    """
    TODO update

    """

    INPUT_PROTOCOL = mrjob.protocol.JSONProtocol
    OUTPUT_PROTOCOL = mrjob.protocol.RawValueProtocol

    def mapper(self, key, pair):
        """TODO"""

        for x in pair:
            if x['type'] == 'splat':
                yield splat_template.format(x), x['ID']


    def reducer(self, splat, IDs):
        """Combine and emit Splat strings."""

        IDs = list(IDs)
        yield None, splat.format(read_count=len(IDs), read_IDs=','.join(IDs))
