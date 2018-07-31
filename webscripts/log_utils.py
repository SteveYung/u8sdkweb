#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author xiaohei
# Date 2015-06-18

import logging
import os
import platform
import sys

curDir = os.getcwd()

def getFullPath(filename):
    if os.path.isabs(filename):
        return filename #如果是绝对路径就直接输出
    try:
        curDir = str(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))+'/'+str(filename)
    except ImportError:
        curDir = str(os.path.abspath(os.path.join(os.getcwd(), "..")))+'/'+str(filename)
    return curDir

def getCurrDir():
    global curDir
    retPath = curDir
    if platform.system() == 'Darwin':
        retPath = sys.path[0]
        lstPath = os.path.split(retPath)
        if lstPath[1]:
            retPath = lstPath[0]

    return retPath

logger = logging.getLogger("")
logger.setLevel(logging.DEBUG)

log_file = getFullPath("log/u8sdk.log")

log_dir = os.path.dirname(log_file)
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

file_handler = logging.FileHandler(log_file, "w", "UTF-8")
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s: %(message)s')
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)


def info(msg, *args):
    if len(msg) <= 0:
        return
    logger.info(msg, *args)
    logger.info('\n')

def debug(msg, *args):
    if len(msg) <= 0:
        return
    logger.debug(msg, *args)
    logger.debug('\n')

def warning(msg, *args):
    if len(msg) <= 0:
        return
    logger.warning(msg, *args)
    logger.warning('\n')

def error(msg, *args):
    if len(msg) <= 0:
        return
    logger.error(msg, *args)
    logger.error('\n')
