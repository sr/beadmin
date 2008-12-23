#!/bin/bash

cp /etc/lighttpd/lighttpd-mysql.conf /etc/lighttpd/lighttpd-mysql.conf.bak
python /beadmin/lighttpd-mysql-config.py > /etc/lighttpd/lighttpd-mysql.conf

echo `date` Lighttpd restarted by $SUDO_USER >> /var/log/restart-lighttpd.log

/etc/init.d/lighttpd reload

if [ "$?" != "0" ] ; then
	echo "Une erreur à eu lieu lors de l'application de votre configuration."
	echo "L'ancienne configuration a été restorée, merci de corriger vos modifications."
	cp /etc/lighttpd/lighttpd-mysql.conf.bak /etc/lighttpd/lighttpd-mysql.conf
	/etc/init.d/lighttpd reload
	echo `date` Lighttpd restart by $SUDO_USER failed. Restarting with old configuration file >> /var/log/restart-lighttpd.log
fi
