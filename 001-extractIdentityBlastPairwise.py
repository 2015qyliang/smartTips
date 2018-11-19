# author: qyliang
# email: qyliang2017@gmail.com
# time: 2018-11-19
# Description: extract identity of Blast Pairwise Sequence Alignment
# Note: align sequence must be fasta format
# step-1: makeblastdb.exe -dbtype nucl -parse_seqids -in example.fasta -out .\database\example
# step-2: blastn.exe -query example.fasta -db .\database\example -evalue 1e-5 \
# 			 -max_target_seqs <Int> -num_threads 8 -outfmt 6 \
# 			 -perc_identity <Int> -out blast_pairwise.txt

import argparse

# parse argument
parser = argparse.ArgumentParser()
parser.add_argument('-i','--i',type=str,dest = 'seqidFile',help = "Sequence id in one column...")
parser.add_argument('-b','--b',type=str,dest = 'blastresultFile',help = "Blast pairwise alignment result...")
parser.add_argument('-o','--o',type=str,dest = 'output',help = "Extracted matrix (matrix.txt)...")
args = parser.parse_args()

# define main function
def extractMatrix(seqidFile,blastresultFile,output):
	SeqId = [ line.strip() for line in open(seqidFile).readlines()]
	extractMat = []
	extractMat.append('seqID' + '\t' + '\t'.join(SeqId) + '\n')
	textBlastResult = open(blastresultFile).readlines()
	for rowid in SeqId:
		newstr = rowid + '\t'
		for colid in SeqId:
			searchstr = rowid + '\t' + colid + '\t'
			for line in textBlastResult:
				if searchstr in line:
					newstr += str(line.split('\t')[2])
					break
		extractMat.append(newstr + '\n')
	open(output, 'w').writelines(extractMat)

# try ... except ...
try:
	extractMatrix(args.seqidFile, args.blastresultFile, args.output)
except Exception as e:
	raise e
