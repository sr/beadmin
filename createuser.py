#!/usr/bin/env python
#-*- coding: utf8 -*-

from dialog import *
import database as db
import dbconf
import re
import sys
import os
import pwgen

login = sys.argv[1]
password = pwgen.Pwgen().returnPwgen(8, useCapital=1, useNumeral=1, notAmbiguousChars=1)

os.system('usermod -p `mkpasswd %s` %s' % (password, login))
db.insert('users', login=login)

print db.query("""GRANT USAGE
	ON * . *
	TO '""" + login + """' @'%%'
	IDENTIFIED BY '""" + password + """' 
	WITH MAX_QUERIES_PER_HOUR 0 
	MAX_CONNECTIONS_PER_HOUR 0 
	MAX_UPDATES_PER_HOUR 0 
	MAX_USER_CONNECTIONS 0 ;""")

print 'Utilisateur %s créé' % login
print 'Mot de passe : "%s"' % password
