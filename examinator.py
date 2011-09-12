#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Examinator Python's Version by aabilio

# This version of Examinator expects a file in the same directory 
# as the executable called "preguntas.txt" or a parameter: path to the file.
# The file should be in the following format:
#	number_of_question*Question*opt1*opt2*opt3*opt4*opt5*rigth_option
# (optx = optionX in text format and right_option in letter format ex.: "e")

import sys
import os
from random import shuffle

#OPCs:
FILE = "preguntas.txt" # Path to the file
NAME = "Examinator" # Program's name
VERSION = "1.0" # Program's version
PRESENTATION = "%s - %s" % (NAME,VERSION) # Presentation on doFromat()
AUTHOR = "aabilio"
# ==== End OPCs

def win32():
	'''return True if the user's platform is Windows'''
	if sys.platform is "Win32": return True
	else: return False
def cls():
	'''Clear screen'''
	if win32(): os.system("cls")
	else: os.system("clear")
def Win32end():
	'''Prevents the close of the cmd window on Windows'''
	raw_input("[PROGRAM END - ENTER TO EXIT]")
	sys.exit()

def usage():
	print "%s (%s) (Python Version) by %s\n\nUsage:\n\t%s [questions_file]" % (NAME, VERSION, AUTHOR, sys.argv[0])
	win32end() if win32() else sys.exit()

def get_answer(msg):
	''' "raw_input()" --> validate the answer'''
	while True:
		char = raw_input(msg)
		if char in ["a","b","c","d","e"]: return char


def printt(*msg):
    '''
    	Take a string and display it on screen with right format for win32 or *nix (spanish)
        Like a built in print python function:
        - Concatenations: '+' o ','
        - Use variables directly or by using format specifiers
        - Always use the "u" unicode
        - printt(), unlike built in print python function, does not print an adiciaonal newline character
        - Examples:
        	* printt(u"Hi! %s you're user number is %d" % (user, 925))
        	* printt(u"This is a message")
    '''
    if win32():
        for i in msg:
            print i.encode("cp850"), 
    else:
        for i in msg:
            print i, 

def doFormat():
	'''print on screen the presentation'''
	#OPCS:
	length = 60 # Must be even
	up_down_symbol = "*" #len() must be even
	lateral_symbol = "*" 
	# ==== end OPCS

	## Do not edit anything from here (unless you know what you're doing)
	w = (length-len(PRESENTATION)-4-len(lateral_symbol)*2)/2
	length = length/len(up_down_symbol)
	cls()
	print up_down_symbol * length
	print lateral_symbol, " " * w, PRESENTATION, " " * w, lateral_symbol
	print up_down_symbol * length

def getScore(win, lose):
	'''print on screen the score'''
	#OPCS:
	length = 30 # Must be even
	up_down_symbol = "-" #len() must be even
	lateral_symbol = "-" 
	# ==== end OPCS
	msg = "Aciertos: %d\tFallos: %d" % (win, lose)
	w = (length-len(msg)-4-len(lateral_symbol)*2)/2
	length = length/len(up_down_symbol)
	print "\t\t" + up_down_symbol * length
	print "\t\t" + lateral_symbol, " " * w, msg, " " * w, lateral_symbol
	print "\t\t" + up_down_symbol * length

def nrandom(top, how_many_questions):
	'''
		Take a top (number of questions on the file) and a number of desire
	 	questions and return a random list of numbers
	'''
	a = [n for n in range(1,top+1)]
	shuffle(a)
	return a[:how_many_questions]

class Question(object):
	''' Question Class '''
	lettopc = {0:"a",1:"b",2:"c",3:"d",4:"e"}
	opclett = {"a":0,"b":1,"c":2,"d":3,"e":4}
	def __init__(self, num, quest, a1, a2, a3, a4, a5, answer):
		self.num = num
		self.quest = quest
		self.a1 = a1
		self.a2 = a2
		self.a3 = a3
		self.a4 = a4
		self.a5 = a5
		self.options = [a1,a2,a3,a4,a5]
		self.answer = answer
		self.answer_str = self.options[self.opclett[answer]]

def doQuiz(questions_str):
	'''The core main of Quiz'''
	top = int(questions_str[-1][0])

	print ""
	hmq = 0
	while hmq <= 0 or hmq > top:
		printt(u"Cuántas preguntas quieres contestar [1 hasta %d]: " % top)
		hmq = raw_input()
		if not hmq.isdigit(): continue
		hmq = int(hmq)
	random_question_number = nrandom(int(questions_str[-1][0]), hmq)

	Q = []
	for number in random_question_number:
		Q.append(Question(int(questions_str[number][0]),questions_str[number][1],questions_str[number][2],
							questions_str[number][3],questions_str[number][4],questions_str[number][5],
							questions_str[number][6],questions_str[number][7].strip()))

	win = lose = 0
	b = 1
	for q in Q:
		doFormat()
		getScore(win, lose)
		print "Pregunta nº %d:" % b
		b += 1
		print "\t"+ q.quest
		print "Opciones:"
		for i in range(len(q.options)):
			print "\t" + q.lettopc[i] + ")", q.options[i]
		print ""
		answer = get_answer("Tu respuesta: ")
		#answer_str = questions[number][opclett[questions[number][7].strip()]]
		if answer == q.answer:
			win += 1
			print "\t\tTu respuesta es: Correcta!!"
		else:
			print "\t\tTu respuesta es: Incorrecta :("
			print "Respuesta Correcta:\n\t%s) %s" % (q.answer, q.answer_str)
			lose += 1
		raw_input()
	doFormat()
	getScore(win,lose)

	print "\nNo hay mas preguntas"
	print "\nResumen:"
	print "\tRespuestas correctas:", str(win)
	printt(u"\tRespuestas erróneas :", str(lose))
	nota = ((10.0000/hmq)*win-(10.0000/60)*lose)
	if nota < 0.00: nota = 0.00
	print "\n\tNota: %.2f\tHas Aprobado! :)" % nota if nota > 5.00 else "\n\tNota: %.2f\tHas Suspendido! :)" % nota

def getQuestionsFromFile(File):
	'''Take an file and return the questions in list of list format'''
	quest = []
	try:
		f = open(File)
	except IOError:
		if win32:
			print "No se encuentra el fichero con las preguntas:", File
			sys.exit()
		else:
			sys.exit("No se encuentra el fichero con preguntas: %s" % File)
	
	quest.append(["Skip this line"])
	while True:
		line = f.readline()
		if not line: break
		else:
			tmp = line.split("*")
			quest.append(tmp)
	f.close()
	return quest


if __name__ == "__main__":
	if len(sys.argv) == 2: File = sys.argv[1]
	elif len(sys.argv) == 1: File = FILE
	else: usage()
	questions_str = getQuestionsFromFile(File)
	try:
		doFormat()
		print ""
		opc = ""
		while opc != "s" and opc != "n":
			opc = raw_input("Empezamos(s/n)?: ")
			if opc == "s": break
			if opc == "n": sys.exit("\nBye!")
		opc = "s"
		while opc == "s":
			doFormat()
			opc = ""
			doQuiz(questions_str)
			while opc != "s" and opc != "n":
				printt(u"\n\nQuiéres hacer otro test (s/n): ")
				opc = raw_input()
				if opc == "n":
					if win32(): win32end()
					else: print "\nOK, Bye!"
	except KeyboardInterrupt:
		if win32():
			print "\nOK, Bye!"
			win32end()
		else:
			sys.exit("\nOK, Bye!")
