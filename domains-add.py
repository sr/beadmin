#!/usr/bin/env python
#-*- coding: utf8 -*-

from dialog import *
import database as db
import dbconf
import re
import sys
import os

if os.environ.has_key('SUDO_USER'):
        user =  os.environ['SUDO_USER']
else:
        user = 'root'

userfromdb = db.select('users', where="login = '%s'" % user)
if len(userfromdb) == 0:
	print 'Votre utilisateur n\'a pas été autorisé à utiliser cet outil.'
	print 'Merci de contacter l\'administrateur.'
	sys.exit()

id_user = list(userfromdb)[0].id

while True:
	domain = text('Nom de domaine du site :')
	if re.match(r'^([a-zA-Z0-9_\-]+\.)+(fr|com|org|net|info|name|be|eu)$', domain):
		break

domains = db.select('domains', where="name = '%s'" % domain)

if len(domains) == 0:
	db.insert('domains', name=domain)
	print 'Domaine ajouté !'
else:
	print 'Ce domaine existe déjà.'
