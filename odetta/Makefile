GENOME_FASTA = 
GENOME_GFF = 
MIN_OVERLAP = 0.8
MIN_EXONS = 2
MIN_MRNA_LENGTH = 1000
READS = reads/*.fasta
SPLIT_SIZE = 25000000

TIME = time
ODETTA = odetta
BOWTIE_BUILD = $(TIME) bowtie-build --offrate 1
BOWTIE = $(TIME) bowtie -f -p 8 -v 0 --suppress 6,7,8
JOB = $(TIME) $(ODETTA) run 
SUPERSPLAT = $(TIME) /path/to/multisplat
SPLAT = $(SUPERSPLAT) splat -t 8 -n 1000 -x 5000 -c 40 -i 41 -S 1
STACK = $(SUPERSPLAT) stack -n 1 -c 1


GENOME_EWBT = genome.1.ewbt genome.2.ewbt genome.3.ewbt \
              genome.4.ewbt genome.rev.1.ewbt genome.rev.2.ewbt

all : overlap.gff

$(GENOME_EWBT) : $(GENOME_FASTA)
		$(BOWTIE_BUILD) $(GENOME_FASTA) genome

unaligned.fasta aligned.bowtie : $(GENOME_EWBT)
		$(BOWTIE) --un unaligned.fasta -a aligned.bowtie $(READS) genome

splat.json : unaligned.fasta
		split --lines=$(SPLIT_SIZE) unaligned.fasta split-unaligned-
		
		for file in split-unaligned-*; do \
		    $(SPLAT) -f $$file -r $(GENOME_FASTA) 
		done
		
		$(JOB) parse./splitsplit.py *.supersplat > splat.json
		rm -f *.supersplat

aligned.json : aligned.bowtie
		$(JOB) parse.bowtie aligned.bowtie > aligned.json

incomplete.json : aligned.json
		$(JOB) pairs.incomplete-filter aligned.json > incomplete.json

pairs.json : splat.json incomplete.json
		$(JOB) pairs.combiner splat.json incomplete_cashx.json > pairs.json

pairs-stats.json : pairs.json
		$(JOB) pairs.distance-statistics pairs.json > pairs-stats.json

valid.json : pairs.json:
		$(JOB) pairs.valid-filter pairs.json > valid.json

valid.splat : valid.json
		$(JOB) pairs.to-splat valid.json > valid.splat

aligned.sam : aligned.json
		$(JOB) to-sam aligned.json > aligned.sam

stacks : valid.splat
		$(STACK) -r $(GENOME_FASTA) -s valid.splat -o stacks

gmb.gff : stacks aligned.sam
		$(GMB) -r $(GENOME_FASTA) -a aligned.sam -s stacks -o gmb.gff

gmb.fasta : gmb.gff
		$(JOB) gff.transcriptome --genome $(GENOME_FASTA) gmb.gff > gmb.fasta

GMB_EWBT = gmb.1.ewbt gmb.2.ewbt gmb.3.ewbt gmb.4.ewbt gmb.rev.1.ewbt gmb.rev.2.ewbt 
$(GMB_EWBT) : gmb.fasta
		$(BOWTIE_BUILD) gmb.fasta gmb

gmb.bowtie : $(GMB_EWBT)
		 $(BOWTIE) -a gmb.bowtie $(READS) gmb

gmb-aligned.json : gmb.bowtie
		$(JOB) parse.bowtie gmb.bowtie > gmb-aligned.json

gmb-pairs.json : gmb-aligned.json
		$(JOB) pairs.combiner gmb-aligned.json > gmb-pairs.json

gmb-pairs-stats.json : gmb-pairs.json
		$(JOB) pairs.distance-statistics gmb-pairs.json > gmb-pairs-stats.json

gmb-valid.json : gmb-pairs.json
		$(JOB) pairs.valid-filter gmb-pairs.json > gmb-valid.json

gmb-unambiguous.json : gmb-valid.json
		$(JOB) pairs.unambiguous-filter gmb-valid.json > gmb-unambiguous.json

gmb-counts.json : gmb-unambiguous.json
		$(JOB) pairs.reference-counts gmb-unambiguous.json > counts.json

filtered.gff : gmb-counts.json gmb.gff
		$(JOB) gff.filter --counts gmb-counts.json --min-length $(MIN_MRNA_LENGTH) \
											--min-exons $(MIN_EXONS) gmb.gff > filtered.gff

overlap.gff : filtered.gff
		$(JOB) gff.overlap --reference $(GENOME_GFF) --min-overlap $(MIN_OVERLAP) \
												filtered.gff > overlap.gff
