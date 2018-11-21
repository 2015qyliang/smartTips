#!/bin/sh
# bacterial draft genome assemble pipeline
# $1 pass forward.fq.gz file name: forward
# $2 pass reverse.fq.gz file name: reverse

if [[ $1 == "" && $2 == "" ]]; then
	echo "---> Please input forward_seq and reverse_seq"
	exit
fi

workpath=$PWD
trimmomatic="/home/liangqiyun/softtools/Trimmomatic-0.36/trimmomatic-0.36.jar"
# Raw reads were trimmed to remove the adapter sequences and low-quality bases using trimmomatic
java -jar $trimmomatic PE -phred33 \
 $1".fq.gz" $2".fq.gz" \
 $1"clean.fq.gz" output_forward_unpaired.fq.gz \
 $2"clean.fq.gz" output_reverse_unpaired.fq.gz \
 ILLUMINACLIP:TruSeq3-PE.fa:2:30:10 LEADING:3 \
 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36
rm -rf output_forward_unpaired.fq.gz output_reverse_unpaired.fq.gz
mkdir rawReads
mv $1".fq.gz" rawReads/
mv $2".fq.gz" rawReads/
gzip -d $1"clean.fq.gz"
gzip -d $2"clean.fq.gz"

# SPAdes assemble
mkdir SPAdes
cd SPAdes
for kmer in 31 41 51 61 71 81 91 101 111 121
do
	spades.py -t 16 -k $kmer --careful --only-assembler -1 $1"clean.fq" -2 $2"clean.fq" -o "kmer_"$kmer
done
cd ..

# SOAPdenovo assemble
mkdir SOAPdenovo
cd SOAPdenovo
echo '''
#maximal read length
max_rd_len=150
[LIB]
#average insert size
avg_ins=350
#if sequence needs to be reversed
reverse_seq=0
#in which part(s) the reads are used
asm_flags=3
#use only first <Int> bps of each read
rd_len_cutoff=150
#in which order the reads are used while scaffolding
rank=1
# cutoff of pair number for a reliable connection (at least 3 for short insert size)
pair_num_cutoff=3
#minimum aligned length to contigs for a reliable read location (at least 32 for short insert size)
map_len=32
# path to reads
''' > config.file
echo "q1="$workpath"/"$1"clean.fq" >> config.file
echo "q2="$workpath"/"$2"clean.fq" >> config.file
for kmer in 21 31 41 51 61 71 81 91 101,111,121
do
	if [[ $kmer -lt 63 ]]; then
		mkdir "kmer_"$kmer
		cd "kmer_"$kmer
		SOAPdenovo-63mer all -s ../config.file -K $kmer -R -p 20 -o "kmer_"$kmer
		cd ..
	fi
	if [[ $kmer -gt 63 ]]; then
		mkdir "kmer_"$kmer
		cd "kmer_"$kmer
		SOAPdenovo-127mer all -s ../config.file -K $kmer -R -p 20 -o "kmer_"$kmer
		cd ..
	fi
done
cd ..

# MaSuRca assemble
mkdir MaSuRca
cd MaSuRca
echo "DATA" > config.file
echo "PE= pe 350 50 " $workpath"/"$1"clean.fq" $workpath"/"$2"clean.fq" >> config.file
echo '''
END
PARAMETERS
EXTEND_JUMP_READS=0
GRAPH_KMER_SIZE = auto
USE_LINKING_MATES = 0
USE_GRID=0
GRID_QUEUE=all.q
GRID_BATCH_SIZE=300000000
LHE_COVERAGE=30
LIMIT_JUMP_COVERAGE = 60
CA_PARAMETERS =  cgwErrorRate=0.25
KMER_COUNT_THRESHOLD = 1
CLOSE_GAPS=1
NUM_THREADS = 16
JF_SIZE = 200000000
SOAP_ASSEMBLY=0
END
''' >> config.file
masurca config.file
./assemble.sh
cd ..

