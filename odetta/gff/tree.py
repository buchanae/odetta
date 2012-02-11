from collections import OrderedDict


def build_tree(features):
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
            feature.parent = chromosomes[feature.seqid]
            feature.parent.children[feature.ID] = feature

        elif feature.type in ['mRNA', 'noncoding_transcript']:
            feature.children = []
            feature.parent = genes[feature.attributes['Parent']]
            feature.parent.children[feature.ID] = feature
            transcripts[feature.ID] = feature

        elif feature.type in ['five_prime_UTR', 'three_prime_UTR', 'exon']:
            feature.parent = transcripts[feature.attributes['Parent']]
            feature.parent.children.append(feature)

        elif feature.type == 'CDS':
            feature.parent = transcripts[feature.attributes['Parent'][0]]
            feature.parent.children.append(feature)

        elif feature.type == 'protein':
            feature.parent = transcripts[feature.attributes['Derives_from']]
            feature.parent.children.append(feature)

    return chromosomes, genes, transcripts
