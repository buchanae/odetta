from mrjob.job import MRJob
from mrjob.protocol import JSONProtocol

from odetta.utils import distance_between


class DistanceFilter(MRJob):

    """
    Filter alignment pairs on a set of criteria including distance, strand, etc.

    --min-distance and --max-distance command-line options configure allowed distance.
    By default, any distance is allowed.
    """

    INPUT_PROTOCOL = JSONProtocol

    def configure_options(self):
        """Define command-line options."""

        super(DistanceFilter, self).configure_options()
        self.add_passthrough_option('--min-distance', action='store',
                                    type=float, default=float('-inf'))
        self.add_passthrough_option('--max-distance', action='store',
                                    type=float, default=float('inf'))

    def mapper(self, key, pair):
        """
        Valid pairs must have...
          - the same reference
          - opposite strands
          - a distance between them within the given bounds
        """

        x, y = pair
        d = distance_between(x, y)
        if d >= self.options.min_distance and d <= self.options.max_distance:
            yield key, pair


if __name__ == '__main__':
    DistanceFilter.run()
