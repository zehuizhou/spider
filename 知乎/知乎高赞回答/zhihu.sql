CREATE TABLE `topic` (
  `id` bigint(20) NOT NULL COMMENT '话题id',
  `title` varchar(255) DEFAULT NULL COMMENT '话题名称',
  `img_url` text COMMENT '图片链接',
  `ranking` int(11) DEFAULT NULL COMMENT '排名',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

