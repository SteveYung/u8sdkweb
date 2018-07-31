import file_utils
import os
import os.path
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import SubElement
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import ElementTree
import os
import os.path
import zipfile
import re
import subprocess
import platform
from xml.dom import minidom
import codecs
import sys

androidNS = 'http://schemas.android.com/apk/res/android'


def execute(channel, pluginInfo, decompileDir, packageName):

	if 'params' in pluginInfo and len(pluginInfo['params']) > 0:
		for param in pluginInfo['params']:
			name = param.get('name')
			if name == 'UMENG_CHANNEL':
				param['value'] = channel['name']
				break
