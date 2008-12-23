#!/usr/bin/env python
#-*- coding: utf8 -*-

from dialog import *
import database as db
import dbconf
import re
import sys
import os
from md5 import md5

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
	email = text('Adresse email à ajouter :')
	if not re.match(r'''^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$''', email):
		print "Ça ne ressemble pas à une adresse email, veuillez réessayer"
	else:
		break

(username, domain) = email.split('@')

password = passwd('Mot de passe :')

domains = db.select('domains', where='name = $domain', vars=locals())

if len(domains) == 0:
	id_domain = db.insert('domains', name=domain)
else:
	id_domain = list(domains)[0].id

if len(db.select('mailboxes', where='domain_id = $id_domain AND user = $username', vars=locals())) > 0:
	print 'Cette boite mail existe déjà !'
	print
	sys.exit()

db.insert('mailboxes', domain_id=id_domain, user=username, password=md5(password).hexdigest(), id_users=id_user)

print 'La nouvelle boite mail est maintenant configurée.'
print 'Pour accéder aux services associer, vos identifiants sont :'
print ' - login : %s@%s' % (username, domain)
print ' - mot de passe : %s' % password
print 'Services disponibles :'
print ' - SMTP / SMTPS (necessite une authentification) : mail.bearnaise.net'
print ' - IMAP / IMAPS : mail.bearnaise.net'
#print ' - POP3 / POP3S' # Plus tard
