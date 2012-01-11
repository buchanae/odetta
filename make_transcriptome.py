from collections import defaultdict

from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

import gff


gff_path = 'a.gff'
genome_path = 'genome.fas'
out_fh = open('transcriptome.fas', 'w')


mrnas = defaultdict(lambda: defaultdict(list))
for line in gff.reader(gff_path):
    try:
        f = gff.Feature.from_string(line)
        if f.type == 'exon':
            mrnas[f.seqid][f.attributes['Parent']].append(f)

    except gff.InvalidGFFString: pass


for record in SeqIO.parse(genome_path, 'fasta'):
    for mrna_id, exons in mrnas[record.id].items():
        seq = Seq('')

        for exon in exons:
            seq += record.seq[exon.start - 1:exon.end]

        rec = SeqRecord(id=mrna_id, seq=seq)
        SeqIO.write(rec, out_fh, 'fasta')
