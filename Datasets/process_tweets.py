# this code preproceses the file "Sarcastic tweets.txt"
# tweets taken directly from tweeter manually.

import tempfile
import re,csv
f = open("Sarcastic tweets.txt","r")

# regular expressions used for filtering
pat1 = r'\d*\s+retweet[s]?'
pat2 = r'\d*\s+favorite[s]?'
pat3 = r'Retweet\s+\d*'
pat4 = r'Favorite\s+\d*'
pat5 = r'Reply'
pat6 = r'More'
pat7 = r'Like\s+\d*'
pat8 = r'\s*\d*like[s]?'
pat9 = r'View conversation'
pat10 = r'http[s]?://.*'
pat11 = r'Embedded image permalink'
pat12 = 'hours ago'
pat13 = r'.*[?]@\w+\s+\w+\s+\d+'
pat14 = r'\s*[Ii]n\s*[Rr]eply\s*[Tt]o.*'
##

new = tempfile.TemporaryFile()

for line in f.readlines():
	line = re.sub(pat1,'',line)
	line = re.sub(pat2,'',line)
	line = re.sub(pat3,'',line)
	line = re.sub(pat4,'',line)
	line = re.sub(pat5,'',line)
	line = re.sub(pat6,'',line)
	line = re.sub(pat7,'',line)
	line = re.sub(pat8,'',line)
	line = re.sub(pat9,'',line)
	line = re.sub(pat10,'',line)
	line = re.sub(pat11,'',line)
	if re.findall(pat13,line) or line.strip().endswith(pat12) or len(line.strip())==1 or re.match(pat14,line):
		new.write('*\n')
	else:
		new.write(line)
f.close()
new.seek(0)

##
# writing to csv file
csvfile = open('processed_tweets.csv','w')
wr = csv.writer(csvfile)
var = ''
for line in new:
	line = line.strip('\n')
	if line.startswith('*') and var.strip().strip('*'):
		var = var.strip('\n').strip()
		wr.writerow([var.strip('*')])
		var = ''
	elif line:
		var += line.strip('\n')
	else:
		pass
new.close()
csvfile.close()
