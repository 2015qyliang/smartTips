# author: qyliang
# email: qyliang2017@gmail.com
# time: 2019-01-15
# Description: download IJSEM.pdf, searched from pubmed

# search following string in NCBI-Pubmed and send PubmedId into pubmed.txt
# (("International journal of systematic and evolutionary microbiology"[Journal])) 
# AND (marine or sea or seawater or ocean or bay or intertidal or costal or beach 
# or sponges or vent or oyster or shark or whale or coral or alga)

import requests
import re

def getPubmed(pubmedId):
	pubmedUrl = 'https://www.ncbi.nlm.nih.gov/pubmed/' + pubmedId
	reponseRul = requests.get(pubmedUrl)
	if reponseRul.status_code == 200:
		# print(re.findall(r'(<a href="//doi.org)(.{23})', reponseRul.text)[0][1])
		ijsemDoi = re.findall(r'(<a href="//doi.org)(.{23})', reponseRul.text)[0][1]
		IjsemUrl = 'https://ijs.microbiologyresearch.org/content/journal/ijsem' + ijsemDoi
		IjsemUrlrespons = requests.get(IjsemUrl)
		if IjsemUrlrespons.status_code == 200:
			# print(re.findall( r'(a href="/deliver/fulltext/ijsem/)(.{77,78})(&amp;mimeType=pdf&amp;isFastTrackArticle=)' , IjsemUrlrespons.text))
			if re.findall( r'(a href="/deliver/fulltext/ijsem/)(.{77,78})(&amp;mimeType=pdf&amp;isFastTrackArticle=)' , IjsemUrlrespons.text) != []:
				pdfUrlMid = re.findall( r'(a href="/deliver/fulltext/ijsem/)(.{77,78})(&amp;mimeType=pdf&amp;isFastTrackArticle=)' , IjsemUrlrespons.text)[0][1]
				pdfUrl = 'https://www.microbiologyresearch.org/deliver/fulltext/ijsem/' + pdfUrlMid + '&amp;mimeType=pdf&amp;isFastTrackArticle='
				pdftext = requests.get(pdfUrl)
				open(str( ijsemDoi.split('.')[-1] +'.pdf'),'wb').write(pdftext.content)


publist = [ line.strip() for line in open('pubmed.txt').readlines() ]
for pub in publist:
	getPubmed(pub)
	print('which downloaded: ',pub)
	open('Downloaded.txt','a').write(pub)
