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
	email = text('Adresse email à modifier :')
	if re.match(r'''^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$''', email):
		break

(username, domain) = email.split('@')

password = passwd('Nouveau mot de passe :')

mailboxes = db.query('''SELECT mailboxes.id
FROM mailboxes, domains
WHERE mailboxes.domain_id = domains.id
AND id_users = $id_user
AND name = $domain
AND user = $username''', vars=locals())

if len(mailboxes) == 0:
	print 'Cette adresse mail n\'existe pas !'
	print
	sys.exit()

mailbox_id = list(mailboxes)[0].id

db.update('mailboxes', password=md5(password).hexdigest(), where='id = $mailbox_id', vars=locals())

print 'Le mot de passe pour la boite mail `%s@%s`' % (username, domain)
print 'a été changé pour `%s`.' % password
