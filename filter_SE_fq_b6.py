#!/usr/bin/env python

from Bio import SeqIO
import sys
import os
import csv

usage = 'python filter_SE_fq_b6.py align_R1.b6 orig_R1.fastq filtered_filename summary_fname/NONE summary_dir/NONE'

if len(sys.argv) < 3:
		print('You must supply the R1 alignment file, original FASTQ, a prefix for the filtered output,\na summary filename or NONE, and a directory for summary files or NONE\n\n%s\n' % usage)
		sys.exit()

inb6_R1 = sys.argv[1]
infastq_R1 = sys.argv[2]
outfq = sys.argv[3]
if sys.argv[4] != 'NONE' and sys.argv[5] != 'NONE':
	summarize = True
	summary_name = sys.argv[4]
	summary = ''.join([sys.argv[4], '_log.txt'])
	summary = os.path.join(sys.argv[5], summary)

host_read_ids = []
with open(inb6_R1, 'r') as inf1:
		tabreader1 = csv.reader(inf1, delimiter='\t')
		for line in tabreader1:
				read_id = str(line[0])
#				print(read_id)
				host_read_ids.append(read_id)
host_read_set = set(host_read_ids)
print('\n...filtering %s reads from FASTQ file...\n' % len(host_read_set))
# Filter the FASTQs to exclude reads from either b6 files (to maintain paired reads)
outfq1 = ''.join([outfq, '.fastq'])
with open(outfq1, 'w') as outf1, open(infastq_R1, 'r') as infq1:
		keep_seqs1 = [record for record in SeqIO.parse(infq1, 'fastq') if str(record.id).split(' ')[0] not in host_read_set]
		SeqIO.write(keep_seqs1, outf1, 'fastq')

if summarize:
	# https://stackoverflow.com/questions/845058/how-to-get-line-count-cheaply-in-python
	def file_len(fname):
		with open(fname) as f:
			for i, l in enumerate(f):
				pass
		return i + 1
	with open(summary, 'w') as outsum:
		original = (file_len(infastq_R1) / 4)
		filtered = len(host_read_set)
		humanfrac = round(filtered / original * 100, 3)
		outsum.write(str(summary_name) + '\t' + str(humanfrac) + '\n')
