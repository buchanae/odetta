from collections import Counter
import math

from mrjob.job import MRJob
from mrjob.protocol import JSONProtocol


class PairJob(MRJob):
    """TODO"""

    INPUT_PROTOCOL = JSONProtocol


class DistanceStatistics(PairJob):

    """
    Calculate statistics on the distance between paired alignments.

    Calculates the mean and standard deviation.
    """

    # necessary for aggregating one set of statistics.
    JOBCONF = {'mapreduce.job.reduces': '1'}

    def reducer_init(self):
        self.mean = 0.0
        self.ssr = 0.0
        self.n = 0.0

    def reducer(self, key, pair):
        """Calculate running statistics for each alignment pair."""

        d = distance_between(x, y)
        self.n += 1
        tmp = self.mean + ((d - self.mean) / self.n)
        self.ssr += (d - self.mean) * (d - tmp)
        self.mean = tmp

    def reducer_final(self):
        """Emit statistics."""
        
        var = self.ssr / self.n
        std = math.sqrt(var)
        yield None, (self.mean, std)


class ReferenceCounts(PairJob):

    """
    TODO
    """

    def mapper(self, key, pair):
        """
        TODO
        """
        yield pair[0]['reference'], pair

    def reducer(self, reference, pairs):
        """
        TODO
        """
        c = Counter()

        for x, y in pairs:
            k = x['type'] + '-' + y['type']
            c[k] += 1

        yield reference, (sum(c.values()), c)


class ValidFilter(PairJob):

    """
    Filter alignment pairs on a set of criteria including distance, strand, etc.

    --min-distance and --max-distance command-line options configure allowed distance.
    By default, any distance is allowed.
    """

    def configure_options(self):
        """Define command-line options."""

        super(ValidFilter, self).configure_options()
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
        if x['reference'] == y['reference'] and x['strand'] != y['strand']:

            d = distance_between(x, y)
            if d >= self.options.min_distance and d <= self.options.max_distance:

                yield key, pair


class UnambiguousFilter(PairJob):

    """
    TODO
    """

    def configure_options(self):
        """Define command-line options."""

        super(AmbiguousFilter, self).configure_options()
        self.add_passthrough_option('--invert', action='store_true', help="TODO.")

    def mapper(self, key, pair):
        """
        TODO
        """

        yield sorted((pair[0]['ID'], pair[1]['ID'])), pair

    def reducer(self, key, pairs):
        """
        TODO
        """

        refs = set()
        pairs = list(pairs)

        for pair in pairs:
            refs.add(pair[0]['reference'])
            refs.add(pair[1]['reference'])

        if (self.options.invert and len(refs) == 1) or \
           (not self.options.invert and len(refs) > 1):

            for p in pairs:
                yield None, p


class Combiner(PairJob):

    """
    TODO update

    For example, given...

      A = Foo\1
      B = Foo\2
      C = Bar\1

    ...A + B make a complete pair.  C is an incomplete pair.
    """

    def mapper(self, key, alignment):
        """Use alignment ID base as key, for grouping."""

        yield ID_base(alignment['ID']), alignment

    def reducer(self, key, alignments):
        """Filter and emit valid alignments individually."""

        for x, y in combinations(alignments, 2):
            if x['ID'] != y['ID']:
                yield None, (x, y)
