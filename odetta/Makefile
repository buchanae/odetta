GENOME_FASTA = 
GENOME_GFF = 
MIN_OVERLAP = 0.8
MIN_EXONS = 2
MIN_MRNA_LENGTH = 1000
READS = reads/*.fasta
SPLIT_SIZE = 25000000

TIME = /usr/bin/time --output=times --append
ODETTA = $(TIME) odetta
BOWTIE_BUILD = $(TIME) bowtie-build --offrate 1 --quiet
BOWTIE = $(TIME) bowtie -f -p 8 -v 0 --suppress 6,7,8 --all
SUPERSPLAT = $(TIME) /path/to/multisplat

JOB = $(ODETTA) run 
SPLAT = $(SUPERSPLAT) splat -t 8 -n 1000 -x 5000 -c 40 -i 41 -S 1
STACK = $(SUPERSPLAT) stack -n 1 -c 1


GENOME_EBWT = genome.1.ebwt genome.2.ebwt genome.3.ebwt \
              genome.4.ebwt genome.rev.1.ebwt genome.rev.2.ebwt

all : overlap.gff

$(GENOME_EBWT) : $(GENOME_FASTA)
		$(BOWTIE_BUILD) $(GENOME_FASTA) genome

unaligned.fasta aligned.bowtie : $(GENOME_EBWT)
		$(BOWTIE) --un unaligned.fasta genome $(READS) aligned.bowtie

split-unaligned : unaligned.fasta
		split --lines=$(SPLIT_SIZE) unaligned.fasta split-unaligned-
		touch split-unaligned

splat-unaligned : split-unaligned-*
		$(SPLAT) -f $? -r $(GENOME_FASTA)
		touch splat-unaligned
		
splat.json : *.supersplat
		$(JOB) parse.split-splat $^ > splat.json

aligned.json : aligned.bowtie
		$(JOB) parse.bowtie aligned.bowtie > aligned.json

pairs.json : splat.json aligned.json
		$(JOB) pairs.combiner splat.json aligned.json > pairs.json

pairs-stats.json : pairs.json
		$(JOB) pairs.distance-statistics pairs.json > pairs-stats.json

valid.json : pairs.json
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

GMB_EBWT = gmb.1.ebwt gmb.2.ebwt gmb.3.ebwt gmb.4.ebwt gmb.rev.1.ebwt gmb.rev.2.ebwt 
$(GMB_EBWT) : gmb.fasta
		$(BOWTIE_BUILD) gmb.fasta gmb

gmb.bowtie : $(GMB_EBWT)
		 $(BOWTIE) -a gmb $(READS) gmb.bowtie

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
