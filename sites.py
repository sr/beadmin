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

sites = db.query("""SELECT domains.name, websites.enabled
		FROM `domains`, `websites`, `users`
		WHERE domains.id = websites.id_domains
		AND users.id = websites.id_users
		AND users.login = '%s'""" % user)

print 'total %s' % len(sites)
for site in sites:
	print '%s dans %s %s' % (site.name, '/home/%s/%s/' % (user, site.name), {'yes':'','no':u'(désactivé)'}[site.enabled])
