# Author   : Ramkrushna Pradhan
# Date     : 4-May-2016
# This code used textblob parsers and seniment analyzers. Feel free to modify them to fit your own purpose.
import sys
import csv
import tempfile
from textblob import TextBlob
from textblob.parsers import PatternParser
from collections import defaultdict

# check is sarcastic
def check_sarc(tweet):
	blob = TextBlob(tweet, parser=PatternParser())
	tokens = blob.parse().split(' ')
	dic = defaultdict(list)	# stores all phrases by category
	temp = ''
	phrases = []	# list of all phrases
	for t in tokens:
		if t.split('/')[2] == 'O':
			if temp:
				phrases.append((ctag,temp))			
			dic[t.split('/')[2]].append(temp)
			temp = t.split('/')[0]+' '
			ctag = t.split('/')[2]
		elif 'B-' in t.split('/')[2]:
			if temp:
				phrases.append((ctag,temp))
			temp = t.split('/')[0]+' '
			dic[t.split('/')[2].split('-')[1]].append(temp)
			ctag = t.split('/')[2].split('-')[1]
		elif 'I-' in t.split('/')[2]:
			dic[t.split('/')[2].split('-')[1]][-1] += t.split('/')[0]+' '
			temp += t.split('/')[0]+' '
			ctag = t.split('/')[2].split('-')[1]
		else:
			pass
	if temp:
		phrases.append((ctag,temp))
	SF = []
	sf = []
	for i in phrases:
		if i[0] in ['NP','ADjP']:
			SF.append(i[1])
		elif i[0]=='VP':
			sf.append(i[1])
	for i in range(len(phrases)-1):
		if phrases[i][0]=='NP' and phrases[i+1][0]=='VP':
			SF.append(phrases[i][1]+' '+phrases[i+1][1])
		elif phrases[i][0]=='ADVP' and phrases[i+1][0]=='VP':
			sf.append(phrases[i][1]+' '+phrases[i+1][1])
		elif phrases[i][0]=='VP' and phrases[i+1][0]=='ADVP':
			sf.append(phrases[i][1]+' '+phrases[i+1][1])
		elif phrases[i][0]=='ADJP' and phrases[i+1][0]=='VP':
			sf.append(phrases[i][1]+' '+phrases[i+1][1])
		elif phrases[i][0]=='VP' and phrases[i+1][0]=='NP':
			sf.append(phrases[i][1]+' '+phrases[i+1][1])
	for i in range(len(phrases)-2):
		if phrases[i][0]=='VP' and phrases[i+1][0]=='ADVP' and phrases[i+2][0]=='ADJP':
			sf.append(phrases[i][1]+' '+phrases[i+1][1]+' '+phrases[i+1][1])
		elif phrases[i][0]=='VP' and phrases[i+1][0]=='ADJP' and phrases[i+2][0]=='NP':
			sf.append(phrases[i][1]+' '+phrases[i+1][1]+' '+phrases[i+2][1])
		elif phrases[i][0]=='ADVP' and phrases[i+1][0]=='ADJP' and phrases[i+2][0]=='NP':
			sf.append(phrases[i][1]+' '+phrases[i+1][1]+' '+phrases[i+2][1])
	print SF
	print sf	
	PSF = []
	NSF = []
	psf = []
	nsf = []
	for i in SF:
		blob = TextBlob(i)
		if blob.polarity > 0:
			PSF.append(i)
		elif blob.polarity < 0:
			NSF.append(i)
		elif blob.polarity == 0:
			pass
	for i in sf:
		blob = TextBlob(i)
		if blob.polarity > 0:
			psf.append(i)
		elif blob.polarity < 0:
			psf.append(i)
		elif blob.polarity == 0:
			pass	
	print PSF
	print NSF
	print psf
	print nsf
	if (PSF and nsf) or (psf and NSF):
		return 1
	else:
		return 0	
if __name__ == "__main__":
	print check_sarc("Wow, my $23 paycheck sure does help out with my financial obligations. #sarcasm #joiningacommune #bye")
