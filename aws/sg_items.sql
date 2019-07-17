CREATE TABLE `sg_items` (
  `sn` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `date` date DEFAULT NULL,
  `sg_name` varchar(255) DEFAULT NULL,
  `sg_id` varchar(64) DEFAULT NULL,
  `direction` varchar(10) DEFAULT NULL,
  `protocol` varchar(20) DEFAULT NULL,
  `port` varchar(10) DEFAULT NULL,
  `ip` varchar(20) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `reg_time` datetime DEFAULT NULL,
  PRIMARY KEY (`sn`),
  KEY `date` (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

