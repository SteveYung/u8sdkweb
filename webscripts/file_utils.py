# -*- coding: utf-8 -*-
# Author:xiaohei
# CreateTime:2014-10-25
#
# All file operations are defined here
import os
import os.path
import re
import platform
import subprocess
import inspect
import sys
import codecs
import threading
import time
import log_utils

curDir = os.getcwd()



def list_files(src, resFiles, igoreFiles):

    if os.path.exists(src):

        if os.path.isfile(src) and src not in igoreFiles:
            resFiles.append(src)
        elif os.path.isdir(src):
            for f in os.listdir(src):
                if src not in igoreFiles:
                    list_files(os.path.join(src, f), resFiles, igoreFiles)

    return resFiles


def del_file_folder(src):
    if os.path.exists(src):
        if os.path.isfile(src):
            try:
                src = src.replace('\\', '/')
                os.remove(src) #删除文件夹
            except:
                pass

        elif os.path.isdir(src):
            for item in os.listdir(src): #列出目录列表
                itemsrc = os.path.join(src, item)
                del_file_folder(itemsrc)

            try:
                os.rmdir(src)
            except:
                pass


def copy_files(src, dest):
    if not os.path.exists(src):
        log_utils.warning("the src is not exists.path:%s", src)
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


def modifyFileContent(sourcefile, oldContent, newContent):
    
    if os.path.isdir(sourcefile):
        log_utils.warning("the source %s must be a file not a dir", sourcefile)
        return

    if not os.path.exists(sourcefile):
        log_utils.warning("the source is not exists.path:%s", sourcefile)
        return

    f = open(sourcefile, 'r+')
    data = str(f.read())
    f.close()
    bRet = False
    idx = data.find(oldContent)
    while idx != -1:
        data = data[:idx] + newContent + data[idx + len(oldContent):]
        idx = data.find(oldContent, idx + len(oldContent))
        bRet = True

    if bRet:
        fw = open(sourcefile, 'w')
        fw.write(data)
        fw.close()
        log_utils.info("modify file success.path:%s", sourcefile)
    else:
        log_utils.warning("there is no content matched in file:%s with content:%s", sourcefile, oldContent)


def getCurrDir():
    global curDir
    retPath = curDir
    if platform.system() == 'Darwin':
        retPath = sys.path[0]
        lstPath = os.path.split(retPath)
        if lstPath[1]:
            retPath = lstPath[0]

    return retPath


def getFullPath(filename):
    #组合绝对路径
    if os.path.isabs(filename):
        return filename #如果是绝对路径就直接输出
    try:
        curDir = str(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))+'/'+str(filename)
    except ImportError:
        curDir = str(os.path.abspath(os.path.join(os.getcwd(), "..")))+'/'+str(filename)
    return curDir


def getSplashPath():
    return getFullPath("config/splash")

def getJavaBinDir():
    if platform.system() == 'Windows':
        return getFullPath("tool/win/jre/bin/")
    else:
        return ""

def getJavaCMD():
    return getJavaBinDir() + "java"

def getToolPath(filename):
    if platform.system() == 'Windows':
        return "tool/win/" + filename
    elif platform.system() == 'Linux':
        return "tool/liunx/" + filename
    else:
        return "tool/mac/" + filename


def getFullToolPath(filename):
    return getFullPath(getToolPath(filename))

def getFullOutputPath(appName, channel):
    path = getFullPath('output/' + appName + '/' + channel)
    #del_file_folder(path)
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def execFormatCmd(cmd):
    cmd = cmd.replace('\\', '/')
    cmd = re.sub('/+', '/', cmd)
    ret = 0

    try:
        (status, output) = subprocess.getstatusoutput(cmd)
        log_utils.error("\n*******CMD*******\n")
        log_utils.error(cmd)
        log_utils.error('\n')
        log_utils.error(output)
        log_utils.error("\n*******************\n")
    except Exception as e:
        log_utils.error(e)
        return

    return status


def execWinCommand(cmd):
    os.system(cmd)  


def execWinCommandInput(tip):
    r = os.popen("set /p s=" + tip)
    txt = r.read()
    r.close()
    return txt

def on_access_error(func, path, exc_info):
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise


def printLogo():

    u = [
        "$$    $$",
        "$$    $$",
        "$$    $$",
        "$$    $$",
        " $$$$$$ "
    ]

    n8=[
        " $$$$$$ ",
        "$$    $$",
        " $$$$$$ ",
        "$$    $$",
        " $$$$$$ "
    ]

    s=[
        " $$$$$$ ",
        " $$     ",
        " $$$$$$ ",
        "     $$ ",
        " $$$$$$ "
    ]

    d=[
        "$$$$$$  ",
        "$     $$",
        "$     $$",
        "$     $$",
        "$$$$$$  "
    ]

    k=[
        "$$    $$",
        "$$  $$  ",
        "$$$$    ",
        "$$  $$  ",
        "$$    $$"
    ]

    print("################################################################")
    print(" ")
    for i in range(0, len(u)):
        line = "    " + u[i] + "    " + n8[i] + "    " + s[i] + "    " + d[i] + "    " + k[i]
        print(line)

    print(" ")
    print("################################################################")

