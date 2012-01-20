#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Examinator Python's Version by aabilio
# aabilio [at] gmail [dot] com

import sys
import os
import codecs
from random import shuffle

#OPCs:
FILE = "preguntas.txt" # Path to the file
NAME = "Examinator" # Program's name
VERSION = "2.0" # Program's version
PRESENTATION = "%s - %s" % (NAME,VERSION) # Presentation on doFromat()
# ==== End OPCs

def win32():
	if sys.platform == "win32": return True
	else: return False
def cls():
	if win32(): os.system("cls")
	else: os.system("clear")
def Win32end():
	raw_input("[PROGRAM END - ENTER TO EXIT]")

def printt(*msg):
    '''
    	Take a string and display it on screen with right format for win32 or *nix (spanish)
        Like a built in print python function:
        - Concatenations: '+' o ','
        - Use variables directly or by using format specifiers
        - Always use the "u" unicode
        - printt(), unlike built in print python function, does not print an adiciaonal newline character
        - Examples:
        	* printt(u"Hi! %s you're user number %d" % (user, 925))
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

def getScore(win, lose, nkna):
	'''print on screen the score'''
	#OPCS:
	length = 44 # Must be even
	up_down_symbol = "-" #len() must be even
	lateral_symbol = "-" 
	# ==== end OPCS

	## Do not edit anything from here (unless you know what you're doing)
	msg = "Aciertos: %d\t  Fallos: %d\tNSNC: %d" % (win, lose, nkna)
	w = (length-len(msg)-4-len(lateral_symbol)*2)/6
	#length = length/len(up_down_symbol)
	print "\t" + up_down_symbol * length
	print "\t" + lateral_symbol, " " * w, msg, " " * w, lateral_symbol
	print "\t" + up_down_symbol * length

def nrandom(top, how_many_questions):
	'''Take a top and a number of questions and return list of numbers'''
	a = [n for n in range(1,top+1)]
	shuffle(a)
	return a[:how_many_questions]

class BadFileFormat(Exception):
	def __init__(self, text, msg = None, line = None):
		self.__text = text
		self.__msg = msg if msg is not None else None
		self.__line = str(line) if line is not None else "Unknow line"
	def __str__(self):
		return self.__msg + " %s --> %s" % (self.__line, self.__text) if self.__msg is not None else "General Format Error on line: %s --> %s" % (self.__line, self.__text)

class Question(object):
	lettopc = {0:"a",1:"b",2:"c",3:"d",4:"e"}
	opclett = {"a":0,"b":1,"c":2,"d":3,"e":4}
	def __init__(self, num, comment, quest, a1, a2, a3, a4, a5, answer):
		self.num = num
		if type(comment) is unicode:
			self.comment = comment if not comment.isspace() else None
		else:
			self.comment = None
		self.quest = quest
		self.a1 = a1 if a1 is not u"" else None
		self.a2 = a2 if a2 is not u"" else None
		self.a3 = a3 if a3 is not u"" else None
		self.a4 = a4 if a4 is not u"" else None
		self.a5 = a5 if a5 is not u"" else None
		self.options = [self.a1,self.a2,self.a3,self.a4,self.a5]
		self.options_let = [self.lettopc[n] for n in range(len(self.options)) if self.options[n] is not None]
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
		Q.append(Question(int(questions_str[number-1][0]),questions_str[number-1][1],questions_str[number-1][2],
							questions_str[number-1][3],questions_str[number-1][4],questions_str[number-1][5],
							questions_str[number-1][6],questions_str[number-1][7],
							questions_str[number-1][8].strip()))

	win = lose = nkna = 0
	b = 1
	for q in Q:
		doFormat()
		getScore(win, lose, nkna)
		printt(u"Pregunta nº %d:\n" % b)
		b += 1
		printt(u"\t"+ unicode(q.quest) + u"\n")
		if q.comment:
			printt(u"Comentario:\n\t%s\n" % q.comment)
		print "Opciones:"
		for i in range(len(q.options)):
			if q.options[i] is not None:
				printt(u"\t" + unicode(q.lettopc[i]) + ")", unicode(q.options[i]) + u"\n")
		while(True):
			try:
				answer = raw_input("\nTu respuesta (ENTER para no contestar): ")
				if answer in q.options_let or answer is '': break
				else: printt(u"\t%c) no es una opción disponible." % answer)
			except TypeError:
				printt(u"\tError de tipado en la respuesta")
		if answer == q.answer:
			win += 1
			print "\t\tTu respuesta es: Correcta!!"
		elif answer == '':
			printt(u"\t\tNo has contestado. No se restarán ni sumarán puntos.\n")
			printt(u"La Respuesta Correcta era:\n\t%s) %s\n" % (unicode(q.answer), unicode(q.answer_str)))
			nkna += 1
		else:
			print "\t\tTu respuesta es: Incorrecta :("
			printt(u"Respuesta Correcta:\n\t%s) %s\n" % (unicode(q.answer), unicode(q.answer_str)))
			lose += 1
		raw_input()
	doFormat()
	getScore(win,lose,nkna)
	print "\nNo hay mas preguntas"
	print "\nResumen:"
	print "\tRespuestas correctas :", str(win)
	printt(u"\tRespuestas erróneas  : %s\n" % str(lose))
	printt(u"\tNo contestadas       : %s\n" % str(nkna))
	nota = ((10.0000/hmq)*win-(10.0000/60)*lose)
	if nota < 0.00: nota = 0.00
	if nota > 5.00: printt(u"\n\tNota: %.2f\tHas Aprobado! :)\n" % nota)
	else: printt(u"\n\tNota: %.2f\tHas Suspendido! :(" % nota) 
	#print "\n\tNota: %.2f\tHas Aprobado! :)" % nota if nota > 5.00 else "\n\tNota: %.2f\tHas Suspendido! :)" % nota
	del nota, win, lose

def getQuestionsFromFile(file):
	'''Take an file and return the questions in list of list format'''
	quest = []
	try:
		#f = open(file)
		f = codecs.open(file, encoding="utf-8")
	except IOError:
		if win32:
			print "No se encuentra el fichero con las preguntas:", file
			sys.exit()
		else:
			sys.exit("No se encuentra el fichero con preguntas: %s" % file)

	line_number = 1
	while True:
		line = f.readline()
		if not line: break
		else:
			if line.startswith('#'): continue
			elif line.isspace(): continue
			# ATENCIÓN: Chapuza para no usar expresiones regulares
			elif line.split("*")[0].isdigit():
				if line.find("\*") != -1:
					line = line.replace("\*", "(AsTeRiScO)")
					line = line.replace("*", "(SePaRaDoR)")
					line = line.replace("(AsTeRiScO)", "*")
					tmp = line.split("(SePaRaDoR)")
				else:
					tmp = line.split("*")
				quest.append(tmp)
			else:
				raise BadFileFormat(line, "File Error on line", line_number)
		line_number += 1
	f.close()
	return quest


if __name__ == "__main__":
	if len(sys.argv) > 1: File = sys.argv[1]
	else: File = FILE

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
			questions_str = getQuestionsFromFile(File)
			doQuiz(questions_str)
			while opc != "s" and opc != "n":
				printt(u"\n\nQuiéres hacer otro test (s/n): ")
				opc = raw_input()
				if opc == "n":
					if win32(): Win32end()
					else: print "\nOK, Bye!"
	except KeyboardInterrupt:
		if win32():
			print "\nOK, Bye!"
			Win32end()
		else:
			sys.exit("\nOK, Bye!")