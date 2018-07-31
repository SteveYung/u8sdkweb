#coding:utf-8 
# -*- coding: UTF-8 -*-
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from xml.etree.ElementTree import SubElement
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import ElementTree
from tkinter import *
from tkinter.ttk import *
import os

config_sdk='config\\sdk'
games='games'


# 字典区域
param_zd={
    'id': None,
    'name':'baidu',
    'sdk':'baidu',
    'desc':'baidu SDK',
    'suffix':'com.morefun.xsanguo.baidu',
    'splash':'0',
    'splash_copy_to_unity':'0',
    'icon':'rb'
}

sdk_params_zd={}

sdk_version_zd={
'versionCode':'1',
'versionName':'3.2.0'
}
# 总体标志区域

existence = {
    'id' : False  # ID是否存在于config中
}


def cleaning():
    param_zd['id'] = None
    param_zd['name'] = 'baidu'
    param_zd['sdk'] = 'baidu'
    param_zd['desc'] = 'baidu SDK'
    param_zd['suffix'] = 'com.morefun.xsanguo.baidu'
    param_zd['splash'] = '0'
    param_zd['splash_copy_to_unity'] = '0'
    param_zd['icon'] = 'rb'


def prettyXml(element, indent, newline, level=0):
    # xml美化
    if element:  # 判断element是否有子元素
        if element.text == None or element.text.isspace():  # 如果element的text没有内容
            element.text = newline + indent * (level + 1)
        else:
            element.text = newline + indent * \
                (level + 1) + element.text.strip() + \
                newline + indent * (level + 1)

    temp = list(element)  # 将elemnt转成list
    for subelement in temp:
        # 如果不是list的最后一个元素，说明下一个行是同级别元素的起始，缩进应一致
        if temp.index(subelement) < (len(temp) - 1):
            subelement.tail = newline + indent * (level + 1)
        else:  # 如果是list的最后一个元素， 说明下一行是母元素的结束，缩进应该少一个
            subelement.tail = newline + indent * level
        prettyXml(subelement, indent, newline, level=level + 1)  # 对子元素进行递归操作

def configxml_xie(jj):
    # 写入games-config
    tree_url = jj+"config.xml"
    tree = ET.parse(tree_url)
    root = tree.getroot()

    # 添加channel节点
    channel = root.find("channels")
    newEle = ET.Element("channel")
    newEle.attrib = {"name":"channel"}
    channel.append(newEle)

    # 添加sdk-params节点和sdk-version节点以及param元素
    #只有一个channels元素所以直接用find不需要二次for
    for sub_channel in root.find("channels"):
        print (sub_channel.get('name'))
        if sub_channel.get('name')=='channel':
            sub_channel.set('name','')
    
            # 通过字典添加param
            for sub_now_param in param_zd :
                now_param = ET.Element("param")
                now_param.attrib = {"name":sub_now_param,"value":param_zd[sub_now_param]}
                sub_channel.append(now_param)

            #添加sdk-params节点
            now_sdk_params = ET.Element("sdk-params")
            now_sdk_params.attrib = {"name":"params"}
            sub_channel.append(now_sdk_params)
        
            #添加sdk-version节点
            now_sdk_version = ET.Element("sdk-version")
            now_sdk_version.attrib = {"name":"version"}
            sub_channel.append(now_sdk_version)



    for sub_sdk_params in root.iter("sdk-params"):
        if sub_sdk_params.get('name')=='params':
            sub_sdk_params.set('name','')
            for paramss in sdk_params_zd :
                now_sdk_params = ET.Element("param")
                now_sdk_params.attrib = {"name":paramss,"value":sdk_params_zd[paramss]}
                sub_sdk_params.append(now_sdk_params)

    for sub_sdk_version in root.iter("sdk-version"):
        if sub_sdk_version.get('name')=='version':
            sub_sdk_version.set('name','')
            for versions in sdk_version_zd :
                now_sdk_version = ET.Element(versions)
                now_sdk_version.text = sdk_version_zd[versions]
                sub_sdk_version.append(now_sdk_version)        

    prettyXml(root, '\t', '\n') # 调用美化
    tree.write(tree_url, encoding="UTF-8", xml_declaration=True, method='xml')#保存


def game_du(gamesxx):
    # 查询到游戏名对应的游戏id
    tree = ET.parse("games\\games.xml")
    root = tree.getroot()
    
    for game in root.iter("game"):
        # print (game)
        for params in game.iter("param"):
            if str(params.get('value')) ==str(gamesxx):
                # print (params.get('name'))
                for games in game.iter("param"):
                    if str(games.get("name")) == 'appID':
                        return games.get("value")
             
def game_xie(appid_v,target_v):
    # 把打包数据写入到预备的xml内，方便打包程序调用
    target_v=game_du(target_v)
    print (target_v)
    tree = ET.parse("scripts\\test.xml")
    root = tree.getroot()

    for param in root.iter("param"):
        print (param)
        if str(param.get('name')) =='appid':
            param.set('value',appid_v)

        if str(param.get('name')) =='target':
            param.set('value',target_v)

    tree.write("scripts\\test.xml", encoding="UTF-8",xml_declaration=True,method='xml')
    tree.write("test.xml", encoding="UTF-8",xml_declaration=True,method='xml')


def configxml_yz(jj, channelsz):
    # 把config中对应ip的channel写入字典内
    tree_url = jj+"config.xml"
    tree = ET.parse(tree_url)
    root = tree.getroot()
    
    for channel in root.iter("channel"):
        # print (chansnel)
        for param in channel.iter("param"):
            # print (param.get('name')+' : ' + param.get('value'))
            if param.get('name') == 'id' and param.get('value') == channelsz:

                    print (param.get('name')+' : ' + param.get('value'))
                    print ("\n")
                    for param in channel.iter("param"):
                        param_zd[param.get('name')] = param.get('value')
                    
                    for params in channel.find("sdk-params").iter("param"):
                        sdk_params_zd[params.get('name')] = params.get('value')


def configxml_xg(jj, channelsz):
    # 当id拥有相对的节点时，将要把节点删除再重新写入节点
    tree_url = jj+"config.xml"
    print (tree_url)
    tree = ET.parse(tree_url)
    root = tree.getroot()

    channelx = root.find("channels")
    for channel in channelx.findall("channel"):
        for param in channel.findall("param"):
            # print (param.get('name')+' : ' + param.get('value'))
            if param.get('name') == 'id' and param.get('value') == channelsz:
                print (param.get('name')+' : ' + param.get('value'))
                print ("\n")
                channelx.remove(channel)#删除节点

    tree.write(tree_url, encoding="UTF-8",xml_declaration=True, method='xml')  # 保存
    configxml_xie(jj)


def aaa(jja, gamex, channelsz):
       
    jj='games\\'+jja+'\\'
    print (jj)
    print (existence['id'])

    if existence['id'] == False:
        configxml_xie(jj)
    elif existence['id'] == True:
        configxml_xg(jj, channelsz)
    print (param_zd)
    print ("\n")
    game_xie(gamex, jja)
    print ("=======================")
    print (param_zd)
    os.system('package_test.bat')


def bbb(jja, channel):
    print (channel)

    jj = 'games\\'+jja+'\\'
    print (jj)

    configxml_yz(jj, str(channel))

    # 字典写入输入框
    if param_zd['id'] == None:
        
        existence['id'] = False

        # 清理输入框数据
        e1.delete('0', 'end')
        e3.delete('0', 'end')
        a1.delete('0', 'end')
        a2.delete('0', 'end')
        # 清空下面的面板防止信息叠加不对称
        e_zd_key = [e5, e7, e9, e11, e13, e15, None]
        e_zd_value = [e6, e8, e10, e12, e14, e16, None]
        for zdkey in e_zd_key:
            if zdkey == None:
                break
            zdkey.delete('0', 'end')

        for zdvalue in e_zd_value:
            if zdvalue == None:
                break
            zdvalue.delete('0', 'end')

        e1.insert('insert', '不存在id：'+str(channel))
    else:
        existence['id'] = True
        # e1.delete('0', 'end')
        # e1.insert('insert', param_zd['id']) #不需要叠加了
        e3.delete('0', 'end')
        e3.insert('insert', param_zd['suffix'])
        a1.delete('0', 'end')
        a1.insert('insert', param_zd['name'])
        a2.delete('0', 'end')
        a2.insert('insert', param_zd['splash'])

        # 字典分割转换为数组
        param_zd_key = list(sdk_params_zd.keys())
        param_zd_key.append(None)
        param_zd_value = list(sdk_params_zd.values())
        param_zd_value.append(None)
        # 由于面板的限制只能写六个数，多余的作废
        e_zd_key = [e5, e7, e9, e11, e13, e15, None]
        e_zd_value = [e6, e8, e10, e12, e14, e16, None]

        # 清空下面的面板防止信息叠加不对称
        for zdkey in e_zd_key :
            if zdkey == None:
                break
            zdkey.delete('0', 'end')
            
        for zdvalue in e_zd_value :
            if zdvalue == None:
                break
            zdvalue.delete('0', 'end')

        # 在后面添加 None 使用紧急机制，防止溢出
        for zd_key in range(len(e_zd_key)):
            if e_zd_key[zd_key] == None or param_zd_key[zd_key] == None:
                break
            e_zd_key[zd_key].delete('0', 'end')
            e_zd_key[zd_key].insert('insert', param_zd_key[zd_key])

        for zd_value in range(len(e_zd_value)):
            if e_zd_value[zd_value] == None or param_zd_value[zd_value] == None:
                break
            e_zd_value[zd_value].delete('0', 'end')
            e_zd_value[zd_value].insert('insert', param_zd_value[zd_value])

    print (param_zd)
    print ('\n')
    print (sdk_params_zd)
    print ('\n')
    print (existence['id'])

    sdk_params_zd.clear()  # 清空字典免得二次查询时残留旧信息
    param_zd.clear()  # param_zd清空
    cleaning()  # param_zd初始化



def sdk_value_Tkinter_a():
    
    cleaning()
    print (param_zd)

    if len(str(e1.get())) > 0 :
        param_zd['id']=str(e1.get())
    if len(str(a1.get())) > 0 :
        param_zd['name']=str(a1.get())
        param_zd['sdk']=str(a1.get())
        param_zd['desc']=str(a1.get())+' SDK'
    if len(str(e3.get())) > 0 :
        param_zd['suffix']=str(e3.get())
    if len(str(a2.get())) > 0 :
        param_zd['splash']=str(a2.get())

    if len(str(e5.get())) > 0 and len(str(e6.get())) > 0:
        sdk_params_zd[e5.get()]=e6.get()
    if len(str(e7.get())) > 0 and len(str(e8.get())) > 0:
        sdk_params_zd[e7.get()]=e8.get()
    if len(str(e9.get())) > 0 and len(str(e10.get())) > 0:
        sdk_params_zd[e9.get()]=e10.get()
    if len(str(e11.get())) > 0 and len(str(e12.get())) > 0:
        sdk_params_zd[e11.get()]=e12.get()
    if len(str(e13.get())) > 0 and len(str(e14.get())) > 0:
        sdk_params_zd[e13.get()]=e14.get()
    if len(str(e15.get())) > 0 and len(str(e16.get())) > 0:
        sdk_params_zd[e15.get()]=e16.get()

    aaa(str(a3.get()), str(a1.get()), str(e1.get()))


def channel_id():
    bbb(str(a3.get()), int(e1.get()))

sdk_value = Tk() # 初始化Tk()

sdk_value.geometry('700x350')
sdk_value.title("写入打包参数")# 设置窗口标题

Label(sdk_value, text="渠道ID:").grid(row=0)
Label(sdk_value, text="渠道名:").grid(row=1)
Label(sdk_value, text="包名:").grid(row=2)
Label(sdk_value, text="闪屏").grid(row=3)
Label(sdk_value, text="0:无,11:横屏,21:竖屏").grid(row=3, column=2)

Label(sdk_value, text="sdk参数1  name:").grid(row=4, column=0)
Label(sdk_value, text="  value:").grid(row=4, column=2)
Label(sdk_value, text="sdk参数2  name:").grid(row=5, column=0)
Label(sdk_value, text="  value:").grid(row=5, column=2)
Label(sdk_value, text="sdk参数3  name:").grid(row=6, column=0)
Label(sdk_value, text="  value:").grid(row=6, column=2)
Label(sdk_value, text="sdk参数4  name:").grid(row=7, column=0)
Label(sdk_value, text="  value:").grid(row=7, column=2)
Label(sdk_value, text="sdk参数5  name:").grid(row=8, column=0)
Label(sdk_value, text="  value:").grid(row=8, column=2)
Label(sdk_value, text="sdk参数6  name:").grid(row=9, column=0)
Label(sdk_value, text="  value:").grid(row=9, column=2)

# 定义输入框
e1 = Entry(sdk_value)
# e2 = Entry(sdk_value)
e3 = Entry(sdk_value)
# e4 = Entry(sdk_value)

e5 = Entry(sdk_value)
e6 = Entry(sdk_value)
e7 = Entry(sdk_value)
e8 = Entry(sdk_value)
e9 = Entry(sdk_value)
e10 = Entry(sdk_value)
e11 = Entry(sdk_value)
e12 = Entry(sdk_value)
e13 = Entry(sdk_value)
e14 = Entry(sdk_value)
e15 = Entry(sdk_value)
e16 = Entry(sdk_value)

# 输入框属性赋予
e1.grid(row=0, column=1,pady=3)
# e2.grid(row=1, column=1,pady=3)
e3.grid(row=2, column=1,pady=3)
# e4.grid(row=3, column=1,pady=3)

e5.grid(row=4, column=1,pady=3)
e6.grid(row=4, column=3,pady=3)
e7.grid(row=5, column=1,pady=3)
e8.grid(row=5, column=3,pady=3)
e9.grid(row=6, column=1,pady=3)
e10.grid(row=6, column=3,pady=3)
e11.grid(row=7, column=1,pady=3)
e12.grid(row=7, column=3,pady=3)
e13.grid(row=8, column=1,pady=3)
e14.grid(row=8, column=3,pady=3)
e15.grid(row=9, column=1,pady=3)
e16.grid(row=9, column=3,pady=3)


# 创建一个下拉列表
#渠道名
a1 = cmbEditCombo = Combobox(sdk_value, values=os.listdir(config_sdk))
a1.grid(row=1, column=1,pady=3)

#闪屏
a2 = cmbEditCombo = Combobox(sdk_value, values=[0,11,21])
a2.grid(row=3, column=1,pady=3)

#游戏
a3 = cmbEditCombo = Combobox(sdk_value, values=os.listdir(games))
a3.grid(row=1, column=3)

Button(sdk_value, text="查询渠道是否存在", width=28,command=channel_id).grid(row=0, column=2)

Button(sdk_value, text="确认以上内容",width=28,command=sdk_value_Tkinter_a).grid(row=11, column=2)

sdk_value.mainloop()

'''
row：   组件所在的行起始位置；
column: 组件所在的列起始位置；
Label : 标签，可以显示文字或图片

padx：设置控件周围水平方向空白区域保留大小
pady：设置控件周围垂直方向空白区域保留大小；

ipadx：设置控件里面水平方向空白区域大小
ipady：设置控件里面垂直方向空白区域大小；

delete('0', 'end') #清空内容
insert('insert', 'hell') #修改内容

a2['values']=[0,11,21] #修改下拉框的下拉内容
a2.bind("<<ComboboxSelected>>", show_msg)  #当a2选中值之后调用函数（show_msg）
'''
