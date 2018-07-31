#encoding:utf-8

import os
import os.path
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
import shutil
import sys

curDir = os.getcwd()

def is_ignored(fpath, ignores):

    for ig in ignores:
        if ig in fpath:

            return True

    return False  


def getCurrDir():
    global curDir
    retPath = curDir
    if platform.system() == "Windows":
        retPath = retPath.decode('gbk')
    return retPath


def getFullPath(filename):
    if os.path.isabs(filename):
        return filename
    currdir = getCurrDir()
    filename = os.path.join(currdir, filename)
    filename = filename.replace('\\', '/')
    filename = re.sub('/+', '/', filename)
    return filename


def copy_files(src, dest):
    if not os.path.exists(src):
        log_utils.warning("copy files . the src is not exists.path:%s", src)
        return

    if os.path.isfile(src):
        copy_file(src, dest)
        return

    for f in os.listdir(src):
        sourcefile = os.path.join(src, f)
        targetfile = os.path.join(dest, f)
        if os.path.isfile(sourcefile):
            copy_file(sourcefile, targetfile)
        else:
            copy_files(sourcefile, targetfile)


def copy_file(src, dest):
    sourcefile = getFullPath(src)
    destfile = getFullPath(dest)
    if not os.path.exists(sourcefile):
        return
    if not os.path.exists(destfile) or os.path.getsize(destfile) != os.path.getsize(sourcefile):
        destdir = os.path.dirname(destfile)
        if not os.path.exists(destdir):
            os.makedirs(destdir)
        destfilestream = open(destfile, 'wb')
        sourcefilestream = open(sourcefile, 'rb')
        destfilestream.write(sourcefilestream.read())
        destfilestream.close()
        sourcefilestream.close()    


if __name__ == "__main__":

    ignores = [".svn", "META-INF", "findnoneclass.py"]

    path = "."
    targetPath = "../../root"

    if not os.path.exists(targetPath):
        os.makedirs(targetPath)

    for root, dirs, files in os.walk(path):

        for f in files:

            if f.endswith(".class"):
                continue

            fpath = os.path.join(root, f)

            if not is_ignored(fpath, ignores):

                if not os.path.exists(root):
                    os.makedirs(root)

                print(fpath)
                ftargetpath = fpath[1:]
                print(ftargetpath)
                ftargetpath = targetPath + ftargetpath
                print(ftargetpath)
                copy_files(fpath, ftargetpath)

