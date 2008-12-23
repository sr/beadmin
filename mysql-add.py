#!/usr/bin/env python
#-*- coding: utf8 -*-

from dialog import *
import database as db
import dbconf
import re
import sys
import os

_GOOD_LETTERS = 'azertyuiopqsdfghjklmwxcvbnAZERTYUIOPQSDFGHJKLMWXCVBN1234567890_-'

def valid_dbname(text):
	if len(text) >= 1 and len(text) < 30:
		for l in text:
			if not l in _GOOD_LETTERS:
				return False
		return True
	else:
		return False
				

if os.environ.has_key('SUDO_USER'):
        user =  os.environ['SUDO_USER']
else:
        user = 'root'

userfromdb = db.select('users', where="login = '%s'" % user)
if len(userfromdb) == 0:
	print 'Votre utilisateur n\'a pas été autorisé à avoir un site.'
	print 'Merci de contacter l\'administrateur.'
	sys.exit()

id_user = list(userfromdb)[0].id

while True:
	dbname = text('Suffixe du nom de la base de donnée :')
	if valid_dbname(dbname): break
	else:
		print 'Le suffixe doit utiliser les caractères `a-z A-Z 0-9 _ et -`, et'
		print 'ne doit pas dépasser les 30 caractères.'

dbs = db.select('bases', where="name = '%s' AND id_users='%s'" % (dbname, id_user))

if len(dbs) == 0:
	id_base = db.insert('bases', name=dbname, id_users=id_user)
	db.query('CREATE DATABASE `%s_%s`;' % (user, dbname))
	db.query("GRANT ALL PRIVILEGES ON `" + user + "_" + dbname + "` . * TO '" + user + "'@'%%' WITH GRANT OPTION;")
else:
	print 'Cette base de donnée existe déjà !'
	sys.exit()

print
print 'La base de donnée a été crée sur MySQL.'
print
print 'Le serveur est accessible via `localhost` et `mysql.bearnaise.net`'
print 'ou `mysql.votredomaine.tld`.'
print 'Le nom de la base de donnée est `%s_%s`.' % (user, dbname)
print 'Votre nom d\'utilisateur mysql est `%s`.' % (user)
print 'Votre mot de passe est celui qui vous a été envoyé précédement.'
print
print 'Vous pouvez accéder à PHPMyAdmin en suivant ce lien :'
print 'http://mysql.bearnaise.net/'
