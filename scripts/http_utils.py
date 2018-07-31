#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author xiaohei
# Date 2015-06-18

import config_utils
#python3.x urllib2,urllib,urlparse,robotparser合并到了urllib中，形成了多个子库
if config_utils.is_py_env_2():
    import urllib2
    import urlparse
else:

    import urllib.request as urllib2
    import urllib.parse as urlparse

def get(url, params):

    full_url = url
    if params != None and len(params) > 0:
        data = urlparse.urlencode(params)
        full_url = full_url + "?" + data

    f = urllib2.urlopen(full_url)
    content = f.read()
    return content

    # with urllib2.urlopen(full_url) as f:
    #     content = f.read()

    # return content


def post(url, params):
    if params != None and len(params) > 0:
        data = urlparse.urlencode(params)
    else:
        data = ""

    data = data.encode('utf-8')

    request = urllib2.Request(url)
    request.add_header("Content-Type", "application/x-www-form-urlencoded;charset=utf-8")

    with urllib2.urlopen(request, data) as f:
        content = f.read()

    return content




