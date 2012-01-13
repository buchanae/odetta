import gff
from mrjob.job import MRJob
from mrjob.protocol import RawValueProtocol


class GFFJob(MRJob):

    OUTPUT_PROTOCOL = RawValueProtocol

    def parse_line(self, line):
        """Parse a GFF formatted line."""

        try:
            return gff.Feature.from_string(line)
        except gff.InvalidGFFString:
            pass
