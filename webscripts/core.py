# -*- coding: utf-8 -*-
#Author:xiaohei
#CreateTime:2014-10-25
#
# The main operation entry
#
# 1、decomplie apk to smali use apktool.jar
# 2、rename the apk package name to new name configed in channel
# 3、copy all sdk resources of the channel to the target decompile dir
#    3.1、copy all none xml files to the target dir
#	 3.2、merge the sdk AndroidManifest.xml to the target apk AndroidManifest.xml
#	 3.3、merge all the sdk res xml like strings.xml, drawables.xml,styles.xml...
# 4、copy all code and resources of supported third-plugins
# 5、generate plugin info and develop info in assets folder,and write meta-data to AndroidManifest.xml
# 6、regenerate the R file
# 7、recompile the apk file
# 8、sign the apk file
# 9、zip allign the apk file

import sys
import file_utils
import apk_utils
import config_utils
import log_utils
import os
import os.path
import time


def pack(game, channel, sourcepath, isPublic):

    sourcepath = sourcepath.replace('\\', '/')
    if not os.path.exists(sourcepath):
        return 1

    appID = game['appID']
    appKey = game['appKey']
    appName = game['appName']

    channelId = channel["id"]
    channelName = channel["name"]
    sdkName = channel["sdk"]

    log_utils.info("now to package %s...", channelName)

    workDir = 'workspace/' + appName + '/' + channelName
    workDir = file_utils.getFullPath(workDir)

    file_utils.del_file_folder(workDir)
    tempApkSource = workDir + "/temp.apk"
    file_utils.copy_file(sourcepath, tempApkSource)
    decompileDir = workDir + "/decompile"
    ret = apk_utils.decompileApk(tempApkSource, decompileDir)

    if ret:
        return 2


    #检查母包接入是否正确
    # ret = apk_utils.checkApkForU8SDK(workDir, decompileDir)
    # if ret:
    #     return 1

    #检查multidex那个jar包
    apk_utils.checkMultiDexJar(workDir, decompileDir)

    #更改XML配置等
    newPackageName = apk_utils.renamePackageName(channel, decompileDir, channel['suffix'], isPublic)

    #复制第三插件资源。注意：这第三个插件必须在主SDK之前运行。
    ret = apk_utils.handleThirdPlugins(workDir, decompileDir, game, channel, newPackageName)

    if ret:
        return 3

    #将SDK代码复制到反编译程序
    sdkSourceDir = file_utils.getFullPath('config/sdk/' + sdkName)
    smaliDir = decompileDir + "/smali"
    sdkDestDir = workDir + "/sdk/" + sdkName
    file_utils.copy_files(sdkSourceDir, sdkDestDir)

    if (not os.path.exists(sdkSourceDir + "/classes.dex")):
        ret = apk_utils.jar2dex(sdkSourceDir, sdkDestDir)
        if ret:
            return 4


    ret = apk_utils.dexes2smali(sdkDestDir, smaliDir, "baksmali.jar")
    if ret:
        return 5

    #复制主SDK资源。
    ret = apk_utils.copyResource(game, channel, newPackageName, sdkDestDir, decompileDir, channel['operations'], channelName)
    if ret:
        return 6

    #自动处理图标
    apk_utils.appendChannelIconMark(game, channel, decompileDir)

    #复制渠道专用资源
    ret = apk_utils.copyChannelResources(game, channel, decompileDir)
    if ret:
        return 7

    #复制游戏根资源和资源
    apk_utils.copyAppResources(game, decompileDir)
    apk_utils.copyAppRootResources(game, decompileDir)
    
    #生成APK运行的配置文件。
    apk_utils.writeDevelopInfo(game, channel, decompileDir)
    apk_utils.writePluginInfo(channel, decompileDir)
    apk_utils.writeManifestMetaInfo(channel, decompileDir)
    apk_utils.writeLogConfig(game, decompileDir)

    #如果主SDK具有特殊逻辑。执行特殊的逻辑脚本。
    ret = apk_utils.doSDKScript(channel, decompileDir, newPackageName, sdkDestDir)
    if ret:
        return 8

    #如果游戏有一些特殊的逻辑。执行特殊的逻辑脚本。 post_script.py
    ret = apk_utils.doGamePostScript(game, channel, decompileDir, newPackageName)
    if ret:
        return 9

    #here to config the splash screen.
    ret = apk_utils.addSplashScreen(workDir, channel, decompileDir)
    if ret:
        return 10

    #检查CPU支持
    apk_utils.checkCpuSupport(game, decompileDir)

    #如果指定频道，修改游戏名称。
    apk_utils.modifyGameName(channel, decompileDir)

    #修改YML
    apk_utils.modifyYml(game, newPackageName, decompileDir)
    #到达复制sdk到临时目录

    #生成新的R.java
    print('生成新的R.java')
    print(newPackageName)
    print(decompileDir)
    print(channel)
    print('===================================')
    ret = apk_utils.generateNewRFile(newPackageName, decompileDir, channel)
    if ret:
        return 11

    #检查分离DEX
    apk_utils.splitDex(workDir, decompileDir)


    targetApk = workDir + "/output.apk"
    log_utils.debug("现在重新编译APK....")
    ret = apk_utils.recompileApk(decompileDir, targetApk)
    if ret:
        return 12

    apk_utils.copyRootResFiles(targetApk, decompileDir)#复制根目录

    ###

    #destApkName = channelName + '.apk'
    channelNameStr = channelName.replace(' ', '')

    if isPublic:  # 获取最终apk包名
        #destApkName = channelNameStr + '-' + time.strftime('%Y%m%d%H') + '.apk'
        destApkName = apk_utils.getOutputApkName(game, channel, newPackageName, decompileDir)
    else:
        destApkName = channelNameStr + '-' + time.strftime('%Y%m%d%H') + '-debug.apk'

    destApkPath = file_utils.getFullOutputPath(appName, channelName)
    destApkPath = os.path.join(destApkPath, destApkName)
    ret = apk_utils.alignApk(targetApk, destApkPath)

    if ret:
        return 13

    if 'signApk' not in channel or channel['signApk'] != '0':
        ret = apk_utils.signApk(workDir, game, channel, destApkPath)#对已经输出的安装包进行签名
        if ret:
            return 14
    else:
        log_utils.debug("APK设置为未签名。")

    #clear workspace
    #file_utils.del_file_folder(workDir)

    log_utils.info("游戏 %s 渠道 %s 打包成功.", appName,channelName)
    return 0


