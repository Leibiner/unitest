# coding = UTF-8

import xml.etree.cElementTree as ET
from .logLib import logLib
import os
from testconfig import config

class xmlHelperLib(object):
    logger = logLib(__name__)

    testDataFile = ""  # xml file path of the test data
    testDataObj = None  # xml object to load the test data xml file

    # automationtestLogConf = 'conf/env/automationtest_log.conf' # The location of automation log configuration file


    def __findNodeElement(self, rootObj, nodePath, filePath):
        env = config['env']
        if env == 'prod' or env == 'yz' or env == 'pre':
            env = 'prod'
        element = rootObj.find(nodePath + "/" + env)
        if element is not None:
            return element
        elif filePath.upper().find("_QA") == -1 and filePath.upper().find("_PROD") == -1:
            element = rootObj.find(nodePath + "[@name='%s']" % env)
            if element is not None:
                return element
            else:
                return rootObj.find(nodePath)
        else:
            return rootObj.find(nodePath)

    def getNodeValueByNodePath(self, nodePath, filePath, diffEnv=True):
        #nodePath = self.__appendEnv(filePath, nodePath, diffEnv)
        self.logger.info("Get the env conf value by node path '%s' with file path '%s'" % (nodePath, filePath))

        if filePath[1:2] != ":":
            filePath = os.path.dirname(os.path.abspath(__file__)) + '/../%s' % filePath
        if self.testDataFile != filePath:
            self.testDataFile = filePath
            self.testDataObj = ET.parse(filePath)
        try:
            element = self.__findNodeElement(self.testDataObj.getroot(), nodePath, filePath)
        except:
            self.logger.warn("Cannot find the element by path %s" % nodePath)
            element = None
        val = None
        if element != None:
            val = element.text
        return val

    def updateNodeTextByNodePath(self, nodePath, filePath, value, diffEnv=True):
        #nodePath = self.__appendEnv(filePath, nodePath, diffEnv)
        self.logger.info("Get the env conf value by node path '%s' with file path '%s'" % (nodePath, filePath))

        if filePath[1:2] != ":":
            filePath = os.path.dirname(os.path.abspath(__file__)) + '/../%s' % filePath
        if self.testDataFile != filePath:
            self.testDataFile = filePath
            self.testDataObj = ET.parse(filePath)
        try:
            element = self.__findNodeElement(self.testDataObj.getroot(), nodePath, filePath)
        except:
            self.logger.warn("Cannot find the element by path %s" % nodePath)
            element = None

        element.text = str(value)
        self.testDataObj.write(filePath, "utf-8")

    def updateNodeAttributeByNodePath(self, nodePath, filePath, attrib, value, diffEnv=True):
        #nodePath = self.__appendEnv(filePath, nodePath, diffEnv)
        self.logger.info("Get the env conf value by node path '%s' with file path '%s'" % (nodePath, filePath))

        if filePath[1:2] != ":":
            filePath = os.path.dirname(os.path.abspath(__file__)) + '/../%s' % filePath
        if self.testDataFile != filePath:
            self.testDataFile = filePath
            self.testDataObj = ET.parse(filePath)
        try:
            element = self.__findNodeElement(self.testDataObj.getroot(), nodePath, filePath)
        except:
            self.logger.warn("Cannot find the element by path %s" % nodePath)
            element = None

        element.attrib[attrib] = str(value)
        self.testDataObj.write(filePath, "utf-8")

    def loadAllConfValuesToDict(self, nodePath, filePath):
        self.logger.info("get the env conf value by node path '%s' with file path '%s'" % (nodePath, filePath))

        if self.testDataFile != filePath:
            self.testDataFile = filePath
            self.testDataObj = ET.parse(filePath)
        try:
            root = self.testDataObj.getroot()
        except:
            root = None
        config = {}
        if root != None:
            for item in root.iter():
                if len(item.findall('*')) == 0:
                    if item.text is not None:
                        config[item.tag] = item.text
        return config

    def __appendEnv(self, filePath, nodePath, diffEnv=True):

        if diffEnv and filePath.upper().find("_QA") == -1 and filePath.upper().find("_PROD") == -1:
            env = config['env']
            if env == 'prod' or env == 'yz' or env == 'pre':
                env = 'prod'

            return nodePath + "[@name='%s']" % env
        return nodePath


xmlHelper = xmlHelperLib()
