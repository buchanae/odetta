from mrjob.job import MRJob


class ParseSam(MRJob):

    """
    """

    def configure_options(self):
        """Define command-line options."""

        super(FilterInvalidPair, self).configure_options()
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


if __name__ == '__main__':
    ParseSam.run()
