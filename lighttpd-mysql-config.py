#!/usr/bin/env python
#-*- coding: utf-8 -*-

from dbconf import *
import database as db
import os
import re

confs = db.query("""SELECT domains.name, websites.config, users.login
	FROM domains, websites, users
	WHERE domains.id = websites.id_domains
	AND users.id = websites.id_users
	AND websites.enabled = 'yes'""")

for conf in confs:
	path = '/home/%s/%s' % (conf.login, conf.name)
        log_path = '/home/%s/logs/%s' % (conf.login, conf.name)

	os.system('mkdir -p "%s"' % log_path)
	os.system('chown -R %s:www-data "/home/%s/logs/"' % (conf.login, conf.login))	
	os.system('chmod -R ug+rwx,o-rwx "/home/%s/logs/"' % conf.login)

	print """
$HTTP["host"] == "%s" {
	server.document-root = "%s/"
	accesslog.filename = "%s/access.log"
	%s
}""" % (conf.name, path, log_path, re.sub("\n", "\n\t", conf.config))
