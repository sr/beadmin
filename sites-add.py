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
	domain = text('Nom de domaine du site :')
	if re.match(r'^([a-zA-Z0-9_\-]+\.)+(fr|cc|com|org|net|info|name|be|eu)$', domain):
		break

domains = db.select('domains', where="name = '%s'" % domain)

if len(domains) == 0:
	id_domain = db.insert('domains', name=domain)
else:
	id_domain = list(domains)[0].id
	if len(db.select('websites', where="id_domains = '%s'" % id)) == 1:
		print 'Ce domaine possède déjà une configuration sur Lighttpd'
		sys.exit()

msg = '''# Configurez ici votre hôte virtuel avec les instructions de
# configuration de lighttpd (voir la doc).
# Si le site est un site PHP, cette étape est souvent inutile.
# En cas de doutes, contactez un administrateur.'''

if len(db.select('websites', where="id_domains = '%s'" % id_domain)) == 1:
	print 'Le domaine %s possède déjà une configuration sur Lighttpd' % domain
	sys.exit()

config = editor(filling=msg).decode('utf8')

if len(db.select('websites', where="id_domains = '%s'" % id_domain)) == 1:
	print 'Erreur : une configuration a été crée pour %s pendant que vous éditiez ce fichier' % id_domain
	sys.exit(1)

enabled = choices('Activer la nouvelle configuration ?', dict(o='yes', n='no'), default='o')
db.insert('websites', enabled=enabled, config=config, id_domains=id_domain, id_users=id_user)

path = '/home/%s/%s' % (user, domain)
log_path = '/home/%s/logs/%s' % (user, domain)

try:
	os.mkdir(path)
        os.mkdir(log_path)
except:
	print 'Attention : impossible de créer automatiquement le répertoire' 
	print '            merci de contacter un administrateur'

os.system('chown -R %s:www-data "%s" "%s"' % (user, path, log_path))
os.system('chmod ug+rwx,o-rwx "%s" "%s"' % (path, log_path))

print 'Le domaine est maintenant configuré sur Lighttpd !1'
print 'Le chemin vers les fichiers est %s' % (path)
print 'Le groupe www-data doit pouvoir lire et écrire dans ce répertoire,'
print 'les permissions adéquoites ont été crées, merci de faire attention'
print 'les garder quand vous copierez les fichiers dans le répertoire.'
print
print 'N\'oubliez pas de relancer Lighttpd pour l\'appliquer'
print 'avec restart-lighttpd.'

