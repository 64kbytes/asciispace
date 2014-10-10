#!/usr/bin/python

import codecs


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

with codecs.open('ship.txt','rU',encoding='utf8') as f:
	cols = []
	for line in f:
		rows = []
		for char in line:
			cols.append(char.rstrip())
		cols.append('\n')
		rows.append(cols)

for y in range(0, len(rows)):
	for x in range(0, len(cols)):
		print rows[y][x]

#print bcolors.OKGREEN + ) + bcolors.ENDC
#quit()


	

	
	
	 


