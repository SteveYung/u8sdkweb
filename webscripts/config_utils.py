#encoding:utf-8
#Author:xiaohei
#CreateTime:2014-10-25
#
# The config operations
#
#
import sys
import os
import os.path
import file_utils
import log_utils
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import SubElement
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import ElementTree


def getLocalConfig():
    configFile = file_utils.getFullPath("config/local/local.properties")
    if not os.path.exists(configFile):
        log_utils.error("local.properties is not exists. %s " % configFile)
        return None

    cf = open(configFile, "r")
    lines = cf.readlines()
    cf.close()

    config = {}

    for line in lines:
        line = line.strip()
        if len(line) == 0:
            continue
        dup = line.split('=')
        config[dup[0]] = dup[1]

    return config


def getToolVersion():
    config = getLocalConfig()
    if config and "tool_versionName" in config:
        return config['tool_versionName']

    return "unkown"


def getJDKHeapSize():
    config = getLocalConfig()
    if config and "jdk_heap_size" in config:
        return config['jdk_heap_size']

    return 512

def get_py_version():
    version = sys.version_info
    major = version.major
    minor = version.minor
    micro = version.micro

    currVersion = str(major)+"."+str(minor)+"."+str(micro)

    return currVersion

def is_py_env_2():

    version = sys.version_info
    major = version.major
    return major == 2

def getAllGames():
    """
        get all games
    """
    configFile = file_utils.getFullPath("games/games.xml")
    try:
        tree = ET.parse(configFile)
        root = tree.getroot()
    except Exception as e:
        log_utils.error("can not parse games.xml.path:%s", configFile)
        return None

    gamesNode = root.find('games')
    if gamesNode == None:
        return None

    games = gamesNode.findall('game')

    if games == None or len(games) <= 0:
        return None

    lstGames = []
    for cNode in games:
        game = {}
        params = cNode.findall('param')
        if params != None and len(params) > 0:
            for cParam in params:
                key = cParam.get("name")
                val = cParam.get("value")
                game[key] = val

        logNode = cNode.find('log')
        if logNode != None:
            game['log'] = dict()
            logParams = logNode.findall('param')
            if logParams != None and len(logParams) > 0:
                for lParam in logParams:
                    key = lParam.get("name")
                    val = lParam.get('value')
                    game['log'][key] = val

        lstGames.append(game)
    # print(lstGames)
    return lstGames


def getTestKeyStore():
    keystore = {}
    keystore['keystore'] = "config/keystore/xiaohei.keystore"
    keystore['password'] = "xiaohei"
    keystore['aliaskey'] = "xiaohei"
    keystore['aliaspwd'] = "xiaohei"

    return keystore


def getKeystore(appName, channelId):
    lstKeystores = getAllKeystores(appName)
    if lstKeystores != None and len(lstKeystores) > 0:
        for keystore in lstKeystores:
            if keystore['channelId'] == channelId:
                return keystore

    return getDefaultKeystore(appName)


def getDefaultKeystore(appName):
    fileName = "games/" + appName + "/keystore.xml"
    configFile = file_utils.getFullPath(fileName)
    try:
        tree = ET.parse(configFile)
        root = tree.getroot()
    except Exception as e:
        log_utils.error("can not parse keystore.xml.path:%s", configFile)
        return None

    params = root.find("default").findall("param")
    channel = {}
    for cParam in params:
        key = cParam.get('name')
        val = cParam.get('value')
        channel[key] = val

    return channel

def getAllKeystores(appName):

    fileName = "games/" + appName + "/keystore.xml"

    configFile = file_utils.getFullPath(fileName)

    try:
        tree = ET.parse(configFile)
        root = tree.getroot()
    except Exception as e:
        log_utils.error("can not parse keystore.xml.path:%s", configFile)
        return None

    channels = root.find("keystores").findall("channel")
    lstKeystores = []

    for cNode in channels:
        channel = {}
        params = cNode.findall("param")
        for cParam in params:
            key = cParam.get('name')
            val = cParam.get('value')
            channel[key] = val

        lstKeystores.append(channel)

    return lstKeystores


def getAppID():
    configFile = file_utils.getFullPath("config/config.xml")

    try:
        tree = ET.parse(configFile)
        root = tree.getroot()
    except Exception as e:
        log_utils.error("can not parse config.xml.path:%s", configFile)
        return None

    gameNode = root.find("game")

    if gameNode == None:
        return None


    appID = gameNode.get('appID')

    return appID

def getAppKey():
    configFile = file_utils.getFullPath("config/config.xml")

    try:
        tree = ET.parse(configFile)
        root = tree.getroot()
    except Exception as e:
        log_utils.error("can not parse config.xml.path:%s", configFile)
        return None

    gameNode = root.find("game")

    if gameNode == None:
        return None


    appID = gameNode.get('appKey')

    return appID


def getAllChannels(appName, isPublic):

    fileName = "games/" + appName + "/config.xml"

    configFile = file_utils.getFullPath(fileName)

    if not os.path.exists(configFile):
        log_utils.error("%s is not exists", configFile)
        return

    try:
        tree = ET.parse(configFile)
        root = tree.getroot()
    except Exception as e:
        log_utils.error("can not parse config.xml.path:%s",configFile)
        return None

    lstGPlugins = []
    globalPluginsNode = root.find("global-plugins")
    if globalPluginsNode is not None:
        globalPlugins = globalPluginsNode.findall("plugin")
        if globalPlugins is not None and len(globalPlugins) > 0:
            for pluginNode in globalPlugins:
                plugin = {}
                plugin['name'] = pluginNode.get("name")
                plugin['desc'] = pluginNode.get("desc")
                lstGPlugins.append(plugin)

    channels = root.find("channels").findall("channel")
    lstChannels = []
    for cNode in channels:
        channel = {}
        params = cNode.findall("param")
        for cParam in params:
            key = cParam.get('name')
            val = cParam.get('value')
            channel[key] = val

        sdkVersionNode = cNode.find('sdk-version')
        if sdkVersionNode != None and len(sdkVersionNode) > 0:
            versionCodeNode = sdkVersionNode.find('versionCode')
            versionNameNode = sdkVersionNode.find('versionName')
            if versionCodeNode != None and versionNameNode != None:
                # u8server use the logic version code to decide which sdk version to use
                channel['sdkLogicVersionCode'] = versionCodeNode.text
                channel['sdkLogicVersionName'] = versionNameNode.text


        sdkParams = cNode.find("sdk-params")
        tblSDKParams = {}

        if sdkParams != None:
            sdkParamNodes = sdkParams.findall('param')
            if sdkParamNodes != None and len(sdkParamNodes) > 0:
                for cParam in sdkParamNodes:
                    key = cParam.get('name')
                    val = cParam.get('value')
                    tblSDKParams[key] = val

        channel['sdkParams'] = tblSDKParams

        localGPlugins = list()
        if len(lstGPlugins) > 0:
            for p in lstGPlugins:
                localP = {}
                localP['name'] = p['name']
                localP['desc'] = p['desc']
                loadThirdPluginUserConfig(appName, channel, localP, localP['name'])
                localGPlugins.append(localP)

        ret = loadChannelUserConfig(appName, channel)
        if ret:
            lstPlugins = [] + localGPlugins
            pluginsNode = cNode.find("plugins")

            if pluginsNode != None:
                pluginNodeLst = pluginsNode.findall("plugin")
                if pluginNodeLst != None and len(pluginNodeLst) > 0:

                    for cPlugin in pluginNodeLst:
                        plugin = {}
                        plugin['name'] = cPlugin.get('name')

                        exists = False
                        for p in lstPlugins:
                            if p['name'] == plugin['name']:
                                exists = True
                                break

                        if not exists:
                            plugin['desc'] = cPlugin.get('desc')
                            loadThirdPluginUserConfig(appName, channel, plugin, plugin['name'])
                            lstPlugins.append(plugin)

            channel['third-plugins'] = lstPlugins
            lstChannels.append(channel)          

    return lstChannels

def loadThirdPluginUserConfig(appName, channel, plugin, pluginName):
    #configFile = file_utils.getFullPath("config/plugin/" + pluginName + "/config.xml")
    configFile = file_utils.getFullPath("games/" + appName + "/channels/" + channel['id'] + "/plugin/" + pluginName + "/config.xml")
    
    if not os.path.exists(configFile):
        configFile = file_utils.getFullPath("games/"+appName+"/plugin/"+pluginName+"/config.xml")
        if not os.path.exists(configFile):
            log_utils.error("the plugin %s config.xml file is not exists.path:%s", pluginName, configFile)
            return 0

    try:
        tree = ET.parse(configFile)
        root = tree.getroot()
    except:
        log_utils.error("can not parse config.xml.path:%s", configFile)
        return 0

    configNode = root

    subpluginNodes = configNode.find("subplugins")

    if subpluginNodes != None and len(subpluginNodes) > 0:
        plugin['subplugins'] = []
        for subNode in subpluginNodes:
            subplugin = {}
            subplugin['name'] = subNode.get('name')
            subplugin['desc'] = subNode.get('desc')
            subParamNodes = subNode.findall('param')
            subplugin['params'] = []
            if subParamNodes != None and len(subParamNodes) > 0:
                for subParamNode in subParamNodes:
                    param = {}
                    param['name'] = subParamNode.get('name')
                    param['value'] = subParamNode.get('value')
                    #log_utils.debug("name:"+param['name']+";val:"+param['value'])
                    param['required'] = subParamNode.get('required')
                    param['showName'] = subParamNode.get('showName')
                    param['bWriteInManifest'] = subParamNode.get('bWriteInManifest')
                    param['bWriteInClient'] = subParamNode.get('bWriteInClient')
                    subplugin['params'].append(param)

            plugin['subplugins'].append(subplugin)


    paramNodes = configNode.find("params")
    plugin['params'] = []
    if paramNodes != None and len(paramNodes) > 0:

        for paramNode in paramNodes:
            param = {}
            param['name'] = paramNode.get('name')
            param['value'] = paramNode.get('value')
            param['required'] = paramNode.get('required')
            param['showName'] = paramNode.get('showName')
            param['bWriteInManifest'] = paramNode.get('bWriteInManifest')
            param['bWriteInClient'] = paramNode.get('bWriteInClient')
            plugin['params'].append(param)

    operationNodes = configNode.find("operations")
    plugin['operations'] = []
    if operationNodes != None and len(operationNodes) > 0:

        for opNode in operationNodes:
            op = {}
            op['type'] = opNode.get('type')
            op['from'] = opNode.get('from')
            op['to'] = opNode.get('to')
            plugin['operations'].append(op)

    pluginNodes = configNode.find("plugins")
    if pluginNodes != None and len(pluginNodes) > 0:
        plugin['plugins'] = []
        for pNode in pluginNodes:
            p = {}
            p['name'] = pNode.get('name')
            p['type'] = pNode.get('type')
            plugin['plugins'].append(p)

    return 1

def loadChannelUserConfig(appName, channel):
    configFile = file_utils.getFullPath("config/sdk/" + channel['sdk'] + "/config.xml")

    if not os.path.exists(configFile):
        log_utils.error("the config.xml is not exists of sdk %s.path:%s", channel['name'], configFile)
        return 0

    try:
        tree = ET.parse(configFile)
        root = tree.getroot()
    except:
        log_utils.error("can not parse config.xml.path:%s", configFile)
        return 0

    configNode = root

    paramNodes = configNode.find("params")
    channel['params'] = []
    if paramNodes != None and len(paramNodes) > 0:

        for paramNode in paramNodes:
            param = {}
            param['name'] = paramNode.get('name')
            param['required'] = paramNode.get('required')

            if param['required'] == '1':

                key = param['name']
                if key in channel['sdkParams'] and channel['sdkParams'][key] != None:
                    param['value'] = channel['sdkParams'][key]
                else:
                    log_utils.error("the sdk %s 'sdkParam's is not all configed in the config.xml.path:%s", channel['name'], configFile)
                    return 0
            else:
                param['value'] = paramNode.get('value')

            param['showName'] = paramNode.get('showName')
            param['bWriteInManifest'] = paramNode.get('bWriteInManifest')
            param['bWriteInClient'] = paramNode.get('bWriteInClient')
            channel['params'].append(param)

    #支持sdk-params里面配置额外的参数，默认写到assets下面u8_developer_config.properties中
    #begin
    if channel['sdkParams'] is not None:

        for key in channel['sdkParams']:
            extraKey = True
            if channel['params'] is not None and len(channel['params']) > 0:
                for p in channel['params']:
                    if p['name'] == key:
                        extraKey = False
                        break

            if extraKey:
                param = {}
                param['name'] = key
                param['value'] = channel['sdkParams'][key]
                param['required'] = "1"
                param['showName'] = key
                param['bWriteInManifest'] = "0"
                param['bWriteInClient'] = "1"
                channel['params'].append(param)
    #end
    #支持sdk-params里面配置额外的参数，默认写到assets下面u8_developer_config.properties中                


    operationNodes = configNode.find("operations")
    channel['operations'] = []
    if operationNodes != None and len(operationNodes) > 0:

        for opNode in operationNodes:
            op = {}
            op['type'] = opNode.get('type')
            op['from'] = opNode.get('from')
            op['to'] = opNode.get('to')
            channel['operations'].append(op)

    pluginNodes = configNode.find("plugins")
    if pluginNodes != None and len(pluginNodes) > 0:
        channel['plugins'] = []
        for pNode in pluginNodes:
            p = {}
            p['name'] = pNode.get('name')
            p['type'] = pNode.get('type')
            channel['plugins'].append(p)


    versionNode = configNode.find("version")
    if versionNode != None and len(versionNode) > 0:
        versionCodeNode = versionNode.find("versionCode")
        versionNameNode = versionNode.find("versionName")
        # the sdk version code is used to check version update for the sdk.
        if versionCodeNode != None and versionNameNode != None:
            channel['sdkVersionCode'] = versionCodeNode.text
            channel['sdkVersionName'] = versionNameNode.text

    return 1

def writeDeveloperProperties(game, channel, targetFilePath):

    targetFilePath = file_utils.getFullPath(targetFilePath)

    if os.path.exists(targetFilePath):
        file_utils.del_file_folder(targetFilePath)

    proStr = ""
    if channel['params'] != None and len(channel['params']) > 0:
        for param in channel['params']:
            if param['bWriteInClient'] == '1':
                proStr = proStr + param['name'] + "=" + param['value'] + "\n"

    if "sdkLogicVersionCode" in channel:
        proStr = proStr + "U8_SDK_VERSION_CODE=" + channel["sdkLogicVersionCode"] + "\n"

    proStr = proStr + "U8_Channel=" + channel['id'] + "\n"
    proStr = proStr + "U8_APPID=" + game["appID"] + "\n"
    proStr = proStr + "U8_APPKEY=" + game["appKey"] + "\n"

    if "payPrivateKey" in game:
        proStr = proStr + "U8_PAY_PRIVATEKEY=" + game["payPrivateKey"] + "\n"

    showSplash = "false"
    if "splash" in channel and int(channel["splash"]) > 0 :
        showSplash = "true"

    proStr = proStr + "U8_SDK_SHOW_SPLASH=" + showSplash + "\n"

    authUrl = None
    orderUrl = None
    analyticsUrl = None
    u8serverUrl = None
    u8analytics = None

    if "u8_auth_url" in game:
        authUrl = game["u8_auth_url"]

    if "u8_order_url" in game:
        orderUrl = game["u8_order_url"]

    if "u8_analytics_url" in game:
        analyticsUrl = game["u8_analytics_url"]

    if "u8server_url" in game:
        u8serverUrl = game["u8server_url"]

    if "u8_analytics" in game:
        u8analytics = game["u8_analytics"]

    #append u8 local config
    local_config = getLocalConfig()

    if authUrl is None and "u8_auth_url" in local_config:
        authUrl = local_config['u8_auth_url']

    if orderUrl is None and "u8_order_url" in local_config:
        orderUrl = local_config['u8_order_url']

    if u8serverUrl is None and "u8server_url" in local_config:
        u8serverUrl = local_config['u8server_url']

    if u8analytics is None and "u8_analytics" in local_config:
        u8analytics = local_config['u8_analytics']

    if analyticsUrl is None and "u8_analytics_url" in local_config:
        analyticsUrl = local_config['u8_analytics_url']

    if authUrl is not None:
        proStr = proStr + "U8_AUTH_URL=" + authUrl + "\n"

    if orderUrl is not None:
        proStr = proStr + "U8_ORDER_URL=" + orderUrl + "\n"

    if analyticsUrl is not None:
        proStr = proStr + "U8_ANALYTICS_URL=" + analyticsUrl + "\n"

    if u8serverUrl is not None:
        proStr = proStr + "U8SERVER_URL=" + u8serverUrl + "\n"

    if u8analytics is not None:
        proStr = proStr + "U8_ANALYTICS=" + u8analytics + "\n"


    #write third plugin info:
    plugins = channel.get('third-plugins')
    if plugins != None and len(plugins) > 0:

        for plugin in plugins:
            if 'params' in plugin and plugin['params'] != None and len(plugin['params']) > 0:
                for param in plugin['params']:
                    if param['bWriteInClient'] == '1':
                        proStr = proStr + param['name'] + "=" + param['value'] + "\n"

    log_utils.debug("the develop info is %s", proStr)
    targetFile = open(targetFilePath, 'wb')
    proStr = proStr.encode('UTF-8')
    targetFile.write(proStr)
    targetFile.close()


def writePluginConfigs(channel, targetFilePath):
    targetTree = None
    targetRoot = None
    pluginNodes = None

    targetTree = ElementTree()
    targetRoot = Element('plugins')
    targetTree._setroot(targetRoot)

    if 'plugins' in channel:
        for plugin in channel['plugins']:
            typeTag = 'plugin'
            typeName = plugin['name']
            typeVal = plugin['type']
            pluginNode = SubElement(targetRoot, typeTag)
            pluginNode.set('name', typeName)
            pluginNode.set('type', typeVal)

    # write third plugin info

    thirdPlugins = channel.get('third-plugins')
    if thirdPlugins != None and len(thirdPlugins) > 0:
        for cPlugin in thirdPlugins:

            if 'plugins' in cPlugin and cPlugin['plugins'] != None and len(cPlugin['plugins']) > 0:
                for plugin in cPlugin['plugins']:
                    typeTag = 'plugin'
                    typeName = plugin['name']
                    typeVal = plugin['type']
                    pluginNode = SubElement(targetRoot, typeTag)
                    pluginNode.set('name', typeName)
                    pluginNode.set('type', typeVal)


    targetTree.write(targetFilePath, 'UTF-8')
