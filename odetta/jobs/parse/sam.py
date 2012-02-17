from mrjob.job import MRJob

from odetta.utils import model_parser


sam_model = model_parser([
    ('ID', ''),
    ('flag', 0),
    ('reference', ''),
    ('start', 0),
    ('map_quality', 0),
    ('CIGAR', ''),
    ('rnext', ''),
    ('pnext', ''),
    ('tlen', ''),
    ('sequence', ''),
    ('quality', ''),
])


class SAM(MRJob):

    """
    Parse a SAM formatted file.

    http://samtools.sourceforge.net/samtools.shtml#5
    """

    def configure_options(self):
        """Define command-line options."""

        super(SAM, self).configure_options()
        self.add_passthrough_option('--type', default='SAM', 
            help="set the 'type' attribute")

    def mapper(self, key, line):

        if line[0] == '@': return

        data = sam_model(line.split('\t'))

        data['end'] = data['start'] + len(data['sequence'])

        # The SAM format stores strand info in a bitwise flag,
        # not obscure at all...
        data['strand'] = '-' if data['flag'] & 16 else '+'
        data['type'] = self.options.type

        yield None, data


if __name__ == '__main__':
    SAM.run()
