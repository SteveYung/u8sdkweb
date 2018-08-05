/*
Navicat MySQL Data Transfer

Source Server         : 本地打包机
Source Server Version : 80011
Source Host           : 172.16.1.92:3306
Source Database       : u8sdk

Target Server Type    : MYSQL
Target Server Version : 80011
File Encoding         : 65001

Date: 2018-07-30 17:46:56
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for channel
-- ----------------------------
DROP TABLE IF EXISTS `channel`;
CREATE TABLE `channel` (
  `game` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT '数据所属的游戏',
  `id` varchar(35) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '渠道id',
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT '渠道英文缩写',
  `sdk` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT '渠道sdk缩写',
  `desc` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT 'sdk名字',
  `suffix` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '包名',
  `splash` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '闪屏',
  `splash_copy_to_unity` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '闪屏复制',
  `icon` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '图标',
  `gameName` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '游戏中文名',
  `sdkLogicVersionCode` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT 'sdkLogic版本号',
  `sdkLogicVersionName` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT 'sdkLogic版本名',
  `sdkParams` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT '对应channel_sdkParams内的id',
  `params` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT '对应channel_params内的id',
  `operations` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT '对应channel_operations内的id',
  `plugins` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT '对应channel_plugins内的id',
  `sdkVersionCode` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT 'SDK版本号',
  `sdkVersionName` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT 'SDK版本名',
  `third-plugins` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ----------------------------
-- Table structure for channel_currency
-- ----------------------------
DROP TABLE IF EXISTS `channel_currency`;
CREATE TABLE `channel_currency` (
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT '渠道名简写',
  `pluginsName` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT '脚本路径关键变量',
  `paramskey1` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '渠道参数的key1',
  `paramskey2` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '渠道参数的key2',
  `paramskey3` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '渠道参数的key3',
  `paramskey4` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '渠道参数的key4',
  `paramskey5` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '渠道参数的key5',
  `paramskey6` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '渠道参数的key6',
  `paramskey7` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '渠道参数的key7',
  `paramskey8` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '渠道参数的key8',
  `paramskey9` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '渠道参数的key9',
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='渠道通用信息表';

-- ----------------------------
-- Table structure for channel_operations
-- ----------------------------
DROP TABLE IF EXISTS `channel_operations`;
CREATE TABLE `channel_operations` (
  `id` varchar(35) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `type1` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `from1` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `to1` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `type2` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `from2` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `to2` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `type3` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `from3` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `to3` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `type4` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `from4` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `to4` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `type5` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `from5` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `to5` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `type6` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `from6` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `to6` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `type7` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `from7` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `to7` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `type8` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `from8` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `to8` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `type9` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `from9` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `to9` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ----------------------------
-- Table structure for channel_params
-- ----------------------------
DROP TABLE IF EXISTS `channel_params`;
CREATE TABLE `channel_params` (
  `id` varchar(35) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `name1` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `value1` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `required1` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `showName1` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `bWriteInManifest1` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `bWriteInClient1` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `name2` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `value2` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `required2` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `showName2` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `bWriteInManifest2` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `bWriteInClient2` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `name3` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `value3` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `required3` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `showName3` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `bWriteInManifest3` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `bWriteInClient3` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `name4` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `value4` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `required4` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `showName4` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `bWriteInManifest4` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `bWriteInClient4` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `name5` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `value5` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `required5` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `showName5` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `bWriteInManifest5` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `bWriteInClient5` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `name6` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `value6` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `required6` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `showName6` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `bWriteInManifest6` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `bWriteInClient6` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `name7` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `value7` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `required7` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `showName7` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `bWriteInManifest7` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `bWriteInClient7` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `name8` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `value8` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `required8` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `showName8` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `bWriteInManifest8` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `bWriteInClient8` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `name9` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `value9` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `required9` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `showName9` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `bWriteInManifest9` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `bWriteInClient9` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ----------------------------
-- Table structure for channel_plugins
-- ----------------------------
DROP TABLE IF EXISTS `channel_plugins`;
CREATE TABLE `channel_plugins` (
  `id` varchar(35) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `name1` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `type1` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `name2` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `type2` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `name3` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `type3` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `name4` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `type4` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `name5` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `type5` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `name6` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `type6` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `name7` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `type7` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `name8` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `type8` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `name9` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `type9` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ----------------------------
-- Table structure for channel_sdkParams
-- ----------------------------
DROP TABLE IF EXISTS `channel_sdkParams`;
CREATE TABLE `channel_sdkParams` (
  `id` varchar(35) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `key1` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `value1` varchar(2048) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `key2` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `value2` varchar(2048) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `key3` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `value3` varchar(2048) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `key4` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `value4` varchar(2048) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `key5` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `value5` varchar(2048) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `key6` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `value6` varchar(2048) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `key7` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `value7` varchar(2048) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `key8` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `value8` varchar(2048) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `key9` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `value9` varchar(2048) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ----------------------------
-- Table structure for game
-- ----------------------------
DROP TABLE IF EXISTS `game`;
CREATE TABLE `game` (
  `appName` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT 'app名字英文简写',
  `appID` int(11) NOT NULL COMMENT 'appid',
  `appKey` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT 'appkey',
  `appDesc` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT 'app中文名字',
  `orientation` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '游戏是横屏还是竖屏(landscape|portrait),不配置默认是横屏',
  `cpuSupport` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '支持的cpu',
  `outputApkName` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '输出安装包命名',
  `minSdkVersion` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '最小支持的Android SDK版本',
  `targetSdkVersion` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '默认使用的Android SDK版本',
  `maxSdkVersion` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '最大支持的Android SDK版本',
  `versionCode` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '游戏包的版本号',
  `versionName` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '游戏包中的版本名称',
  `ulog.enable` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '是否进行日志打印',
  `ulog.level` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '日志级别(DEBUG|INFO|WARNING|ERROR)',
  `ulog.local` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '是否在logcat中打印',
  `ulog.remote` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '是否在网页中远程打印，这里设置为true，需要启动scripts/uconsole.py',
  `ulog.remote_interval` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '远程打印时间间隔，单位毫秒',
  `ulog.remote_url` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '远程打印地址，uconsole.py启动监听的地址',
  PRIMARY KEY (`appName`,`appDesc`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ----------------------------
-- Table structure for packTask
-- ----------------------------
DROP TABLE IF EXISTS `packTask`;
CREATE TABLE `packTask` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '任务ID',
  `game` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT '游戏名',
  `channel` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT '渠道名',
  `channelVersion` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '渠道版本',
  `gameVersion` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '游戏版本',
  `startTime` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '创建时间',
  `founder` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '创建人',
  `state` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '打包状况',
  `journal` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '日志',
  `link` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '下载链接',
  PRIMARY KEY (`id`,`game`,`channel`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
