#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author xiaohei
# Date 2015-06-18
#
# 如果某个游戏需要统一做一些特殊的工作，那么可以考虑将这些特殊的工作
# 放在这里执行。
# 
# 比如游戏中接入了一个推送插件，推送插件的某个activity的android:name属性
# 需要设置为游戏的包名+Activity名称。插件是接在母包中的
# 
# 而每个渠道SDK的包名又不一样，所以我们需要一个做这个工作的地方
# 
# 虽然每个渠道SDK都需要这个，但是将这个操作放到各个渠道SDK的特殊脚本中执行
# 还是有点不合适。所以，我们定义了这个post_script.py。
# 
# 每个渠道SDK在打包的时候，资源合并完成，渠道SDK自己的特殊化脚本执行完毕之后
# 我们执行post_script.py。来处理该游戏的特殊需求
# 
# 该脚本放在 游戏配置目录下/scripts/post_script.py；比如game1/scripts/post_script.py
#
import file_utils
import apk_utils
import os
import os.path
import config_utils
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import SubElement
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import ElementTree
import os
import os.path
import zipfile
import re
import subprocess
import platform
from xml.dom import minidom
import codecs
import sys

androidNS = 'http://schemas.android.com/apk/res/android'

def execute(game, channel, decompileDir, packageName):

    configFile = file_utils.getFullPath('games/'+game['appName']+'/game_config.properties')

    if not os.path.exists(configFile):
        print("game_config file not exists."+configFile)
        return 1

    manifest = decompileDir + '/AndroidManifest.xml'
    ET.register_namespace('android', androidNS)
    key = '{' + androidNS + '}name'
    keyVal = '{'+androidNS+'}value'
    tree = ET.parse(manifest)
    root = tree.getroot()

    appNode = root.find('application')
    if appNode is None:
        return 1

    f = open(configFile, 'r')
    for line in f.readlines():
        item = line.strip().split('=',1)
        metaDataNode = SubElement(appNode, 'meta-data')
        metaDataNode.set(key, item[0])
        metaDataNode.set(keyVal, item[1])

    f.close()


    tree.write(manifest, 'UTF-8')

    return 0



