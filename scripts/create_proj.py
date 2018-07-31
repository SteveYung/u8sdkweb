# -*- coding: utf-8 -*-
#Author:xiaohei
#CreateTime:2014-10-25
#
# All apk operations are defined here
#
#

import file_utils
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
import argparse
import shutil
import time
from PIL import Image
import image_utils
import log_utils
import smali_utils


def create_proj(projPath, targetName, classPrefix):

    if not os.path.exists(projPath):
        log_utils.debug("the U8SDK_Projects dir is not exists."+projPath)
        return

    templatePath = os.path.join(projPath, "U8SDK_Template")

    if not os.path.exists(templatePath):
        log_utils.debug("the template project is not exists."+templatePath)
        return

    if not targetName.startswith("U8SDK_"):
        targetName = "U8SDK_" + targetName

    targetPath = os.path.join(projPath, targetName)
    if os.path.exists(targetPath):
        log_utils.debug("the target project is already exists."+targetPath)
        return

    file_utils.copy_files(templatePath, targetPath)

    srcPath = os.path.join(targetPath, "src/com/u8/sdk")

    for f in os.listdir(srcPath):
        fname = os.path.join(srcPath, f)
        file_utils.modifyFileContent(fname, "Temp", classPrefix)

        ftarget = f.replace("Temp", classPrefix)
        os.rename(fname, os.path.join(srcPath, ftarget))

    configPath = os.path.join(targetPath, "config.xml")
    file_utils.modifyFileContent(configPath, "Temp", classPrefix) 

    projFilePath = os.path.join(targetPath, ".project")
    file_utils.modifyFileContent(projFilePath, "U8SDK_Template", targetName)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(u"U8SDK 渠道工程创建工具")
    parser.add_argument('-t', '--targetName', help=u"指定渠道名，英文或者拼音")
    parser.add_argument('-p', '--classPrefix', help=u"类名前缀")

    args = parser.parse_args()

    projPath = "../../U8SDK_Projects"

    log_utils.debug("create "+args.targetName+"...")

    create_proj(projPath, args.targetName, args.classPrefix)

    log_utils.debug("create "+args.targetName+" end")  
