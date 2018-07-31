import file_utils
import apk_utils
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

def generateShareSDKXmlFile(pluginInfo, decompileDir):
	assetsPath = file_utils.getFullPath(decompileDir) + "/assets"

	if not os.path.exists(assetsPath):
		os.makedirs(assetsPath)

	shareSdkXml = assetsPath + "/ShareSDK.xml"

	if os.path.exists(shareSdkXml):
		os.remove(shareSdkXml)
		
	tree = ElementTree()
	root = Element('DevInfor')
	tree._setroot(root)

	shareNode = SubElement(root, 'ShareSDK')

	if 'params' in pluginInfo and pluginInfo['params'] != None and len(pluginInfo['params']) > 0:
		for param in pluginInfo['params']:
			paramName = param.get('name')
			if paramName == 'AppKey':
				paramValue = param.get('value')
				shareNode.set('AppKey', paramValue)
				break

	subplugins = pluginInfo.get('subplugins')

	if subplugins != None and len(subplugins) > 0:
		index = 1
		for subplg in subplugins:
			subplgNode = SubElement(root, subplg['name'])
			subparams = subplg.get('params')
			if subparams != None and len(subparams) > 0:
				for subparam in subparams:
					subplgNode.set(subparam['name'], subparam['value'])

			if subplgNode.get('Id') == None:
				subplgNode.set('Id', str(index))
			else:
				subplgNode.attrib['Id'] = str(index)

			if subplgNode.get('Enable') == None:
				subplgNode.set('Enable', 'true')
			else:
				subplgNode.attrib['Enable'] = 'true'

			index = index + 1

	tree.write(shareSdkXml, 'UTF-8')


def appendAppIdForQZone(pluginInfo, decompileDir):
	qzoneAppID = None
	subplugins = pluginInfo.get('subplugins')

	appId = 0
	if subplugins != None and len(subplugins) > 0:
		for subplg in subplugins:
			if subplg['name'] == "QZone":
				params = subplg.get('params')
				for param in params:
					if param['name'] == 'AppId':
						appId = int(param['value'])
						break

			if appId > 0:
				break

	if appId == 0:
		return

	manifestFile = decompileDir + "/AndroidManifest.xml"
	manifestFile = file_utils.getFullPath(manifestFile)
	ET.register_namespace('android', androidNS)

	tree = ET.parse(manifestFile)
	root = tree.getroot()

	applicationNode = root.find('application')
	if applicationNode is None:
		return
	key = '{'+androidNS+'}name'
	scheme = '{'+androidNS+'}scheme'

	activityNodes = applicationNode.findall('activity')
	if activityNodes != None and len(activityNodes) > 0:
		for activityNode in activityNodes:
			name = activityNode.get(key)
			if name == 'com.mob.tools.MobUIShell':
				intentNodes = activityNode.findall('intent-filter')
				if intentNodes != None and len(intentNodes) > 0:
					for intentNode in intentNodes:
						dataNode = SubElement(intentNode, 'data')
						dataNode.set(scheme, 'tencent'+str(appId))
						break

				else:
					intentNode = SubElement(activityNode, 'intent-filter')
					dataNode = SubElement(intentNode, 'data')
					dataNode.set(scheme, 'tencent'+str(appId))
					actionNode = SubElement(intentNode, 'action')
					actionNode.set(key, 'android.intent.action.VIEW')
					categoryNode = SubElement(intentNode, 'category')
					categoryNode.set(key, 'android.intent.category.DEFAULT')
					categoryNode2 = SubElement(intentNode, 'category')
					categoryNode2.set(key, 'android.intent.category.BROWSABLE')

	tree.write(manifestFile, 'UTF-8')


def generateWXEntryActivity(channel, pluginInfo, decompileDir, packageName):

	sdkDir = decompileDir + '/../plugins/' + pluginInfo['name']
	if not os.path.exists(sdkDir):
		file_utils.printF("The plugin temp folder is not exists. path:"+sdkDir)
		return 1

	extraFilesPath = sdkDir + '/extraFiles'
	relatedJar = os.path.join(extraFilesPath, 'ShareSDK-Wechat-Core.jar')
	WXPayEntryActivity = os.path.join(extraFilesPath, 'WXEntryActivity.java')
	file_utils.modifyFileContent(WXPayEntryActivity, 'cn.sharesdk.socialization.sample.wxapi', packageName+".wxapi")


	splitdot = ';'
	if platform.system() == 'Darwin':
		splitdot = ':'

	cmd = '"%sjavac" -source 1.7 -target 1.7 "%s" -classpath "%s"%s"%s"' % (file_utils.getJavaBinDir(), WXPayEntryActivity, relatedJar, splitdot, file_utils.getFullToolPath('android.jar'))

	ret = file_utils.execFormatCmd(cmd)
	if ret:
		return 1

	packageDir = packageName.replace('.', '/')
	srcDir = sdkDir + '/tempDex'
	classDir = srcDir + '/' + packageDir + '/wxapi'

	if not os.path.exists(classDir):
		os.makedirs(classDir)

	sourceClassFilePath = os.path.join(extraFilesPath, 'WXEntryActivity.class')
	targetClassFilePath = classDir + '/WXEntryActivity.class'

	file_utils.copy_file(sourceClassFilePath, targetClassFilePath)

	targetDexPath = os.path.join(sdkDir, 'WXEntryActivity.dex')

	dxTool = file_utils.getFullToolPath("/lib/dx.jar")

	cmd = file_utils.getJavaCMD() + ' -jar -Xmx512m -Xms512m "%s" --dex --output="%s" "%s"' % (dxTool, targetDexPath, srcDir)



	ret = file_utils.execFormatCmd(cmd)

	if ret:
		return 1

	ret = apk_utils.dex2smali(targetDexPath, decompileDir+'/smali', "baksmali.jar")

	if ret:
		return 1

	manifest = decompileDir + '/AndroidManifest.xml'
	ET.register_namespace('android', androidNS)
	name = '{' + androidNS + '}name'
	theme = '{'+androidNS+'}theme'
	configChanges = '{' + androidNS + '}configChanges'
	exported = '{' + androidNS + '}exported'
	screenOrientation = '{' + androidNS + '}screenOrientation'
	tree = ET.parse(manifest)
	root = tree.getroot()

	appNode = root.find('application')
	if appNode is None:
		return 1

	activityNode = SubElement(appNode, 'activity')
	activityNode.set(name, packageName + '.wxapi.WXEntryActivity')
	activityNode.set(theme, '@android:style/Theme.Translucent.NoTitleBar')
	activityNode.set(configChanges, 'keyboardHidden|orientation')
	activityNode.set(exported, 'true')
	activityNode.set(screenOrientation, 'portrait')

	tree.write(manifest, 'UTF-8')

	return 0	


def execute(channel, pluginInfo, decompileDir, packageName):
	generateShareSDKXmlFile(pluginInfo, decompileDir)
	appendAppIdForQZone(pluginInfo, decompileDir)
	generateWXEntryActivity(channel, pluginInfo, decompileDir, packageName)