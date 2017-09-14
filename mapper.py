# Author : Ramkrushna Pradhan
# Date	 : 4-May-2016

import csv,sys,time
#import matplotlib.pyplot as plt
from pblga import check_sarc as PBLGA
from antonym import check_sarc as PSWAP
from interjection import check_sarc as IWS

if __name__ == "__main__":
	# logfile = open("log_5000.txt","w")	# store unresolved tweets	
	cnt = 0
	sarc_count = 0
	pblga_cnt,pswap_cnt,iws_cnt = 0,0,0
	graph_data = {}
	stime = time.time()	# start time
	ctime = int(time.time() - stime)
	newcnt = 0
	for tweet in sys.stdin:	# read from standard input
		tmp = int(time.time() - stime)		
		if tmp > ctime:
			graph_data[ctime] = newcnt
			newcnt = 1
			ctime = tmp
		else:
			newcnt += 1
		if len(tweet.split()) > 1:	# ignoring single word tweets
			try:
				if PSWAP(tweet):
					# print 'Tweet : ',cnt,1,'\tPSWAP'
					sarc_count += 1
					pswap_cnt += 1
				elif IWS(tweet):
					# print 'Tweet : ',cnt,1,'\tIWS'
					sarc_count += 1
					iws_cnt += 1 
				elif PBLGA(tweet):
					# print 'Tweet : ',cnt,1,'\tPBLGA'
					sarc_count += 1
					pblga_cnt += 1 
				else:
					# print 'Tweet : ',cnt,0
					pass
				cnt += 1
			except:
				pass
				# logfile.write(tweet + '\n')
	#f.close()
	#logfile.close()
	#print "Accuracy : ",sarc_count*100.0/cnt
	#print "Total Sarcastic : ",sarc_count
	#print "IWS : ",iws_cnt
	#print "PBLGA : ",pblga_cnt
	#print "PSWAP : ",pswap_cnt
	# plotting 	
	x = []
	y = []
	for i in graph_data:
		x.append(i)
		y.append(graph_data[i])
	for i in zip(x,y):
		print i[0],i[1]	
	#print sum(graph_data.values())
	#plt.plot(x,y,'ro')
	#plt.xlabel('Time (per 5 second)')
	#plt.ylabel('Number of Tweets')
#plt.show()
