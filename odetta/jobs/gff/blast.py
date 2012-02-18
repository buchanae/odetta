import argparse
import re
import sys

from lxml import etree

from odetta.gff.feature import Feature
from odetta.gff.tree import build_tree, flatten_tree


parser = argparse.ArgumentParser()
parser.add_argument('gmb')
parser.add_argument('blast')
parser.add_argument('--max-gap-size', type=int, default=10)
parser.add_argument('--min-match', type=float, default=0.8)


if __name__ == '__main__':
    args = parser.parse_args()

    rx = re.compile(' {{max_gap}}'.format(max_gap=args.max_gap_size))
    chromosomes, genes, transcripts = build_tree(Feature.from_file(args.gmb))
    tree = etree.parse(open(args.blast))

    for x in tree.iterfind('.//Iteration'):
        ID = x.findtext('.//Iteration_query-def')
        query_len = x.findtext('.//Iteration_query-len')

        hits = x.findall('.//Hit')
        for hit in hits:
            hit_def = hit.findtext('.//Hit_def')
            hit_len = hit.findtext('.//Hit_len')
            identity = hit.findtext('.//Hsp_identity')
            align_len = hit.findtext('.//Hsp_align-len')
            if identity != align_len:
                midline = hit.findtext('.//Hsp_midline')
                gap_match = rx.search(midline)
                if gap_match:
                    continue

            p = (float(identity) / float(hit_len)) * (float(identity) / float(query_len))
            if p >= args.min_match:
                try:
                    t = transcripts[ID]
                except KeyError:
                    pass
                else:
                    try:
                        t.attributes['blasts_to'] = ','.join([t.attributes['blasts_to'],
                                                              hit_def])
                    except KeyError:
                        t.attributes['blasts_to'] = hit_def

    for f in flatten_tree(chromosomes):
        print f
