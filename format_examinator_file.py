#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Format examinator layer - Python's Version by aabilio

import sys

def win32():
	if sys.platform is "Win32": return True
	else: return False

def usage():
	print "Format Examinator questions' file by aabilio\n\nUsage:\n\t%s <file> [> output_file]" % sys.argv[0]
	#print 

def getQuestionsFromFile(file):
	'''Take an file and return the questions in list of list format'''
	quest = []
	try:
		f = open(file)
	except IOError:
		if win32:
			print "No se encuentra el fichero con las preguntas:", file
			sys.exit()
		else:
			sys.exit("No se encuentra el fichero con preguntas: %s" % file)

	while True:
		line = f.readline()
		if not line: break
		else:
			tmp = line.split("*")
			quest.append(tmp)
	f.close()
	return quest

if __name__ == "__main__":
	if len(sys.argv) != 2:
		sys.exit(usage())
	else:
		File = sys.argv[1]
	
	questions = getQuestionsFromFile(File)
	qtonum = {2:"a",3:"b",4:"c",5:"d",6:"e"}

	for question in questions:
		print "%s) %s" % (question[0], question[1])
		for i in range(2,7):
			if qtonum[i] == question[7].strip():
				print "  > %s) %s" % (qtonum[i],question[i])
			else:
				print "    %s) %s" % (qtonum[i],question[i])
