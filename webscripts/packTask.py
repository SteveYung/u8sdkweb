# -*- coding: utf-8 -*-
import pack
import sql
import os
import file_utils
import time
import shutil

bag_datas = sql.Initial_contrast('select `game`, `channel` from `packTask` where state="no"')

for bag_data in bag_datas:
    print(bag_data)
    gamename,channelname = str(bag_data[0]),str(bag_data[1])
    try:
        bag_ok = pack.start_bag(gamename, channelname)
    finally:
        ttime = str(time.time()*1000000).replace('.', '')
        log_file = file_utils.getFullPath('log/u8sdk.log')
        log_upto = file_utils.getFullPath('webscripts/static/u8sdklog/'+channelname+'-'+gamename+'-'+ttime+'.txt')
        log_uurl = '/u8sdklog/'+channelname+'-'+gamename+'-'+ttime+'.txt'
        apk_file = file_utils.getFullPath('output/'+gamename+'/'+channelname+'/'+gamename+'_'+channelname+'.apk')
        apk_upto = file_utils.getFullPath('webscripts/static/outapk/'+gamename+'_'+channelname+'.apk')
        apl_uurl = '/outapk/'+gamename+'_'+channelname+'.apk'
        shutil.copyfile(log_file, log_upto)  # 复制日志文件
        if bag_ok == 0:
            shutil.move(apk_file,apk_upto) #把apk移动到可访问目录
            bag_sql = sql.write('update `packTask` set state="yes",journal="'+log_uurl+'",link="'+apl_uurl+'" where game="'+gamename+'" and channel="'+channelname+'"')
        else:
            bag_sql = sql.write('update `packTask` set state="no",journal="'+log_uurl+'" where game="'+gamename+'" and channel="'+channelname+'"')
    # os.path.exists(test_file.txt) #检查文件存在
