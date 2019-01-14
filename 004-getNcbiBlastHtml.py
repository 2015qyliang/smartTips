# author: qyliang
# email: qyliang2017@gmail.com
# time: 2019-01-14
# Description: save blast result as Html

from Bio.Blast import NCBIWWW
from Bio import SeqIO
import argparse

# parse argument
parser = argparse.ArgumentParser()
parser.add_argument('-f','--file',type=str,dest = 'seqfile',help = "Fasta format sequences file")
args = parser.parse_args()

# define main function
def getNcbiBlast(seqfile):
	for sequence in SeqIO.parse(open(seqfile),'fasta'):
		start = time.time()
		result_handle = NCBIWWW.qblast('blastn', 'nt', sequence.seq, hitlist_size=200, format_type="HTML")
		end = time.time()
		print(sequence.id,str(end - start))
		open(str(sequence.id + '.html'), 'w').write(result_handle.read())

# try ... except ...
try:
	getNcbiBlast(str(args.seqfile))
except Exception as e:
	raise e

