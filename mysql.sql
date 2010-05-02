--
-- Table structure for table `accounts`
--

CREATE TABLE IF NOT EXISTS `accounts` (
  `mobileno` varchar(13) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `service` varchar(8) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `username` varchar(30) COLLATE utf8_unicode_ci DEFAULT NULL,
  `password` varchar(30) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`mobileno`,`service`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `accounts`
--


-- --------------------------------------------------------

--
-- Table structure for table `inbox`
--

CREATE TABLE IF NOT EXISTS `inbox` (
  `id` int(11) NOT NULL,
  `sms_to` varchar(13) COLLATE utf8_unicode_ci DEFAULT NULL,
  `sms_from` varchar(13) COLLATE utf8_unicode_ci DEFAULT NULL,
  `sms_text` varchar(1024) COLLATE utf8_unicode_ci DEFAULT NULL,
  `sms_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `processed` int(1) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `inbox`
--


-- --------------------------------------------------------

--
-- Table structure for table `outbox`
--

CREATE TABLE IF NOT EXISTS `outbox` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sms_to` varchar(13) COLLATE utf8_unicode_ci DEFAULT NULL,
  `sms_from` varchar(13) COLLATE utf8_unicode_ci DEFAULT NULL,
  `sms_text` varchar(1024) COLLATE utf8_unicode_ci DEFAULT NULL,
  `sms_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `processed` int(1) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1050507 ;

--
-- Dumping data for table `outbox`
--


-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE IF NOT EXISTS `users` (
  `mobileno` varchar(13) COLLATE utf8_unicode_ci NOT NULL,
  `password` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`mobileno`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `users`
--
