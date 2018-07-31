# -*- coding: utf-8 -*-
#Author:xiaohei
#CreateTime:2014-10-25
#
# The main operation entry for channel select and one thread.
#

import sys
import core
import file_utils
import apk_utils
import config_utils
import log_utils
import os
import os.path
import time
import main
import main_thread


def entry(isPublic, isSelectable, threadNum, appID, channelName):


    #file_utils.printLogo()

    log_utils.info("Curr Python Version::%s", config_utils.get_py_version())
    log_utils.info("Curr U8SDK Version::%s", config_utils.getToolVersion())

    games = config_utils.getAllGames()

    selectedGameID = appID

    if selectedGameID is None:

        print(u"################################################################")
        print(u"\t%-20s%-20s%-20s\n" % ("AppID", u"AppName", u"描述"))

        
        if games != None and len(games) > 0:
            for ch in games:
                print(u"\t%-20s%-20s%-20s" % (ch['appID'], ch['appName'], ch['appDesc']))
                #print(u"\t %s \t\t %s \t\t\t%s" % (ch['appID'], ch['appName'], ch['appDesc']))

        print("")
        
        sys.stdout.write(u"请选择一个游戏(输入appID)：")
        sys.stdout.flush()

        selectedGameID = input()
        selectedGameID = str(selectedGameID)

    game = getGameByAppID(selectedGameID, games)

    log_utils.info("current selected game is %s(%s)", game['appName'], game['appDesc'])

    if isSelectable:
        main.main(game, isPublic, channelName)
    else:
        main_thread.main(game, isPublic, threadNum)



def getGameByAppID(appID, games):

    if games == None or len(games) <= 0:
        return None

    for game in games:
        if game['appID'] == appID:
            return game

    return None


