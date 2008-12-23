#!/usr/bin/env python
#-*- coding: utf8 -*-

from dialog import *
import database as db
import dbconf
import re
import sys
import os
from md5 import md5

class Email:
	def __init__(self, email):
		self.email = email
	
	def get_domain(self):
		if self.email:
			return self.email.split('@')[1]
	
	def get_username(self):
		if self.email:
			return self.email.split('@')[0]

	def is_well_formatted(self):
		return re.match(r'''^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$''', self.email)


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

is_catchall = choices('Voulez vous créer un catch-all ?', dict(o=True, n=False), default='n')

print

if is_catchall:
	while True:
		email = text('Nom de domaine de l\'adresse :')
		if re.match(r'^([a-zA-Z0-9_\-]+\.)+(fr|com|be|org|net|info|name)$', email):
			email = '@' + email
			break
else:
	while True:
		email = text('Email à créer :')
		if re.match(r'''^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$''', email):
			break

email_source = Email(email)

destinations = []

print
print 'Vous allez maintenant ajouter les adresses de destinations.'
print 'Quand vous aurez terminé la saisie, tapez ^D pour valider.'
print 

while True:
	try:
		email = text('Adresse email de destination à ajouter :')
	except EOFError:
		print 'Fin !'
		break
	if re.match(r'''^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$''', email):
		destinations.append(Email(email))
		print ' -> Adresse ajoutée !'

if len(destinations) == 0:
	print 'Aucune adresse ajoutée à la liste, annulation...'
	print
	sys.exit()

print
print 'Création de la redirection depuis %s vers :' % email_source.email
for destination in destinations:
	print ' -> %s' % destination.email
print

domains = db.select('domains', where='name = $email_source.get_domain()', vars=locals())

if len(domains) == 0:
	id_domain = db.insert('domains', name=email_source.get_domain())
else:
	id_domain = list(domains)[0].id

db.insert('mailaliases', domain_id=id_domain, source=email_source.get_username(), destination=','.join([e.email for e in destinations]), id_users=id_user)

print 'Effectué !'
print
