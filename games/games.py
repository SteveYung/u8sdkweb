#coding:utf-8
# -*- coding: UTF-8 -*-
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import sql
import os


def query(appName, appID):
    #数据查询
    result = sql.Initial_contrast("select appDesc from game where appName='"+str(appName) +"' and appID='"+str(appID)+"'")
    # print("select appDesc from game where appName='"+str(appName) +"' and appID='"+str(appID)+"'")
    if len(result) == 0:
        return True
    else:
        return False

def games_xal():
    # 把game.xml导入数据库
    tree = ET.parse("games.xml")
    root = tree.getroot()
    a = 0
    appName = appID = ''
    for game in root.iter("game"):
        a=a+1
        # print (game)
        name=''
        value=''
        for params in game.iter("param"):
            name = name+'`'+str(params.get('name'))+'`,'
            value = value+'"'+str(params.get('value'))+'",'
            if str(params.get('name')) == 'appName':
                appName = str(params.get('value'))
            if str(params.get('name')) == 'appID':
                appID = str(params.get('value'))
            # print(str(params.get('name'))+' : '+str(params.get('value')))

        sql_write = 'insert into game ('+name[:-1]+') values ('+value[:-1]+')'
        # print(sql_write)
        # print(query(appName, appID))
        if query(appName, appID):
            if not sql.write(sql_write):
                if not sql.write(sql_write):
                    if not sql.write(sql_write):
                        print(sql_write)
    print(a)


games_xal()
