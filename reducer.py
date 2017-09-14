import sys
from collections import defaultdict,OrderedDict
final_data = []
for line in sys.stdin:
	a,b = line.split()
	final_data.append((a,b))
print final_data
