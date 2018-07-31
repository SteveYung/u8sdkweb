#coding:utf-8
# -*- coding: UTF-8 -*-
import os
import time
import random
import config_utils
import sql
isPublic = True


def query(gamename, channelid, channelname):
    #数据查询
    result = sql.Initial_contrast("select id from channel where id='"+str(channelid) +"' and game='"+str(gamename)+"' and name='"+str(channelname)+"'")
    print("select id from channel where id='"+str(channelid) +"' and game='"+str(gamename)+"' and name='"+str(channelname)+"'")
    if len(result) == 0:
        return True
    else:
        return False

def write(sql_write):
    #数据写入
    if not sql.write(sql_write):
        if not sql.write(sql_write):
            if not sql.write(sql_write):
                print('######################################')
                print(sql_write)
                print('######################################')
                return False
    return True

def game_config_xml():
    for filename in os.listdir(os.getcwd()+'/games'):
        filename = str(filename)
        if not (filename == 'sql.py' or filename == 'games.xml' or filename == 'games.py' or filename == '__pycache__' or filename == 'config_utils.py' or filename == 'file_utils.py' or filename == 'log_utils.py' or filename == 'log'):#排除非正常目录文件
            print(filename)
            channels = config_utils.getAllChannels(filename, isPublic)#读取目录config内容
            for channel in channels:
                channel_sql_key = channel_sql_value = sdkParams_sql_key = sdkParams_sql_value = params_sql_key = params_sql_value = operations_sql_key = operations_sql_value = plugins_sql_key = plugins_sql_value = ''
                for channel_sub in channel:
                    channel_sub = str(channel_sub)
                    if not(channel_sub == 'params' or channel_sub == 'operations' or channel_sub == 'plugins' or channel_sub == 'sdkParams' or channel_sub == 'third-plugins'):
                        # print(channel_sub+' : '+ channel[channel_sub])
                        channel_sql_key = channel_sql_key+'`'+str(channel_sub)+'`,'
                        channel_sql_value = channel_sql_value+'"'+str(channel[channel_sub])+'",'

                    if channel_sub == 'sdkParams':
                        sdkParams = channel[channel_sub]
                        sdkParamint = 1
                        for sdkParam in sdkParams:
                            # print(sdkParam+' : ' + sdkParams[sdkParam])
                            sdkParams_sql_key = sdkParams_sql_key+'`key'+str(sdkParamint)+'`,`value'+str(sdkParamint)+'`,'
                            sdkParams_sql_value = sdkParams_sql_value+'"'+str(sdkParam)+'","'+str(sdkParams[sdkParam])+'",'
                            sdkParamint = sdkParamint+1
                    
                    if channel_sub == 'params':
                        params = channel[channel_sub]
                        paramint = 1
                        for param in params:
                            for param_sub in param:
                                # print(param_sub+' : ' + param[param_sub])
                                params_sql_key = params_sql_key+'`'+str(param_sub)+str(paramint)+'`,'
                                params_sql_value = params_sql_value+'"'+str(param[param_sub])+'",'
                            paramint = paramint + 1

                    if channel_sub == 'operations':
                        operations = channel[channel_sub]
                        operationint = 1
                        for operation in operations:
                            for operation_sub in operation:
                                # print(operation_sub+' : ' + operation[operation_sub])
                                operations_sql_key = operations_sql_key+'`'+str(operation_sub)+str(operationint)+'`,'
                                operations_sql_value = operations_sql_value+'"'+str(operation[operation_sub])+'",'
                            operationint = operationint + 1

                    if channel_sub == 'plugins':
                        plugins = channel[channel_sub]
                        pluginint = 1
                        for plugin in plugins:
                            for plugin_sub in plugin:
                                # print(plugin_sub+' : ' + plugin[plugin_sub])
                                plugins_sql_key = plugins_sql_key+'`'+str(plugin_sub)+str(pluginint)+'`,'
                                plugins_sql_value = plugins_sql_value+'"'+str(plugin[plugin_sub])+'",'
                            pluginint = pluginint + 1
                    
                    if channel_sub == 'id':
                        channelid = str(channel[channel_sub])
                    if channel_sub == 'name':
                        gamename = str(channel[channel_sub])

                sql_sign = str(int(time.time()*10000000000)+ random.randint(0, 999999999))
                channel_sql_write = 'insert into channel ('+channel_sql_key + '`sdkParams`,`params`,`operations`,`plugins`,`game`) values (' + channel_sql_value+'"'+sql_sign+'","'+sql_sign+'","'+sql_sign+'","'+sql_sign+'","'+filename+'")'
                sdkParams_sql_write = 'insert into channel_sdkParams ('+sdkParams_sql_key+'`id`) values ('+sdkParams_sql_value+'"'+sql_sign+'")'
                params_sql_write = 'insert into channel_params ('+params_sql_key+'`id`) values ('+params_sql_value+'"'+sql_sign+'")'
                operations_sql_write = 'insert into channel_operations ('+operations_sql_key+'`id`) values ('+operations_sql_value+'"'+sql_sign+'")'
                plugins_sql_write = 'insert into channel_plugins ('+plugins_sql_key+'`id`) values ('+plugins_sql_value+'"'+sql_sign+'")'

                if query(filename, channelid, gamename):
                    if write(channel_sql_write):  # 写入渠道信息
                        write(sdkParams_sql_write)
                        write(params_sql_write)
                        write(operations_sql_write)
                        write(plugins_sql_write)

            print('===================================================')

game_config_xml()


