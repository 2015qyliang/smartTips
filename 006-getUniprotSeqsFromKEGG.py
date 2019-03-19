# author: qyliang
# email: qyliang2017@gmail.com
# time: 2019-03-19
# Description: download uniprot seqs from KEGG according KO id
# python getUniprotSeqsFromKEGG.py K01915

import requests
import time
import sys
import re

keggUrl = 'https://www.genome.jp/dbget-bin/get_linkdb?-t+10+ko:'
uniprotUrl = 'https://www.genome.jp/dbget-bin/www_bget?uniprot:'

ko = sys.argv[1]
html = requests.get(keggUrl + ko)
newseq = []
if html.status_code == 200:
	print('----  Getting ', ko, '  ----')
	# get uniprot seq id
	matchList = re.findall( r'(<a href="/dbget-bin/www_bget\?uniprot:)(\w{4,12})(">)' , html.text)
	seqIdList = [ line[1] for line in matchList ]
	seqsNum = len(seqIdList)
	# maybe this ko links nothing
	if seqsNum == 0:
		print('No link information was found !\n----    Trying another    ----')
	# get sequences
	order = 1
	for seqid in seqIdList:
		seqUrl = uniprotUrl + seqid
		time.sleep(0.1)
		seqHtml = requests.get(seqUrl)
		if seqHtml.status_code == 200:
			seqmatch = re.findall( r'(     )([\w\s]{5,70})(\n)', seqHtml.text)
			# get row sequence
			seqList = [ line[1].replace(' ', '') for line in seqmatch if line[1].replace(' ', '').isupper() ]
			seqs = ''.join(seqList)
			newseq.append('>' + seqid + '\n' + seqs + '\n')
			print('---- ', ko, ' -- ',order , ' of ',seqsNum, '  --  ' , seqid)
			order += 1
open(ko + '.fasta', 'w').writelines(newseq)

