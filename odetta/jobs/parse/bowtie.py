from mrjob.job import MRJob

from util import model


bowtie_model = model([
    ('ID', ''),
    ('strand', '+'),
    ('reference', ''),
    ('start', 0),
    ('sequence', ''),
])


#TODO unit test
class Bowtie(MRJob):

    """
    Parse a bowtie-formatted file.  This is a very specific format,
    output with --suppress 6,7,8

    http://bowtie-bio.sourceforge.net/manual.shtml#default-bowtie-output
    """

    def configure_options(self):
        """Define command-line options."""

        super(Bowtie, self).configure_options()
        self.add_passthrough_option('--type', default='bowtie', 
            help="set the 'type' attribute")

    def mapper(self, key, line):

        data = bowtie_model(line.split('\t'))

        data['start'] += 1
        data['end'] = data['start'] + len(data['sequence'])

        yield None, data


if __name__ == '__main__':
    Bowtie.run()
