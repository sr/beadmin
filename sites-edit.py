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
        print 'Votre utilisateur n\'a pas été autorisé à avoir un site.'
        print 'Merci de contacter l\'administrateur.'
        sys.exit()

id_user = list(userfromdb)[0].id

if len(sys.argv) > 1:
	default = sys.argv[1]
else:
	default = ""

while True:
       	domain = text('Nom de domaine du site à éditer :', default)
       	if re.match(r'^([-a-zA-Z0-9_]+\.)+(fr|eu|cc|com|org|net|info|name|be)$', domain):
               	break
	default = ""

sites = db.query("""SELECT websites.*, domains.name
	FROM websites, domains
	WHERE websites.id_domains = domains.id
	AND domains.name = '%s'
	AND websites.id_users = '%s'""" % (domain, id_user))

if len(sites) == 0:
	print 'Aucun site portant ce domaine n\'existe sous votre nom'
	sys.exit()

site = list(sites)[0]

site_id = site.id
try:
	if site.enabled == "yes":
		enabled = choices('Voulez-vous Éditer ou Désactiver le site ?', dict(e='edit', d='no'), default='e')
	else:
		enabled = choices('Voulez-vous Éditer ou Activer le site ?', dict(e='edit', a='yes'), default='e')
except KeyboardInterrupt:
        print
        sys.exit()

if enabled == "edit":
	config = editor(filling=site.config.encode('utf8')).decode('utf8')
	db.update('websites', where='id = $site_id', config=config, vars=locals())
	print 'La configuration de %s a été mise à jour.' % domain
else:
	db.update('websites', where='id = $site_id', enabled=enabled, vars=locals())
	print 'Le site %s a été %s' % (domain, {'yes':'activé', 'no':'désactivé'}[enabled])

print 'N\'oubliez pas de relancer Lighttpd pour l\'appliquer'
print 'avec restart-lighttpd.'
