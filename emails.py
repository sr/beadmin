#!/usr/bin/env python
#-*- coding: utf8 -*-

#from dialog import *
import database as db
import dbconf
import os

if os.environ.has_key('SUDO_USER'):
	user =  os.environ['SUDO_USER']
else:
	user = 'root'

emails = db.query("""SELECT user, name as domain
FROM mailboxes, domains, users
WHERE mailboxes.domain_id = domains.id
AND mailboxes.id_users = users.id
AND users.login = $user
ORDER BY domain, user""", vars=locals())

print 'total %s' % len(emails)

for email in emails:
	print '%s@%s' % (email.user, email.domain)
