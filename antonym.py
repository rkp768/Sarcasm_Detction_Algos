# Author   : Ramkrushna Pradhan
# Date     : 2-May-2016
# Purpose  : This program takes a tweet as input and returns if the tweet is sarcastic or not.
# The tagger used for this task was taken from the following resources
# Citation : Improved Part-of-Speech Tagging for Online Conversational Text with Word Clusters,
#	     Olutobi Owoputi, Brendan O'Connor, Chris Dyer, Kevin Gimpel, Nathan Schneider and Noah A. Smith. 
#	     In Proceedings of NAACL 2013.


import sys
import csv
import tempfile
import subprocess
from subprocess import Popen,call
from textblob import TextBlob

# get antonym pairs from corpus
def get_antonym():
	ANTONYM = {}
	with open('antonyms.txt') as f:
  		for line in f:
       			(key, val) = line.split(':')
       			ANTONYM[key.strip()] = val.strip()
	f.close()
	return ANTONYM

# check if sarcastic
def check_sarc(tweet):
	ANTONYM = get_antonym()
	temp = zip(tweet.split('\t')[0].split(),tweet.split('\t')[1].split())
	lst = []
	blob = TextBlob(tweet.split('\t')[0])
	flag = 0	
	if blob.polarity >0:
		flag = 1
	for i in temp:
		if i[1]=='A' or i[1]=='N' or i[1]=='V' or i[1]=='R':
			lst.append(i[0])
	for i in lst:
		try:
			if (ANTONYM[i] in lst) and flag:
				return 1	# sarcasm detected
		except:
			pass
	return 0	# no sarcasm

# check if sarcastic
def check_sarc1(tweet):
	ANTONYM = get_antonym()
	f = open("temp.txt","w")	# create a temporary file
	f.write(tweet)
	f.close()	
	p = Popen("java -Xmx500m -jar ark-tweet-nlp-0.3.2.jar temp.txt".split(), stdout=subprocess.PIPE)	# perform POS tagging
	out,err = p.communicate()
	temp = zip(out.split('\t')[0].split(),out.split('\t')[1].split())
	call(["rm","temp.txt"])		# delete the temprary file
	lst = []
	for i in temp:
		if i[1]=='A' or i[1]=='N' or i[1]=='V' or i[1]=='R':
			lst.append(i[0])
	for i in lst:
		try:
			if ANTONYM[i] in lst:
				return 1	# sarcasm detected
		except:
			pass
	return 0	# no sarcasm

if __name__ == "__main__":
	f = open("all_tagged.txt","r")
	possible = 0
	yes = 0 
	for tweet in f.readlines():
		try:
			temp = tweet.split('\t')[1].split()
			blob = TextBlob(tweet.split('\t')[0])
			if blob.polarity > 0 and any(x in ['A','N','V','R'] for x in temp):
				possible += 1
				try:
					if check_sarc(tweet):
						yes += 1
				except:
					pass
		except:
			pass
	f.close()
	print "possible = ",possible
print "yes = ",yes
