# -*- coding: utf-8 -*-
#CreateTime:2014-10-25

import sys
import file_utils
import os
import os.path
import time
import zipfile


def entry():
    sourceApkFile = file_utils.getFullPath("u8source.apk")
    channelsFile = file_utils.getFullPath("channels.txt")

    if not os.path.exists(channelsFile):
        file_utils.printF("The channels.txt file is not exists.")
        return

    f = open(channelsFile)
    channelLines = f.readlines()
    f.close()

    channels = []
    if channelLines != None and len(channelLines) > 0:

        for line in channelLines:
            targetChannel = line.strip()
            channels.append(targetChannel)

    else:
        file_utils.printF("There is no channel configed in channels.txt")

    modify(channels, sourceApkFile)



def modify(channels, sourceApkFile):

    sourceApkFile = sourceApkFile.replace('\\', '/')
    if not os.path.exists(sourceApkFile):
        file_utils.printF("The source apk file is not exists")
        return

    tempFolder = file_utils.getFullPath('temp')
    if not os.path.exists(tempFolder):
        os.makedirs(tempFolder)


    empty_file = os.path.join(tempFolder, "temp.txt")
    f = open(empty_file, 'w')
    f.close()

    for channel in channels:
        generateNewChannelApk(sourceApkFile, empty_file, channel)

    file_utils.del_file_folder(tempFolder)


def generateNewChannelApk(sourceApkFile, empty_file, channelID):

    file_utils.printF("Now to generate channel %s", channelID)

    targetApk = file_utils.getFullPath("channels/u8-"+channelID+".apk")
    file_utils.copy_file(sourceApkFile, targetApk)

    zipped = zipfile.ZipFile(targetApk, 'a', zipfile.ZIP_DEFLATED)
    emptyChannelFile = "META-INF/u8channel_{channel}".format(channel=channelID)
    zipped.write(empty_file, emptyChannelFile)
    zipped.close()


entry()

