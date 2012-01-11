from mrjob.job import MRJob


class ParseSplat(MRJob):

    """
    TODO update
    Split Splat records into multiple records with one read per record.

    Splat records contain multiple read IDs i.e. one-to-many.
    We need to work with read IDs individually i.e. one-to-one.
    This converts one-to-many -> one-to-one.

    For example, given...

      SplatDataA, Read1,Read2,Read3

    ...this will emit...
      Read1 SplatDataA
      Read2 SplatDataA
      Read3 SplatDataA
    """

    def mapper(self, key, line):
        """Parse a Splat formatted string."""

        fields = ('reference', 'flanks', 'a_length', 'b_length', 'intron_length',
                  'a_start', 'a_end', 'b_start', 'b_end', 'sequence', 'read_count',
                  'read_IDs', 'strand')

        ints = ('a_length', 'b_length', 'intron_length', 'a_start', 'a_end', 'b_start',
                'b_end', 'read_count')
                  
        data = {}
        for key, value = zip(fields, line.split('\t')):
            data[key] = value

        for key in ints:
            data[key] = int(data[key])

        if data['a_start'] < data['b_start']:
            data['start'] = data['a_start']
            data['end'] = data['b_end']
        else:
            data['start'] = data['b_start']
            data['end'] = data['a_end']

        data['type'] = 'splat'

        yield None, data


if __name__ == '__main__':
    ParseSplat.run()
