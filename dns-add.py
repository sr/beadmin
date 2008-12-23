#!/usr/bin/env python
#-*- coding: utf8 -*-
from dialog import *
import re
import database as db
import dbconf
import datetime
import sys

IPADDR = '88.191.76.4'
IPADDR6 = '2a01:e0b:1:76:2e0:f4ff:fe19:e76b'
MBOX = 'antoine.inaps.org.'

print 'Bienvenue dans l\'assistant de création d\'un nom de domaine'
print 'dans le serveur DNS de bearnaise !'
print

while True:
	domain = text('Nom de domaine (ex: bearnaise.net)')
	if re.match(r'^([a-zA-Z0-9_\-]+\.)+(fr|be|cc|com|org|net|info|name|eu)\.?$', domain):
		break

if not re.match(r'.*\.$', domain): domain += "." # pour NaPs <3

nbsoa = len(db.query("SELECT * FROM soa WHERE origin = '%s'" % domain))
if nbsoa != 0:
	print
	print 'Le nom de domaine est déjà géré par le serveur.'
	sys.exit()

serial = '%d%02d%02d00' % (datetime.date.today().year, datetime.date.today().month, datetime.date.today().day)
id_soa = db.insert('soa', origin=domain, mbox=MBOX, serial=serial, ns='ns.bearnaise.net.')
db.insert('rr', zone=id_soa, type='NS', data='ns.bearnaise.net.', aux=0, name='')
db.insert('rr', zone=id_soa, type='NS', data='nssec.dedibox.fr.', aux=0, name='')
db.insert('rr', zone=id_soa, name=domain, type='A', data=IPADDR, aux=0)
db.insert('rr', zone=id_soa, name=domain, type='AAAA', data=IPADDR6, aux=0)
db.insert('rr', zone=id_soa, name='mysql.'+domain, type='CNAME', data=domain, aux=0)
db.insert('rr', zone=id_soa, name='www.'+domain, type='CNAME', data=domain, aux=0)

mx = choices('Serveur de mail sur bearnaise ?', dict(o=True, n=False), default='o')
spf = False
if mx:
	spf = choices('Activer la protection SPF ?', dict(o=True, n=False), default='n')
joker = choices('Créer aussi *.%s ?' % domain, dict(o=True, n=False), default='o')


if joker:
	db.insert('rr', zone=id_soa, name='*', type='CNAME', data=domain, aux=0)
if mx:
	db.insert('rr', zone=id_soa, name='', aux=10, type='MX', data=domain)
if spf:
	db.insert('rr', zone=id_soa, type='TXT', name='', aux=0, data='v=spf1 a -all')

print
print 'Le nom de domaine a été créé.'
print 'Merci de contacter un administrateur au plus vite pour l\'enregistrement'
print 'DNS secondaire.'
print
print 'Pour rappel, les DNS à configurer chez votre registar sont :'
print ' - primaire : ns.bearnaise.net'
print ' - secondaire : nssec.dedibox.fr'
