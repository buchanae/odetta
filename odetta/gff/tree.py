from collections import OrderedDict


def build_tree(features, safe=False):
    chromosomes = OrderedDict()
    genes = OrderedDict()
    transcripts = OrderedDict()

    for feature in features:

        if feature.type == 'chromosome':
            feature.children = OrderedDict()
            chromosomes[feature.ID] = feature

        elif feature.type == 'gene':
            feature.children = OrderedDict()
            genes[feature.ID] = feature

            try:
                feature.parent = chromosomes[feature.seqid]
                feature.parent.children[feature.ID] = feature
            except KeyError:
                if safe:
                    pass
                else:
                    raise

        elif feature.type in ['mRNA', 'noncoding_transcript']:
            feature.children = []
            transcripts[feature.ID] = feature

            try:
                feature.parent = genes[feature.attributes['Parent']]
                feature.parent.children[feature.ID] = feature
            except KeyError:
                if safe:
                    pass
                else:
                    raise

        elif feature.type in ['five_prime_UTR', 'three_prime_UTR', 'exon']:
            try:
                feature.parent = transcripts[feature.attributes['Parent']]
                feature.parent.children.append(feature)
            except KeyError:
                if safe:
                    pass
                else:
                    raise

        elif feature.type == 'CDS':
            try:
                feature.parent = transcripts[feature.attributes['Parent'][0]]
                feature.parent.children.append(feature)
            except KeyError:
                if safe:
                    pass
                else:
                    raise

        elif feature.type == 'protein':
            try:
                feature.parent = transcripts[feature.attributes['Derives_from']]
                feature.parent.children.append(feature)
            except KeyError:
                if safe:
                    pass
                else:
                    raise

    return chromosomes, genes, transcripts


def flatten_tree(chromosomes):
    flat = []
    for chromosome in chromosomes.values():
        flat.append(chromosome)
        for gene in chromosome.children.values():
            flat.append(gene)
            for transcript in gene.children.values():
                flat.append(transcript)
                for part in transcript.children:
                    flat.append(part)
    return flat
