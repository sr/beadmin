#!/usr/bin/env python
import os
class PwgenScore:
	def __init__(self):
		self.score = 0
		return None
	
	def calculScore(self, width, useCapital=0, useNumeral=0, useSymbol=0):
		score = 0
		if width > 6: score = score + 1
		if width > 12: score = score + 1
		if width > 30: score = score + 1
		if useCapital: score = score + 2
		if useNumeral: score = score + 2
		if useSymbol: score = score + 3
		
		self.score = score
		return self.score
	
	def returnLastScore(self):
		return self.score

class Pwgen:
	def returnArgLine(self, width, useCapital=0, useNumeral=0, useSymbol=0, useSecureMode=0, notAmbiguousChars=0):
		options = ['--capitalize', '--no-capitalize','--numerals','--no-numerals', '--symbols', '--secure', '--ambiguous', '-1']
		usedOptions = []
		
		if useCapital: usedOptions.append(options[0])
		else: usedOptions.append(options[1])
		
		if useNumeral: usedOptions.append(options[2])
		else: usedOptions.append(options[3])

		if useSymbol: usedOptions.append(options[4])
		if useSecureMode: usedOptions.append(options[5])
		if notAmbiguousChars: usedOptions.append(options[6])
		usedOptions.append(options[7])

		usedOptions.append(str(int(width)))
		usedOptions.append('1')

		return ' '.join(usedOptions)

	def returnPwgen(self, width, useCapital=0, useNumeral=0, useSymbol=0, useSecureMode=0, notAmbiguousChars=0):
		argv = self.returnArgLine(width, useCapital, useNumeral, useSymbol, useSecureMode, notAmbiguousChars)
		pwgenPipe = os.popen('pwgen %s' % (argv))
		print '[pwgen_lib.Pwgen.returnPwgen] Executed : pwgen %s' % (argv)
		return pwgenPipe.readline()[0:-1]
