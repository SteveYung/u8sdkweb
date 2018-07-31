# -*- coding: utf-8 -*-
#Author:xiaohei
#CreateTime:2014-10-25
#
# The main operation entry for multi thread.
#

import sys
import core
import file_utils
import apk_utils
import config_utils
import os
import os.path
import time
import threading
import log_utils

if config_utils.is_py_env_2():
    import Queue as queue
else:
    import queue


def main(game, isPublic, threadNum = 1):

    packAllChannels(game, isPublic, threadNum)


def packAllChannels(game, isPublic, threadNum):

    basePath = file_utils.getCurrDir()
    log_utils.info("Curr Work Dir::%s", basePath)

    appName = game['appName']
    channels = config_utils.getAllChannels(appName, isPublic)

    if channels != None and len(channels) > 0:

        clen = len(channels)
        log_utils.info("Now Have %s channels to package ", clen)
        packagePath = file_utils.getFullPath('games/'+game['appName']+'/u8.apk')
        log_utils.info("The base apk file is : %s", packagePath)

        if not os.path.exists(packagePath):
            log_utils.error("The apk file name must be 'u8.apk'")
            return

        que = queue.Queue()
        for channel in channels:
            que.put(channel, True, None)

        # start threads to pack

        if threadNum <= 0:
            threadNum = 1

        log_utils.info("Now start %s threads to pack", threadNum)

        for i in range(threadNum):
            thread = PackerThread(que, packagePath, isPublic, game, i+1)
            thread.start()

        que.join()

        log_utils.info("<< all nice done >>")
    else:
        log_utils.info("<< no channels to pack >>")


# The thread to pack
class PackerThread(threading.Thread):
    def __init__(self, que, sourcepath, ispublic, game, index):
        threading.Thread.__init__(self)
        self.daemon = False
        self.queue = que
        self.sourcePath = sourcepath
        self.isPublic = ispublic
        self.game = game
        self.threadIndex = str(index)
        self.sucNum = 0
        self.failNum = 0

    def run(self):
        while True:
            if self.queue.empty():
                break
            channel = self.queue.get()

            ret = core.pack(self.game, channel, self.sourcePath, self.isPublic)

            if ret:
                self.failNum = self.failNum + 1
            else:
                self.sucNum = self.sucNum + 1

            self.queue.task_done()

        log_utils.info("Thread-%s:sucNum:%s;failNum:%s",self.threadIndex,str(self.sucNum), str(self.failNum))
        return
