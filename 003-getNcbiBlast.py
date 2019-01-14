# author: qyliang
# email: qyliang2017@gmail.com
# time: 2019-01-14
# Description: summary seqs blast result, return tab file

from Bio.Blast import NCBIWWW
from Bio import SeqIO
import requests
import argparse
import time
import re

# parse argument
parser = argparse.ArgumentParser()
parser.add_argument('-f','--file',type=str,dest = 'seqfile',help = "Fasta format sequences file")
args = parser.parse_args()

# define main function
def getNcbiBlast(seqfile):
	for sequence in SeqIO.parse(open(seqfile),'fasta'):
		start = time.time()
		result_handle = NCBIWWW.qblast('blastn', 'nt', sequence.seq, hitlist_size=200, format_type="Text")
		end = time.time()
		print(sequence.id,str(end - start))
		open(str(sequence.id + '.txt'), 'w').write(result_handle.read())
		blast_result = [ line for line in open(str(sequence.id + '.txt')).readlines()[15:] ]
		for i in range(len(blast_result)):
			linestr = blast_result[i]
			if linestr.startswith('>'):
				genebankId = linestr.split(' ')[0][1:]
				identity = blast_result[i+5].split('),')[0].split('(')[1]
				ncbiUrl = 'https://www.ncbi.nlm.nih.gov/nuccore/' + genebankId
				responseNuccore = requests.get(ncbiUrl)
				print(sequence.id, genebankId)
				time.sleep(0.2)
				if responseNuccore.status_code == 200:
					pattern = re.compile(r'(index.cgi\?ORGANISM=)(\d{3,12})' )
					taxId = pattern.findall(responseNuccore.text)[0][1]
					taxUrl = 'https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?id=' + taxId
					responseTax = requests.get(taxUrl)
					if responseTax.status_code == 200:
						hitphylum = re.findall(r'(TITLE="phylum">)(\w{5,30})(</a>)',responseTax.text)
						hitclass = re.findall(r'(TITLE="class">)(\w{5,30})(</a>)', responseTax.text)
						hitorder = re.findall(r'(TITLE="order">)(\w{5,30})(</a>)', responseTax.text)
						hitfamily = re.findall(r'(TITLE="family">)(\w{5,30})(</a>)', responseTax.text)
						hitgenus = re.findall(r'(TITLE="genus">)(\w{5,30})(</a>)', responseTax.text)
						hitspecies = re.findall(r'(<h2>)(\w{5,20}\s\w{5,20})(</h2>)', responseTax.text)
						if hitspecies != [] and hitfamily != [] and hitorder != []:
							strList = [sequence.id, genebankId, str(identity), hitphylum[0][1], hitclass[0][1], hitorder[0][1],
							           hitfamily[0][1], hitgenus[0][1], hitspecies[0][1]]
							seqHitstring = '\t'.join(strList) + '\n'
							open( seqfile.split('.')[0] + 'NcbiBlast' + '.txt','a').write(seqHitstring)
							break

# try ... except ...
try:
	getNcbiBlast(str(args.seqfile))
except Exception as e:
	raise e

