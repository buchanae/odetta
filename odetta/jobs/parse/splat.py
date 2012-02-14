from mrjob.job import MRJob

from odetta.utils import model_parser

splat_model = model_parser([
    ('reference', ''),
    ('flanks', ''),
    ('a_length', 0),
    ('b_length', 0),
    ('intron_length', 0),
    ('a_start', 0),
    ('a_end', 0),
    ('b_start', 0),
    ('b_end', 0),
    ('sequence', ''),
    ('read_count', 0),
    ('read_IDs', ''),
])

class Splat(MRJob):

    """
    Parse a Splat formatted line.
    """

    def parse_line(self, line):

        data = splat_model(line.split('\t'))

        if data['a_start'] <= data['b_start']:
            data['start'] = data['a_start']
            data['end'] = data['b_end']
        else:
            data['start'] = data['b_start']
            data['end'] = data['a_end']

        data['type'] = 'splat'

        return data

    def mapper(self, key, value):
        yield None, self.parse_line(value)


if __name__ == '__main__':
    Splat.run()
