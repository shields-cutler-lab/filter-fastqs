#!/usr/bin/env python

from Bio import SeqIO
import sys
import os
import csv

usage = 'python filter_by_b6.py align_R1.b6 align_R2.b6 orig_R1.fastq orig_R2.fastq filtered_prefix'

# Will add '_R1' and '_R2' to the end of the filtered prefix

if len(sys.argv) < 5:
	print('You must supply the R1 and R2 alignment files, original FASTQs, and a prefix for the filtered output\n\n%s\n' % usage)
	sys.exit()

inb6_R1 = sys.argv[1]
inb6_R2 = sys.argv[2]
infastq_R1 = sys.argv[3]
infastq_R2 = sys.argv[4]
outfq = sys.argv[5]

host_read_ids = []
with open(inb6_R1, 'r') as inf1, open(inb6_R2, 'r') as inf2:
	tabreader1 = csv.reader(inf1, delimiter='\t')
	for line in tabreader1:
		read_id = str(line[0])
#		print(read_id)
		host_read_ids.append(read_id)
	tabreader2 = csv.reader(inf2, delimiter='\t')
	for line in tabreader2:
		read_id = str(line[0])
		host_read_ids.append(read_id)
host_read_set = set(host_read_ids)
print('\n...filtering %s read pairs from FASTQ files...\n' % len(host_read_set))
# Filter the FASTQs to exclude reads from either b6 files (to maintain paired reads)
outfq1 = '_'.join([outfq, 'R1.fastq'])
outfq2 = '_'.join([outfq, 'R2.fastq'])
with open(outfq1, 'w') as outf1, open(infastq_R1, 'r') as infq1:
#	keep_seqs1 = [record for record in SeqIO.parse(infq1, 'fastq') if str(record.id).split(' ')[0] not in host_read_set]
#	SeqIO.write(keep_seqs1, outf1, 'fastq')
	# Previous two lines work the same as below line but consume massive RAM
	[SeqIO.write(record, outf1, 'fastq') for record in SeqIO.parse(infq1, 'fastq') if str(record.id).split(' ')[0] not in host_read_set]
with open(outfq2, 'w') as outf2, open(infastq_R2, 'r') as infq2:
#	keep_seqs2 = [record for record in SeqIO.parse(infq2, 'fastq') if str(record.id).split(' ')[0] not in host_read_set]
#	SeqIO.write(keep_seqs2, outf2, 'fastq')
	# Previous two lines work the same as below line but consume massive RAM
	[SeqIO.write(record, outf2, 'fastq') for record in SeqIO.parse(infq2, 'fastq') if str(record.id).split(' ')[0] not in host_read_set]

