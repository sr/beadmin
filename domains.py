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

domains = db.query("""SELECT domains.id, domains.name, users.login
	FROM domains
	LEFT JOIN websites ON websites.id_domains=domains.id
	LEFT JOIN users ON websites.id_users=users.id""")

#print 'total %s' % len(domains)

for domain in domains:
	if domain.login == user:
		login = 'vous'
	else:
		login = domain.login
		
	mailboxes = len(db.select('mailboxes', where='domain_id = $domain.id', vars=locals()))
	mailaliases = len(db.select('mailaliases', where='domain_id = $domain.id', vars=locals()))

	if login or mailboxes or mailaliases:
		print '%s,' % domain.name,
	else:
		print domain.name,

	if login:
		print 'hébergé par %s' % login,
		if mailboxes or mailaliases:
			print 'avec',
	
	if mailboxes:
		print '%s boite(s)' % mailboxes,
		if mailaliases:
			print 'et', 
	if mailaliases:
		print '%s alias' % mailaliases,

	print
