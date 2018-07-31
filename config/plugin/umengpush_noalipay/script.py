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
	manifestFile = decompileDir + "/AndroidManifest.xml"
	manifestFile = file_utils.getFullPath(manifestFile)
	ET.register_namespace('android', androidNS)
	key = '{' + androidNS + '}launchMode'

	tree = ET.parse(manifestFile)
	root = tree.getroot()
	package = root.attrib.get('package')

	applicationNode = root.find('application')
	if applicationNode is None:
		return 1

	key = '{'+androidNS+'}name'
	receiverNodeList = applicationNode.findall('receiver')

	if receiverNodeList != None:
		for node in receiverNodeList:
			if node.attrib[key] == 'com.umeng.message.RegistrationReceiver':
				intentNodeLst = node.findall('intent-filter')
				if intentNodeLst is None:
					break

				for intentNode in intentNodeLst:
					actionNodeList = intentNode.findall('action')
					if actionNodeList is None:
						break

					for actionNode in actionNodeList:
						if actionNode.attrib[key].endswith('intent.action.COMMAND'):
							newVal = package + ".intent.action.COMMAND";
							actionNode.set(key, newVal)



	serviceNodeList = applicationNode.findall('service')

	if serviceNodeList != None:
		for node in serviceNodeList:
			if node.attrib[key] == 'com.umeng.message.UmengService':
				intentNodeLst = node.findall('intent-filter')
				if intentNodeLst is None:
					break

				for intentNode in intentNodeLst:
					actionNodeList = intentNode.findall('action')
					if actionNodeList is None:
						break

					for actionNode in actionNodeList:
						if actionNode.attrib[key].endswith('intent.action.START'):
							newVal = package + '.intent.action.START'
							actionNode.set(key, newVal)

						if actionNode.attrib[key].endswith('intent.action.COCKROACH'):
							newVal = package + '.intent.action.COCKROACH'
							actionNode.set(key, newVal)	



	tree.write(manifestFile, 'UTF-8')

	return 0

