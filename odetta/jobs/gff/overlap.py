import argparse

#TODO maybe make rtree optional and fall back on pyrtree?
import rtree

from odetta.gff.feature import Feature
from odetta.gff.tree import build_tree, flatten_tree


# TODO check that file can be opened

# TODO self.add_file_option('--rtree', help='TODO')

parser = argparse.ArgumentParser(description='TODO')
parser.add_argument('reference', help='TODO')
parser.add_argument('gff')

#TODO unit tests for these options
parser.add_argument('--min-overlap', type=float, default=float('-inf'),help='TODO')
parser.add_argument('--max-overlap', type=float, default=float('inf'), help='TODO')

parser.add_argument('--min-overlap-count', type=float, default=float('-inf'), help='TODO')
parser.add_argument('--max-overlap-count', type=float, default=float('inf'), help='TODO')


class PositionDatabase(object):
    def __init__(self, features):
        self.refs = []

        def generator_function():
            for i, f in enumerate(features):
                try:
                    ref_i = self.refs.index(f.seqid)
                except ValueError:
                    ref_i = len(self.refs)
                    self.refs.append(f.seqid)

                yield (i, (f.start, ref_i, f.end, ref_i), f)

        self.rtree = rtree.index.Index(generator_function())

    def overlaps(self, f):
        """TODO"""

        try:
            ref_i = self.refs.index(f.seqid)
        except ValueError:
            return []

        o = self.rtree.intersection((f.start, ref_i, f.end, ref_i), objects=True)
        return [n.object for n in o if n.object.type == f.type]


def calc_overlap(a, b):
    """TODO"""

    if b.end < a.start or b.start > a.end: return 0
    start = a.start if a.start > b.start else b.start
    end = a.end if a.end < b.end else b.end
    return (end - start + 1) / b.length


def overlap(db, feature):
    overlaps = db.overlaps(feature)

    if len(overlaps) >= args.min_overlap_count and \
       len(overlaps) <= args.max_overlap_count: 

        valid = []
        for o in overlaps:
            amt = calc_overlap(o, feature)
            if amt >= args.min_overlap and amt <= args.max_overlap:
                valid.append(o.ID)

        if len(valid) > 0:
            feature.attributes['overlaps'] = ','.join(valid)


if __name__ == '__main__':
    args = parser.parse_args()

    db = PositionDatabase(Feature.from_file(args.reference))
    chromosomes, genes, transcripts = build_tree(Feature.from_file(args.gff))

    for t in transcripts.values():
        overlap(db, t)

    flat = flatten_tree(chromosomes)
    print '\n'.join([str(f) for f in flat])
