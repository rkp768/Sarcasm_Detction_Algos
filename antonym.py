# Author   : Ramkrushna Pradhan
# Date     : 2-May-2016
# The tagger used for this task was taken from the following resources
# Citation : Improved Part-of-Speech Tagging for Online Conversational Text with Word Clusters,
#	     Olutobi Owoputi, Brendan O’Connor, Chris Dyer, Kevin Gimpel, Nathan Schneider and Noah A. Smith. 
#	     In Proceedings of NAACL 2013.


import sys
import csv
import tempfile
import subprocess
from subprocess import Popen,call
from nltk.corpus import wordnet as wn

# get antonym pairs from corpus
def antonym():
	ANTONYM = {}	# antonym list
	for i in wn.all_synsets():
    		if i.pos() in ['a', 's']:
        		for j in i.lemmas():
        		    if j.antonyms():
        		        ANTONYM[j.name()] = j.antonyms()[0].name()
	return ANTONYM

# check if sarcastic
def check_sarc(tweet):
	ANTONYM = antonym()
	f = open("temp.txt","w")	# create a temporary file
	f.write(tweet)
	f.close()
	# perform POS tagging	
	p = Popen("java -Xmx500m -jar ark-tweet-nlp-0.3.2.jar temp.txt".split(), stdout=subprocess.PIPE)	
	out,err = p.communicate()
	print out
	temp = zip(out.split('\t')[0].split(),out.split('\t')[1].split())
	call(["rm","temp.txt"])		# delete the temprary file
	lst = []
	if out.split('\t')[1].split().count('A') >= 2:
		for i in temp:
			if i[1]=='A':
				lst.append(i[0])
	for i in lst:
		if ANTONYM[i] in lst:
			return 1
	return 0

if __name__ == "__main__":
	# check sarcasm of the processed file, beware , this may take lot of time, you may use a smaller file
	f = open("Datasets/processed_tweets.csv","r")	
	rdr = csv.reader(f)
	sarc_cnt = 0
	cnt = 0
	for line in rdr:
		cnt += 1
		if check_sarc(line[0]):
			sarc_cnt += 1
	print "Total Sarcasm Tweets : ",sarc_cnt
	f.close()
