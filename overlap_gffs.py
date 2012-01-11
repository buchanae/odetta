import argparse

import rtree

import gff

#TODO convert to mrjob?
#TODO figure out how to install libspatialindex on pseudo nodes

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="TODO.")

    parser.add_argument('gffa', metavar='A.gff',
        help='query')

    parser.add_argument('gffb', metavar='B.gff',
        help='reference')

    args = parser.parse_args()

    idx = rtree.index.Index()

    print 'building tree'
    for i, f in enumerate(gff.reader(args.gffa)):
        
        if f.type == 'mRNA':
            # TODO crappy GFF entry, and rtree doesn't handle this well either
            if f.end > f.start:
                idx.insert(i, (f.start, 0, f.end, 0))

    print 'querying tree'
    for i, f in enumerate(gff.reader(args.gffb)):
        try:
            f = gff.Feature.from_string(line)
        except gff.InvalidGFFString:
            pass

        if f.type == 'mRNA':
            #TODO useful output
            print f, list(idx.intersection((f.start, 0, f.end, 0)))
