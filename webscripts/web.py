# -*-coding: utf-8 - *-
from flask import Flask, jsonify, request, render_template, url_for
# from concurrent.futures import ThreadPoolExecutor#异步处理
from flask_cors import *
# gevent生产环境
# from gevent import monkey
# monkey.patch_all()
# from gevent import pywsgi
import base64
import sql
import os
import pack

web = Flask(__name__, static_url_path='')
CORS(web, supports_credentials=True)  # 允许跨域
# executor = ThreadPoolExecutor(5)  # 同时处理的最大线程数


@web.route('/admin', methods=['GET'])
def admin():
    #主页面
    return render_template('admin.html')

@web.route('/start_packing', methods=['GET'])
def start_packing():
    #开始打包界面
    imgbasename = {}
    gamepath = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))+'/games'
    for filename in os.listdir(gamepath):
        if not (filename == 'sql.py' or filename == 'games.xml' or filename == 'games.py' or filename == '__pycache__' or filename == 'config_utils.py' or filename == 'file_utils.py' or filename == 'log_utils.py' or filename == 'log'):  # 排除非正常目录文件
            doscname = sql.Initial_contrast("select appDesc from game where appName='"+filename+"'")
            doscname = str(doscname[0][0]) if not len(doscname)==0 else '无法获取名字'
            f = open(gamepath+'/'+filename+'/icon/icon.png', 'rb')  # 二进制方式打开图文件
            iconbase64 = base64.b64encode(f.read())  # 读取文件内容，转换为base64编码
            imgbasename[filename] = {'doc': str(doscname),'base':str(iconbase64)[:-1][2:],'name':filename}
            f.close()
    context = {
        'imgbasename': imgbasename
    }

    return render_template('start_packing.html', **context)

@web.route('/packTask', methods=['GET'])
def packTask():
    #渠道包管理界面
    return render_template('packTask.html')

@web.route('/gameadmin', methods=['GET'])
def gameadmin():
    #游戏管理界面
    return render_template('gameadmin.html')

@web.route('/channeladmin', methods=['GET'])
def channeladmin():
    #渠道管理界面
    details = request.args
    context = {
        'game': details.get('game')
        }
    return render_template('channeladmin.html', **context)


@web.route('/configuration/<game>/<channel>', methods=['GET'])
def configuration(game, channel):
    #游戏渠道参数配置
    if game == 'None' or channel == 'None':
        return '游戏或者渠道参数没有输入呦！！！'
    context = {
        'game': game,
        'channel': channel
    }
    return render_template('configuration.html', **context)

@web.route('/channeldata/<game>', methods=['GET'])
def channeldata(game):
    #获取游戏包含渠道的接口
    sql_data = sql.Initial_contrast("select `name`,`id`,`sdkVersionName` from channel where game='"+game+"'")
    gamedata = []
    for sql_data_sub in sql_data:
        gamedata.append({'name': sql_data_sub[0], 'id': sql_data_sub[1], 'edition': sql_data_sub[2], 'state': 'ok', })

    return jsonify({"code": 0, "msg": "ok", "count": len(gamedata), "data": gamedata})


@web.route('/confirmdata/<game>/<channel>', methods=['GET'])
def confirmdata(game, channel):
    #获取确认信息的接口
    gamedata = []
    channel = channel.split(',')
    for channel_sub in channel:
        sql_data = sql.Initial_contrast("select `sdkVersionName` from channel where game='"+game+"' and name='"+channel_sub+"'")
        gamedata.append({'game': game, 'channel': channel_sub,'phone': 'android', 'edition': sql_data[0][0]})

    return jsonify({"code": 0, "msg": "ok", "count": len(gamedata), "data": gamedata})


@web.route('/packing/<game>/<channel>', methods=['GET'])
def packing(game, channel):
    #提交打包信息写入列队表接口
    pack.packing_sub(game, channel)
    return 'ok'


@web.route('/packTaskdata', methods=['GET'])
def packTaskdata():
    #获取列队表接口
    details = request.args
    taskdata = pack.packTaskdata_sub()
    taskdata = pack.laypage(int(details.get('page')),int(details.get('limit')), taskdata)
    return jsonify({"code": 0, "msg": "ok", "count": len(taskdata), "data": taskdata})

@web.route('/gameData', methods=['GET'])
def gameData():
    #查询游戏数据接口
    details = request.args
    gameta = pack.gameData_sub()
    gamepage = pack.laypage(int(details.get('page')),int(details.get('limit')), gameta)
    gamepage.append({'appName':'', 'appID': '', 'appKey':'','appDesc': '', 'versionCode': '', 'versionName':'','neme':''})
    return jsonify({"code": 0, "msg": "ok", "count": len(gameta), "data": gamepage})


@web.route('/gameDataEdit', methods=['POST'])
def gameDataEdit():
    #游戏数据修改接口
    details = request.form
    return pack.game_write(details)


@web.route('/gameDataFound', methods=['POST'])
def gameDataFound():
    #游戏数据创建接口
    details = request.form
    return pack.game_found(details)

@web.route('/channelCurrency', methods=['GET'])
def channelCurrency():
    #查询渠道通用数据接口
    details = request.args
    channelta = pack.Currency_query()
    channeltage = pack.laypage(int(details.get('page')),int(details.get('limit')), channelta)
    return jsonify({"code": 0, "msg": "ok", "count": len(channelta), "data": channeltage})

@web.route('/configurationdata/<game>/<channel>', methods=['GET'])
def configurationdata(game, channel):
    #游戏接入渠道主要信息接口
    configdata = pack.channel_query(game, channel)
    return jsonify({"code": 0, "msg": "ok", "count": len(configdata), "data": configdata})

@web.route('/configurationdataSub/<game>/<channel>/<subb>', methods=['GET'])
def configurationdataSub(game, channel, subb):
    #渠道子数据查询接口
    configdataSub = pack.channel_config_sub(game, channel, subb)
    return jsonify({"code": 0, "msg": "ok", "count": len(configdataSub), "data": configdataSub})


@web.route('/channelupdata', methods=['POST'])
def channelupdata():
    #渠道信息添加接口
    details = request.form
    return pack.channel_write(details)


@web.route('/channelmodify', methods=['POST'])
def channelmodify():
    #渠道信息修改接口
    details = request.form
    return pack.channel_modify(details)


if __name__ == '__main__':
    web.run(host='0.0.0.0', port=5678, debug=True)

# #使用gevent布置
# server = pywsgi.WSGIServer(('0.0.0.0', 5678), web)
# server.serve_forever()











