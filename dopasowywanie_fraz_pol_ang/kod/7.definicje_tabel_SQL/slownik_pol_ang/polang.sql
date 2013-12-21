DROP TABLE IF EXISTS `polang`.`statistics_pol`;
DROP TABLE IF EXISTS `polang`.`statistics_ang`;
DROP TABLE IF EXISTS `polang`.`description`;
DROP TABLE IF EXISTS `polang`.`gender`;
DROP TABLE IF EXISTS `polang`.`dictonary`;


CREATE TABLE `polang`.`statistics_pol` (
  `id` bigint(20) NOT NULL auto_increment,
  `frequency` int(11) NOT NULL default '0',
  `word1` varchar(25) default NULL,
  `word2` varchar(25) default NULL,
  `word3` varchar(25) default NULL,
  `word4` varchar(25) default NULL,
  `word5` varchar(25) default NULL,
  `word6` varchar(25) default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin2

CREATE TABLE `polang`.`statistics_ang` (
  `id` bigint(20) NOT NULL auto_increment,
  `frequency` int(11) NOT NULL default '0',
  `word1` varchar(25) default NULL,
  `word2` varchar(25) default NULL,
  `word3` varchar(25) default NULL,
  `word4` varchar(25) default NULL,
  `word5` varchar(25) default NULL,
  `word6` varchar(25) default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin2


CREATE TABLE `polang`.`description` (
  `id_description` int(8) unsigned NOT NULL,
  `description` varchar(50) NOT NULL,
  PRIMARY KEY  (`id_description`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;

CREATE TABLE `polang`.`dictionary` (
  `id_word` int(15) unsigned NOT NULL auto_increment,
  `word` varchar(100) default NULL,
  `translation` varchar(100) default NULL,
  `id_description` int(8) default NULL,
  `id_gender` int(8) default NULL,
  PRIMARY KEY  (`id_word`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin2;


CREATE TABLE `polang`.`gender` (
  `id_gender` int(8) unsigned NOT NULL,
  `gender` varchar(50) NOT NULL default '',
  PRIMARY KEY  (`id_gender`)
) ENGINE=MyISAM DEFAULT CHARSET=latin2;


