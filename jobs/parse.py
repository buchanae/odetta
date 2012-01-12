import mrjob


class Sam(mrjob.job.MRJob):

    """
    TODO
    """

    def configure_options(self):
        """Define command-line options."""

        super(Sam, self).configure_options()
        self.add_passthrough_option('--type', action='store', type=string, default='SAM',
            help="TODO.")

    def mapper(self, key, line):
        """Parse a SAM formatted string."""

        data = {}
        fields = line.split('\t')

        flag = int(fields[1])
        sequence = fields[9]

        data['ID'] = fields[0]
        data['reference'] = fields[2]
        data['start'] = int(fields[3])
        data['end'] = data['start'] + len(sequence)

        # The SAM format stores strand info in a bitwise flag,
        # not obscure at all...
        data['strand'] = '-1' if flag & 16 else '1'
        data['type'] = self.options.type

        yield None, data


class Splat(mrjob.job.MRJob):

    """
    TODO update
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


class SplitSplat(Splat):

    """
    TODO update
    """

    def mapper(self, key, line):
        """TODO"""

        key, splat = super(SplitSplat, self).mapper(key, line)

        IDs = splat['read_IDs'].split(',')

        del splat['read_count']
        del splat['read_IDs']

        for ID in IDs:
            splat['ID'] = ID
            yield key, splat
