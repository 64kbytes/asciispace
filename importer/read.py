#!/usr/bin/python
import codecs

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

with codecs.open('ship.txt','rU', encoding='utf8') as f:
	lin = []
	for line in f:
		shipmap = []
		print line.rstrip()
		for char in line:
			lin.append(char)
		shipmap.append(lin)

