CREATE TABLE `bases` (
  `id_users` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  PRIMARY KEY  (`id_users`,`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `domains` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=99 ;

CREATE TABLE `mailaliases` (
  `id` int(11) NOT NULL auto_increment,
  `domain_id` int(11) NOT NULL,
  `source` varchar(40) NOT NULL,
  `destination` varchar(80) NOT NULL,
  `id_users` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `domain_id` (`domain_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=58 ;

CREATE TABLE `mailboxes` (
  `id` int(11) NOT NULL auto_increment,
  `domain_id` int(11) NOT NULL,
  `user` varchar(40) NOT NULL,
  `password` varchar(32) NOT NULL,
  `id_users` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `UNIQUE_EMAIL` (`domain_id`,`user`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=31 ;

CREATE TABLE `rr` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `zone` int(10) unsigned NOT NULL,
  `name` char(64) NOT NULL,
  `type` enum('A','AAAA','ALIAS','CNAME','HINFO','MX','NAPTR','NS','PTR','RP','SRV','TXT') default NULL,
  `data` char(128) NOT NULL,
  `aux` int(10) unsigned NOT NULL,
  `ttl` int(10) unsigned NOT NULL default '86400',
  PRIMARY KEY  (`id`),
  UNIQUE KEY `rr` (`zone`,`name`,`type`,`data`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=292 ;

CREATE TABLE `soa` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `origin` char(255) NOT NULL,
  `ns` char(255) NOT NULL,
  `mbox` char(255) NOT NULL,
  `serial` int(10) unsigned NOT NULL default '1',
  `refresh` int(10) unsigned NOT NULL default '28800',
  `retry` int(10) unsigned NOT NULL default '7200',
  `expire` int(10) unsigned NOT NULL default '604800',
  `minimum` int(10) unsigned NOT NULL default '86400',
  `ttl` int(10) unsigned NOT NULL default '86400',
  PRIMARY KEY  (`id`),
  UNIQUE KEY `origin` (`origin`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=41 ;

CREATE TABLE `users` (
  `id` int(11) NOT NULL auto_increment,
  `login` varchar(20) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `login` (`login`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=16 ;

CREATE TABLE `websites` (
  `id` int(11) NOT NULL auto_increment,
  `enabled` enum('yes','no') character set latin1 NOT NULL,
  `config` longtext character set latin1 NOT NULL,
  `id_domains` int(11) NOT NULL,
  `id_users` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `id_domains` (`id_domains`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=93 ;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `bearnaise`.`view_mailaliases` AS select concat(`bearnaise`.`mailaliases`.`source`,_latin1'@',`bearnaise`.`domains`.`name`) AS `email`,`bearnaise`.`mailaliases`.`destination` AS `destination` from (`bearnaise`.`mailaliases` left join `bearnaise`.`domains` on((`bearnaise`.`mailaliases`.`domain_id` = `bearnaise`.`domains`.`id`)));

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `bearnaise`.`view_mailboxes` AS select concat(`bearnaise`.`mailboxes`.`user`,_latin1'@',`bearnaise`.`domains`.`name`) AS `email`,`bearnaise`.`mailboxes`.`password` AS `password` from (`bearnaise`.`mailboxes` left join `bearnaise`.`domains` on((`bearnaise`.`mailboxes`.`domain_id` = `bearnaise`.`domains`.`id`)));


ALTER TABLE `mailaliases`
  ADD CONSTRAINT `mailaliases_ibfk_1` FOREIGN KEY (`domain_id`) REFERENCES `domains` (`id`) ON DELETE CASCADE;

ALTER TABLE `mailboxes`
  ADD CONSTRAINT `mailboxes_ibfk_1` FOREIGN KEY (`domain_id`) REFERENCES `domains` (`id`) ON DELETE CASCADE;
