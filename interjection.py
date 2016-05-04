# Author   : Ramkrushna Pradhan
# Date     : 3-May-2016
# The tagger used for this task was taken from the following resources
# Citation : Improved Part-of-Speech Tagging for Online Conversational Text with Word Clusters,
#	     Olutobi Owoputi, Brendan O'Connor, Chris Dyer, Kevin Gimpel, Nathan Schneider and Noah A. Smith. 
#	     In Proceedings of NAACL 2013.
# Tags     : '!' = interjection,'R' = adverb,'A' = adjective,'N' = noun,'V' = verb.

import sys
import csv
import tempfile
import subprocess
from subprocess import Popen,call

# check if sarcastic
def check_sarc(tweet):
	f = open("temp.txt","w")	# create a temporary file
	f.write(tweet)
	f.close()	
	p = Popen("java -Xmx500m -jar ark-tweet-nlp-0.3.2.jar temp.txt".split(), stdout=subprocess.PIPE)	# perform POS tagging
	out,err = p.communicate()
	
	pairs = zip(out.split('\t')[0].split(),out.split('\t')[1].split())
	words = out.split('\t')[0].split()
	tags  = out.split('\t')[1].split()
	print tags
	call(["rm","temp.txt"])		# delete the temprary file
	
	FT    = tags[0]	# first tag
	INT   = tags[1] # Immediate Next Tag
	NT    = [(tags[i],tags[i+1]) for i in range(2,len(tags)-1)]	# all the next tags 
	
	if (FT == '!' and INT in ['A','R']):
		return 1	# sarcasm found
	elif  (FT == '!' and any(x in NT for x in [('A','R'),('A','N'),('A','V')])):
		return 1	# sarcasm found
	else:
		return 0	# no sarcasm


if __name__ == "__main__":
	print check_sarc("wow publicly promoting the 1% concept. great.")		
