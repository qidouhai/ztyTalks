SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for repair_service_sheet
-- ----------------------------
DROP TABLE IF EXISTS `talks_sheet`;
CREATE TABLE `talks_sheet` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `username` varchar(128) NOT NULL COMMENT '用户',
  `openid` varchar(128)  NOT NULL COMMENT 'openid',
  `status` tinyint(11) DEFAULT NULL COMMENT '发布状态',
  `publish` tinyint(11) DEFAULT 0 COMMENT '权限',
  `publishDate` int(11) DEFAULT NULL COMMENT '发布时间',
  `description` text  DEFAULT NULL COMMENT '说说内容',
  `mediaUrl` text  DEFAULT NULL COMMENT '媒体资源',
  `thumbUp` int(11) DEFAULT 0 COMMENT '点赞',
  `label` varchar(128) NOT NULL DEFAULT "默认标签" COMMENT '标签',
  `location` varchar(128) DEFAULT NULL COMMENT '发布位置',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

SET FOREIGN_KEY_CHECKS = 1;

