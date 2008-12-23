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

while True:
	domain = text('Nom de domaine du site à supprimer :')
	if re.match(r'^([a-zA-Z0-9_\-]+\.)+(fr|be|eu|com|org|net|info|name)$', domain):
		break

sites = db.query("""SELECT websites.id, domains.name, websites.enabled
                FROM `domains`, `websites`, `users`
                WHERE domains.id = websites.id_domains
                AND users.id = websites.id_users
                AND users.login = '%s'
		AND domains.name = '%s'""" % (user, domain))

if len(sites) == 0:
	print 'Ce site n\'a pas l\'air d\'exister, navré.'
	sys.exit()

site_id = list(sites)[0].id

typed = ''

while typed != 'oui, vraiment!' and typed != 'non':
	typed = text('Voulez vous VRAIMENT supprimer %s ? Ceci est irréversible.\nTapez "oui, vraiment!" si c\'est le cas, ou "non" dans le cas contraire :' % domain)

if typed == 'non':
	sys.exit()

path = '/home/%s/%s' % (user, domain)
log_path = '/home/%s/logs/%s' % (user, domain)

delete_files = choices('Supprimer aussi les fichiers dans %s ?' % path, dict(o=True,n=False), default='n')
delete_logs = choices('Supprimer également les logs dans %s ?' % log_path, dict(o=True,n=False), default='n')

db.delete('websites', where='id = $site_id', vars=locals())

os.system('/beadmin/restart-lighttpd.sh')

if delete_files:
	os.system('rm -Rf %s' % path)
if delete_logs:
	os.system('rm -Rf %s' % log_path)

print '%s a été supprimé !' % domain
