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

aliases = db.query("""SELECT source as username, name as domain, destination
FROM mailaliases, users, domains
WHERE mailaliases.id_users = users.id
AND mailaliases.domain_id = domains.id
AND users.login = $user
ORDER BY source""", vars=locals())

print 'total %s' % len(aliases)

for alias in aliases:
	if not alias.username:
		username = '*'
	else:
		username = alias.username
	destinations = alias.destination.split(',')
	print '%s@%s -> %s' % (username, alias.domain, ', '.join(destinations))
