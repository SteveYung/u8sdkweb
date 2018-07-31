#!/usr/bin/env python
# -*- coding: utf-8 -*-
import file_utils
import random
import core
import sql
import time

def write(sql_write):
    #数据写入
    if not sql.write(sql_write):
        time.sleep(3)
        if not sql.write(sql_write):
            time.sleep(3)
            if not sql.write(sql_write):
                print('######################################')
                print(sql_write)
                print('######################################')
                return False
    return True

def operations(channel_operations):
    #筛选组合operations数据
    operationss = []
    for i in range(1, 27, 3):
        operations_sub = {}
        a = channel_operations[i]
        b = channel_operations[i+1]
        c = channel_operations[i+2]
        if not a == None or not b == None or not c == None:
            operations_sub['type'] = str(a) if not a == None else ''
            operations_sub['from'] = str(b) if not b == None else ''
            operations_sub['to'] = str(c) if not c == None else ''
            operationss.append(operations_sub)
    return operationss

def plugins(channel_plugins):
    #筛选组合plugins数据
    pluginss = []
    for i in range(1, 18, 2):
        plugins_sub = {}
        a = channel_plugins[i]
        b = channel_plugins[i+1]
        if not a == None or not b == None:
            plugins_sub['name'] = str(a) if not a == None else ''
            plugins_sub['type'] = str(b) if not b == None else ''
            pluginss.append(plugins_sub)
    return pluginss

def params(channel_params):
    #筛选组合params数据
    paramss = []
    for i in range(1, 54, 6):
        params_sub = {}
        a = channel_params[i]
        b = channel_params[i+1]
        c = channel_params[i+2]
        d = channel_params[i+3]
        e = channel_params[i+4]
        f = channel_params[i+5]
        if not a == None or not b == None:
            params_sub['name'] = str(a) if not a == None else ''
            params_sub['value'] = str(b) if not b == None else ''
            params_sub['required'] = str(c) if not c == None else ''
            params_sub['showName'] = str(d) if not d == None else ''
            params_sub['bWriteInManifest'] = str(e) if not e == None else ''
            params_sub['bWriteInClient'] = str(f) if not f == None else ''
            paramss.append(params_sub)
    return paramss

def sdkParams(channel_sdkParams):
    #筛选组合sdkParams数据
    sdkParamss = {}
    for i in range(1, 18, 2):
        a = channel_sdkParams[i]
        b = channel_sdkParams[i+1]
        if not a == None or not b == None:
            sdkParamss[str(a) if not a == None else ''] = str(b) if not b == None else ''
    return sdkParamss

def u8_data_game (game):
    #组合游戏信息
    sql_game = sql.Initial_contrast('select * from game where appName="'+game+'"')[0]
    game_data = {
        'appName': sql_game[0], 
        'appID': str(sql_game[1]), 
        'appKey': sql_game[2], 
        'appDesc': sql_game[3], 
        'orientation': sql_game[4], 
        'cpuSupport': sql_game[5], 
        'outputApkName': sql_game[6],

        'minSdkVersion': sql_game[7],
        'targetSdkVersion': sql_game[8],
        'maxSdkVersion': sql_game[9],
        
        'versionCode': sql_game[10], 
        'versionName': sql_game[11], 
        'log': {
            'ulog.enable': sql_game[12], 
            'ulog.level': sql_game[13], 
            'ulog.local': sql_game[14], 
            'ulog.remote': sql_game[15], 
            'ulog.remote_interval': sql_game[16], 
            'ulog.remote_url': sql_game[17]
            }
        }
    SdkVersion = False

    for game_data_sub in game_data:
        if str(game_data_sub) == 'minSdkVersion' or str(game_data_sub) == 'targetSdkVersion' or str(game_data_sub) == 'maxSdkVersion':
            if game_data[game_data_sub] == None:
                SdkVersion = True
                break
    if SdkVersion :
        game_data.pop('minSdkVersion')
        game_data.pop('targetSdkVersion')
        game_data.pop('maxSdkVersion')
    return game_data


def u8_data_channel(game,channel):
    #组合渠道信息
    sql_channel = sql.Initial_contrast('select * from channel where game="'+game+'" and name="'+channel+'"')[0]
    sql_channel_sdkParams = sql.Initial_contrast('select * from channel_sdkParams where id='+str(sql_channel[12]))[0]
    sql_channel_params = sql.Initial_contrast('select * from channel_params where id='+str(sql_channel[13]))[0]
    sql_channel_operations = sql.Initial_contrast('select * from channel_operations where id='+str(sql_channel[14]))[0]
    sql_channel_plugins = sql.Initial_contrast('select * from channel_plugins where id='+str(sql_channel[15]))[0]
    channel_data = {
        'game': sql_channel[0],
        'id': sql_channel[1],
        'name': sql_channel[2],
        'sdk': sql_channel[3],
        'desc': sql_channel[4],
        'suffix': sql_channel[5],
        'splash': sql_channel[6],
        'splash_copy_to_unity': sql_channel[7],
        'icon': sql_channel[8],
        'gameName': sql_channel[9] if not str(sql_channel[9])=='None' else '' ,
        'sdkLogicVersionCode': sql_channel[10],
        'sdkLogicVersionName': sql_channel[11],
        'sdkParams': sdkParams(sql_channel_sdkParams), #12##
        'params': params(sql_channel_params), #13##
        'operations': operations(sql_channel_operations),  # 14##
        'plugins': plugins(sql_channel_plugins), #15##
        'sdkVersionCode': sql_channel[16],
        'sdkVersionName': sql_channel[17],
        'third-plugins': [] #18
        }
    return channel_data


def start_bag(game, channel):
    #总调用打包
    baseApkPath = file_utils.getFullPath('games/'+game+'/u8.apk')
    isPublic = True
    gamedata = u8_data_game(game)
    channeldata = u8_data_channel(game, channel)
    # print(gamedata)
    # print(channeldata)
    bag = core.pack(gamedata, channeldata, baseApkPath, isPublic)
    print(bag)
    return bag


def laypage(page,limit,ddta):
    #数据分页处理
    pagess = len(ddta)
    data = []
    pages = int(pagess/limit) if not (pagess/limit) > int(pagess/limit) else int(pagess/limit)+1
    if (int(page*limit)) >= (pages*limit):
        print(range(int((page-1)*limit), pagess))
        for i in range(int((page-1)*limit), pagess) :
            data.append(ddta[i])
    else:
        for i in  range(int((page-1)*limit), int(page*limit)) :
            data.append(ddta[i])
    return data


def packing_sub(game, channel):
    # 把提交打包的信息写入列队表
    channel = channel.split(',')
    for channel_sub in channel:
        sql_write_query =  sql.Initial_contrast("select id from packTask WHERE game='"+game+"' and channel='"+channel_sub+"'")
        if len(sql_write_query)==0:
            channelVersion = sql.Initial_contrast("select sdkVersionName from channel WHERE game='"+game+"' and name='"+channel_sub+"'")
            gameVersion = sql.Initial_contrast("select versionName from game WHERE appName='"+game+"'")
            startTime = time.strftime('%F %R')
            founder = 'admin'
            state = 'no'
            packTask_sql = "insert into `packTask` (`game`, `channel`, `channelVersion`, `gameVersion`, `startTime`, `founder`, `state`) VALUES ('"+str(game)+"','"+str(channel_sub)+"','"+str(channelVersion[0][0])+"','"+str(gameVersion[0][0])+"','"+str(startTime)+"','"+str(founder)+"','"+str(state)+"')"
            aaa = sql.write(packTask_sql)
            print(aaa)

def packTaskdata_sub():
    #获取列队表
    taskdata = []
    bagdata = sql.Initial_contrast("select id,game,channel,channelVersion,gameVersion,startTime,founder,state,journal,link from packTask")
    for bagdata_sub in bagdata:
        game = sql.Initial_contrast("select appDesc from game WHERE appName='"+str(bagdata_sub[1])+"'")
        channel = sql.Initial_contrast("select appDesc from game WHERE appName='"+str(bagdata_sub[2])+"'")
        game = str(game[0][0]) if not len(game) == 0 else str(bagdata_sub[1])
        channel = str(channel[0][0]) if not len(channel) == 0 else str(bagdata_sub[2])
        taskdata.append({'id': str(bagdata_sub[0]), 'game': game, 'channel': channel, 'channelVersion': str(bagdata_sub[3]), 'gameVersion': str(bagdata_sub[4]), 'startTime': str(bagdata_sub[5]), 'founder': str(bagdata_sub[6]), 'state': str(bagdata_sub[7]), 'journal': str(bagdata_sub[8]), 'link': str(bagdata_sub[9])})
    return taskdata
    
def gameData_sub():
    # 查询游戏数据
    gameta = []
    gameda = sql.Initial_contrast("select appName,appID,appKey,appDesc,versionCode,versionName from game")
    for game_sub in gameda:
        gameta.append({'appName': game_sub[0], 'appID': game_sub[1], 'appKey': game_sub[2],'appDesc': game_sub[3], 'versionCode': game_sub[4], 'versionName': game_sub[5],'sign':game_sub[0]})
    return gameta

def game_write(details):
    #游戏数据修改
    sign,appName, appID, appKey, appDesc, versionCode, versionName = details['sign'], details['appName'],details['appID'], details['appKey'], details['appDesc'], details['versionCode'], details['versionName']
    game_write_sql = 'update `game` set appName="'+appName+'", appID="'+appID+'", outputApkName="'+appName+'_{channelName}.apk", appKey="'+appKey+'", appDesc="'+appDesc+'", versionCode="'+versionCode+'", versionName="'+versionName+'" where appName="'+sign+'"'
    print(game_write_sql)
    write_ok = write(game_write_sql)
    return str(write_ok)

def game_found(details):
    #游戏数据创建
    appName, appID, appKey, appDesc, versionCode, versionName = details['appName'], details['appID'], details['appKey'], details['appDesc'], details['versionCode'], details['versionName']
    game_found_sql = 'insert into game (`appName`,`appID`,`appKey`,`appDesc`,`orientation`,`cpuSupport`,`outputApkName`,`versionCode`,`versionName`,`ulog.enable`,`ulog.level`,`ulog.local`,`ulog.remote`,`ulog.remote_interval`,`ulog.remote_url`)  values ("'+appName +'", '+appID+', "'+appKey+'", "'+appDesc+'", "landscape", "armeabi|armeabi-v7a|x86|mips", "'+appName + '_{channelName}.apk", "'+versionCode+'", "'+versionName+'", "true", "DEBUG", "true", "true", "1000", "http://192.168.1.108:8090/")'
    write_ok = write(game_found_sql)
    return str(write_ok)

def Currency_query():
    # 查询渠道通用数据
    channelta = []
    channelda = sql.Initial_contrast("select name,pluginsName,paramskey1,paramskey2,paramskey3,paramskey4,paramskey5,paramskey6,paramskey7,paramskey8,paramskey9 from `channel_currency`")
    for channel_sub in channelda:
        channelta.append({'sign': channel_sub[0], 'name': channel_sub[0], 'pluginsName': channel_sub[1], 'paramskey1': channel_sub[2], 'paramskey2': channel_sub[3], 'paramskey3': channel_sub[4],'paramskey4': channel_sub[5], 'paramskey5': channel_sub[6], 'paramskey6': channel_sub[7], 'paramskey7': channel_sub[8], 'paramskey8': channel_sub[9], 'paramskey9': channel_sub[10]})
    channelta.append({'name':'','pluginsName':'','paramskey1':'','paramskey2':'','paramskey3':'','paramskey4':'','paramskey5':'','paramskey6':'','paramskey7':'','paramskey8':'','paramskey9':'','sign':''})
    return channelta

def channel_query(game, channel):
    #游戏接入渠道主要信息
    channelda = sql.Initial_contrast("select id,suffix,splash,icon,gameName,sdkLogicVersionCode,sdkLogicVersionName,sdkVersionCode,sdkVersionName from `channel` where game='"+game+"' and name='"+channel+"'")
    if len(channelda)==0:
        configdata=[
            {'key': 'game', 'value': game, 'illustrate': '数据所属的游戏'},
            {'key': 'id', 'value': '', 'illustrate': '渠道id'},
            {'key': 'name', 'value': channel, 'illustrate': '渠道英文缩写'},
            {'key': 'suffix', 'value': '', 'illustrate': '包名'},
            {'key': 'splash', 'value': '', 'illustrate': '闪屏'},
            {'key': 'icon', 'value': '', 'illustrate': '图标'},
            {'key': 'gameName', 'value': '', 'illustrate': '游戏中文名'},
            {'key': 'sdkLogicVersionCode', 'value': '', 'illustrate': 'sdkLogic版本号'},
            {'key': 'sdkLogicVersionName', 'value': '', 'illustrate': 'sdkLogic版本名'},
            {'key': 'sdkVersionCode', 'value': '', 'illustrate': 'SDK版本号'},
            {'key': 'sdkVersionName', 'value': '', 'illustrate': 'SDK版本名'}
        ]
    else:
        configdata = [
            {'key': 'game', 'value': game, 'illustrate': '数据所属的游戏'},
            {'key': 'id', 'value': channelda[0][0], 'illustrate': '渠道id'},
            {'key': 'name', 'value': channel, 'illustrate': '渠道英文缩写'},
            {'key': 'suffix', 'value': channelda[0][1], 'illustrate': '包名'},
            {'key': 'splash', 'value': channelda[0][2], 'illustrate': '闪屏'},
            {'key': 'icon', 'value': channelda[0][3], 'illustrate': '图标'},
            {'key': 'gameName', 'value': channelda[0][4], 'illustrate': '游戏中文名'},
            {'key': 'sdkLogicVersionCode', 'value': channelda[0][5], 'illustrate': 'sdkLogic版本号'},
            {'key': 'sdkLogicVersionName', 'value': channelda[0][6], 'illustrate': 'sdkLogic版本名'},
            {'key': 'sdkVersionCode', 'value': channelda[0][7], 'illustrate': 'SDK版本号'},
            {'key': 'sdkVersionName', 'value': channelda[0][8], 'illustrate': 'SDK版本名'}
            ]
    # configdata.append({'key': '', 'value': '', 'illustrate': '主要信息添加券'})
    return configdata

def params_query(paramsid):
    #渠道子数据params查询
    channel_lin=[]
    channel_params = sql.Initial_contrast("select name1,value1,name2,value2,name3,value3,name4,value4,name5,value5,name6,value6,name7,value7,name8,value8,name9,value9 from `channel_params` where id='"+paramsid+"'")
    params_sub = channel_params[0]
    for params_int in range(0,18,2):
        if not params_sub[params_int]==None:
            channel_lin.append({'key': params_sub[params_int], 'illustrate': 'params组数据', 'value': params_sub[params_int+1]})
    channel_lin.append({'key': '', 'illustrate': 'params组数据', 'value': ''})
    return channel_lin

def sdkParams_query(sdkParamsid):
    #渠道子数据sdkParams查询
    sdkParams_lin=[]
    sdkParams_params = sql.Initial_contrast("select * from `channel_sdkParams` where id='"+sdkParamsid+"'")
    params_sub = sdkParams_params[0]
    for params_int in range(1,19,2):
        if not params_sub[params_int]==None:
            sdkParams_lin.append({'key': params_sub[params_int], 'illustrate': 'sdkParams组数据', 'value': params_sub[params_int+1]})
    sdkParams_lin.append({'key': '', 'illustrate': 'params组数据', 'value': ''})
    return sdkParams_lin

def operations_query(operationsid):
    #渠道子数据operations查询
    operations_lin=[]
    operations_params = sql.Initial_contrast("select * from `channel_operations` where id='"+operationsid+"'")
    params_sub = operations_params[0]
    for params_int in range(1,28,3):
        if not params_sub[params_int]==None:
            operations_lin.append({'type': params_sub[params_int], 'from': params_sub[params_int+1], 'to': params_sub[params_int+2]})
    operations_lin.append({'type': '', 'from': '', 'to': ''})
    return operations_lin

def channel_config_sub(game, channel, subb):
    #渠道子数据查询更新
    configdataSub = []
    ascription_sql = sql.Initial_contrast("select params,name from `channel` where game='"+game+"' and name='"+channel+"'")
    if subb=='params':
        if len(ascription_sql) == 0:
            configdataSub = [{'key': '', 'illustrate': 'params组数据', 'value': ''}]
        else:
            configdataSub = params_query(ascription_sql[0][0])
    elif subb == 'operations':
        if len(ascription_sql) == 0:
            configdataSub = [{'type': '', 'from': '', 'to': ''}]
        else:
            configdataSub = operations_query(ascription_sql[0][0])
    elif subb == 'sdkParams':
        if len(ascription_sql) == 0:
            configdataSub =[{'key': '', 'illustrate': 'params组数据', 'value': '','right': 'up'}]
        else:
            configdataSub = sdkParams_query(ascription_sql[0][0])
    return configdataSub


def found_channel_sql(game, channel):
    # 数据库没有该渠道信息，添加数据库
    params_sub_value,params_sub_key,lng = '','',1
    plugins_data = str(sql.Initial_contrast('select `pluginsName` from `channel_currency` where name="'+channel+'"')[0][0])
    sql_sign = str(int(time.time()*10000000000)+ random.randint(0, 999999999))
    channel_params_sub = sql.Initial_contrast("select paramskey1,paramskey2,paramskey3,paramskey4,paramskey5,paramskey6,paramskey7,paramskey8,paramskey9 from channel_currency where name='"+channel+"'")
    if not len(channel_params_sub)==0:
        for params_sub in [i for i in channel_params_sub[0] if not i=='' ]:
            params_sub_value = params_sub_value + '"'+params_sub+'","'+''+'","'+'1'+'","'+params_sub+'","'+'0'+'","'+'1'+'",'
            params_sub_key = params_sub_key + '`name'+str(lng)+'`,`value'+str(lng)+'`,`required'+str(lng)+'`,`showName'+str(lng)+'`,`bWriteInManifest'+str(lng)+'`,`bWriteInClient'+str(lng)+'`,'
            lng = lng + 1
    channel_sql_write = 'insert into channel (`sdkParams`,`params`,`operations`,`plugins`,`game`,`name`,`sdk`,`desc`) values ("'+sql_sign+'","'+sql_sign+'","'+sql_sign+'","'+sql_sign+'","'+game+'","'+channel+'","'+channel+'","'+channel+'SDK")'
    sdkParams_sql_write = 'insert into channel_sdkParams (`id`) values ("'+sql_sign+'")'
    params_sql_write = 'insert into channel_params ('+params_sub_key+'`id`) values ('+params_sub_value+'"'+sql_sign+'")'
    operations_sql_write = 'insert into channel_operations (`id`) values ("'+sql_sign+'")'
    plugins_sql_write = 'insert into channel_plugins (`id`,`name1`,`type1`,`name2`,`type2`) values ("'+sql_sign+'","com.u8.sdk.'+plugins_data+'User","1","com.u8.sdk.'+plugins_data+'Pay","2")'
    write(channel_sql_write)
    write(sdkParams_sql_write)
    write(params_sql_write)
    write(operations_sql_write)
    write(plugins_sql_write)
    return sql_sign


def operations_number_query(operationsid, valuess=None):
    #查询数据位置节点
    operations_number = sql.Initial_contrast('select * from `channel_operations` where id="'+operationsid+'"')
    operations_sub = operations_number[0]
    for operations_int in range(1, 28, 3):
        if operations_sub[operations_int] == valuess:
            return int(((operations_int-1)/3)+1)


def params_number_query(paramsid, valuess=None):
    #查询数据位置节点
    channel_params = sql.Initial_contrast("select name1,value1,name2,value2,name3,value3,name4,value4,name5,value5,name6,value6,name7,value7,name8,value8,name9,value9 from `channel_params` where id='"+paramsid+"'")
    params_sub = channel_params[0]
    for params_int in range(0,18,2):
        if params_sub[params_int] == valuess:
            return int((params_int/2)+1)


def sdkParams_number_query(sdkParamsid, valuess=None):
    #查询数据位置节点
    sdkParams_params = sql.Initial_contrast("select * from `channel_sdkParams` where id='"+sdkParamsid+"'")
    params_sub = sdkParams_params[0]
    for params_int in range(1,19,2):
        if params_sub[params_int] == valuess:
            return int(((params_int-1)/2)+1)

def channel_write(details):
    # 渠道信息添加
    subb = details['subb']
    if subb == 'channel_currency':
        name, pluginsName, paramskey1, paramskey2, paramskey3, paramskey4, paramskey5, paramskey6, paramskey7, paramskey8, paramskey9 = details['name'], details['pluginsName'], details['paramskey1'], details['paramskey2'], details['paramskey3'], details['paramskey4'], details['paramskey5'], details['paramskey6'], details['paramskey7'], details['paramskey8'], details['paramskey9']
        currency_sql_write = 'insert into channel_currency (`name`, `pluginsName`, `paramskey1`, `paramskey2`, `paramskey3`, `paramskey4`, `paramskey5`, `paramskey6`, `paramskey7`, `paramskey8`, `paramskey9`) values ("'+name+'", "'+pluginsName+'", "'+paramskey1+'", "'+paramskey2+'", "'+paramskey3+'", "'+paramskey4+'", "'+paramskey5+'", "'+paramskey6+'", "'+paramskey7+'", "'+paramskey8+'", "'+paramskey9+'")'
        write_ok = write(currency_sql_write)
        return str(write_ok)

    game, channel = details['game'], details['channel']
    inspect = sql.Initial_contrast('select `params` from `channel`  where game="'+game+'" and name="'+channel+'"')
    if len(inspect)==0:
        identifyid = found_channel_sql(game, channel)
    else:
        identifyid = inspect[0][0]

    if subb=='channel_operations':
        strat = str(operations_number_query(identifyid))
        write_sql = 'update `channel_operations` set type'+strat+'="'+str(details['type'])+'",from'+strat+'="'+str(details['from'])+'",to'+strat+'="'+str(details['to'])+'" where id="'+identifyid+'"'
        write_ok = write(write_sql)
        return str(write_ok)
    elif subb == 'channel_params':
        strat = str(params_number_query(identifyid))
        write_sql = 'update `channel_params` set name'+strat+'="'+str(details['key'])+'",value'+strat+'="'+str(details['value'])+'",required'+strat+'="1",showName'+strat+'="'+str(details['key'])+'",bWriteInManifest'+strat+'="0",bWriteInClient'+strat+'="1" where id="'+identifyid+'"'
        write_ok = write(write_sql)
        return str(write_ok)
    elif subb == 'channel_sdkParams':
        strat = str(sdkParams_number_query(identifyid))
        write_sql = 'update `channel_sdkParams` set key'+strat+'="'+str(details['key'])+'",value'+strat+'="'+str(details['value'])+'" where id="'+identifyid+'"'
        write_ok = write(write_sql)
        return str(write_ok)

    return 'ok'


def channel_modify(details):
    # 渠道信息修改
    subb = details['subb']
    if subb == 'channel_currency':
        sign,name, pluginsName, paramskey1, paramskey2, paramskey3, paramskey4, paramskey5, paramskey6, paramskey7, paramskey8, paramskey9 = details['sign'], details['name'], details['pluginsName'], details['paramskey1'], details['paramskey2'], details['paramskey3'], details['paramskey4'], details['paramskey5'], details['paramskey6'], details['paramskey7'], details['paramskey8'], details['paramskey9']
        write_sql = 'update `channel_currency` set name="'+name+'", pluginsName="'+pluginsName+'", paramskey1="'+paramskey1+'", paramskey2="'+paramskey2+'", paramskey3="'+paramskey3+'", paramskey4="'+paramskey4+'", paramskey5="'+paramskey5+'", paramskey6="'+paramskey6+'", paramskey7="'+paramskey7+'", paramskey8="'+paramskey8+'", paramskey9="'+paramskey9+'" where name="'+sign+'"'
        write_ok = write(write_sql)
        return str(write_ok)

    game, channel = details['game'], details['channel']
    inspect = sql.Initial_contrast('select `params` from `channel`  where game="'+game+'" and name="'+channel+'"')
    if len(inspect) == 0:
        identifyid = found_channel_sql(game, channel)
    else:
        identifyid = inspect[0][0]

    if subb=='channel_operations':
        strat = str(operations_number_query(identifyid, valuess=str(details['type'])))
        print(strat)
        write_sql = 'update `channel_operations` set type'+strat+'="'+str(details['type'])+'",from'+strat+'="'+str(details['from'])+'",to'+strat+'="'+str(details['to'])+'" where id="'+identifyid+'"'
        write_ok = write(write_sql)
        return str(write_ok)
    elif subb == 'channel_params':
        strat = str(params_number_query(identifyid, valuess=str(details['key'])))
        print(strat)
        write_sql = 'update `channel_params` set name'+strat+'="'+str(details['key'])+'",value'+strat+'="'+str(details['value'])+'",required'+strat+'="1",showName'+strat+'="'+str(details['key'])+'",bWriteInManifest'+strat+'="0",bWriteInClient'+strat+'="1" where id="'+identifyid+'"'
        write_ok = write(write_sql)
        return str(write_ok)
    elif subb == 'channel_sdkParams':
        strat = str(sdkParams_number_query(identifyid, valuess=str(details['key'])))
        print(strat)
        write_sql = 'update `channel_sdkParams` set key'+strat+'="'+str(details['key'])+'",value'+strat+'="'+str(details['value'])+'" where id="'+identifyid+'"'
        write_ok = write(write_sql)
        return str(write_ok)
    elif subb == 'channel':
        write_sql = 'update `channel` set '+str(details['key'])+'="'+str(details['value'])+'"  where game="'+game+'" and name="'+channel+'"'
        write_ok = write(write_sql)
        return str(write_ok)

    return 'ok'
