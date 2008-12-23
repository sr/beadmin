#!/usr/bin/env python

import random
import os
import tempfile
import sys
from getpass import getpass

def choices(title, choices, default=None):
	typed = ''
	choices = dict([(k.lower(), v) for k, v in choices.items()])
	default = default.lower()
	try:
		while not typed.lower() in [c for c in choices.keys()]:
			print '\033[1m%s\033[0m [%s]' % (title, '/'.join([d.upper() for d in [default] if d != None] + [c for c in choices.keys() if c != default])),
			typed = raw_input()
			if not typed and default: typed = default
	except KeyboardInterrupt:
		print
		sys.exit()
	return choices[typed.lower()]
		
def text(title, default=None):
	try:
		while True:
			print '\033[1m%s\033[0m' % title,
			if default: print '[%s]' % default,
			typed = raw_input()
			if not typed and not default: continue
			elif not typed:
				typed = default
				break
			else: break
	except KeyboardInterrupt:
		print
		sys.exit()
	return typed

def passwd(title, default=None):
	try:
		while True:
			print '\033[1m%s\033[0m' % title,
			if default: print '[%s]' % default,
			typed = getpass('')
			if not typed and not default: continue
			elif not typed:
				typed = default
				break
			else: break
	except KeyboardInterrupt:
		print
		sys.exit()
	return typed


def nanoide(filling='', filename='', pathtonano='nano'):
        '''Fonction qui retourne le texte soumis par l'utilisateur avec nano.
        L'argument filling permet de pre-remplir nano avec du texte (instructions, etc...)'''

        # Definition du fichier :
        if filename == '':
                filename = tempfile.mktemp(suffix='-nanoide')

        # Creation du fichier

        file = open(filename, 'w')
        file.write(filling)
        file.close()

        # ouverture de nano
        os.system('%s %s' % (pathtonano, filename))

        # Recuperation du fichier

        file = open(filename, 'r')
        filecontent = ''.join(file.readlines())
        file.close()

        os.remove(filename)

        return filecontent

