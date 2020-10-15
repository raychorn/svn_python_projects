/*
MySQL Data Transfer
Source Host: localhost
Source Database: vypertwitz
Target Host: localhost
Target Database: vypertwitz
Date: 5/27/2010 12:42:43 AM
*/

SET FOREIGN_KEY_CHECKS=0;
-- ----------------------------
-- Table structure for bitlys
-- ----------------------------
DROP TABLE IF EXISTS `bitlys`;
CREATE TABLE `bitlys` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `api_login` varchar(64) NOT NULL,
  `api_key` varchar(64) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `indx_api_login` (`api_login`),
  UNIQUE KEY `indx_api_key` (`api_key`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for feeds
-- ----------------------------
DROP TABLE IF EXISTS `feeds`;
CREATE TABLE `feeds` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `username` varchar(64) NOT NULL,
  `password` varchar(64) NOT NULL,
  `last_used` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP,
  `frequency` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `indx_name` (`name`),
  UNIQUE KEY `indx_username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for phrases
-- ----------------------------
DROP TABLE IF EXISTS `phrases`;
CREATE TABLE `phrases` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `phrase_type` tinyint(4) NOT NULL,
  `phrase` varchar(120) NOT NULL,
  `last_used` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `indx_phrase` (`phrase`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for prepositions
-- ----------------------------
DROP TABLE IF EXISTS `prepositions`;
CREATE TABLE `prepositions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `preposition` varchar(32) NOT NULL,
  `last_used` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `indx_prep` (`preposition`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for product_indexes
-- ----------------------------
DROP TABLE IF EXISTS `product_indexes`;
CREATE TABLE `product_indexes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `product` varchar(64) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `indx_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for product_keywords
-- ----------------------------
DROP TABLE IF EXISTS `product_keywords`;
CREATE TABLE `product_keywords` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `indx` int(11) NOT NULL,
  `keyword` varchar(64) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `indx` (`indx`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for products
-- ----------------------------
DROP TABLE IF EXISTS `products`;
CREATE TABLE `products` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `indx` int(11) NOT NULL,
  `asin` varchar(32) NOT NULL,
  `url` varchar(256) NOT NULL,
  `group` varchar(128) NOT NULL,
  `title` varchar(256) NOT NULL,
  `last_used` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `indx_title` (`title`),
  KEY `indx_lastused` (`last_used`),
  KEY `indx` (`indx`),
  KEY `indx_asin` (`asin`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for sources
-- ----------------------------
DROP TABLE IF EXISTS `sources`;
CREATE TABLE `sources` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `source_type` varchar(16) NOT NULL,
  `bitly` int(11) NOT NULL,
  `source` varchar(512) NOT NULL,
  `feed` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `indx_source` (`source`),
  KEY `fkey_bitlys` (`bitly`),
  KEY `fkey_feed` (`feed`),
  CONSTRAINT `fkey_bitlys` FOREIGN KEY (`bitly`) REFERENCES `bitlys` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fkey_feed` FOREIGN KEY (`feed`) REFERENCES `feeds` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for sponsors
-- ----------------------------
DROP TABLE IF EXISTS `sponsors`;
CREATE TABLE `sponsors` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sponsor_type` int(11) NOT NULL,
  `url` varchar(512) NOT NULL,
  `freq_secs` int(11) NOT NULL,
  `last_used` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `indx_url` (`url`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for used_links
-- ----------------------------
DROP TABLE IF EXISTS `used_links`;
CREATE TABLE `used_links` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `source` int(11) NOT NULL,
  `link` varchar(512) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `indx_link` (`link`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records 
-- ----------------------------
