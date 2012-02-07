from collections import defaultdict


def transcript_splice_junctions(features):
    """
    Given features, return a dict describing the positions of splice junctions
    within each transcript.

    Each splice junction position is relative to the transcript start.
    """

    transcript_exons = defaultdict(list)

    for f in features:
        if f.type == 'exon':
            for p in f.parents:
                transcript_exons[p].append(f)

    junctions = {}
    for ID, exons in transcript_exons.items():

        start = 0
        junctions[ID] = []

        for e in sorted(exons, key=lambda e: e.start)[:-1]:
            start += e.length
            junctions[ID].append(start)

    return junctions
