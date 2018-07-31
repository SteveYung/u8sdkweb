#!/usr/bin/env python
# -*- coding: utf-8 -*-


import games
import main
import main_thread
import sys
import http_utils
import argparse
import stat

if __name__ == "__main__":

    parser = argparse.ArgumentParser(u"U8SDK 打包工具")
    parser.add_argument('-r', '--release', help=u"标记为正式包，非正式包会在包名后面加上.debug",action="store_true", dest="release", default=True)
    parser.add_argument('-s', '--select', help=u"让用户自己选择需要打包的渠道。否则将会打出所有渠道包", action="store_true", dest="selectable", default=True)
    parser.add_argument('-t', '--thread', help=u"全部打包时的打包线程数量", action='store', dest="threadNum", type=int, default=1)
    parser.add_argument('-g', '--game', help=u"游戏AppID")
    parser.add_argument('-c', '--channelName', help=u"指定渠道名,可以为*，这样打出该游戏的所有渠道")
    parser.add_argument('--version', help=u"查看当前使用的U8SDK版本", action='version', version='v2.0')

    args = parser.parse_args()

    print(args)

    games.entry(args.release, args.selectable, args.threadNum, args.game, args.channelName)