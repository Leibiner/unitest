# -*- coding: utf-8 -*-

import json
import os
from datetime import datetime
import requests
from lxml import etree
from .logLib import logLib
from . import globalVariables
import traceback
import sys
import imp

# Set coding to utf-8
imp.reload(sys)
sys.setdefaultencoding('utf-8')


def readXmlLog(self, xmlName):
    if xmlName[1:2] != ":" and not xmlName.startswith("/"):
        xmlName = os.getcwd() + r"\%s" % (xmlName)
    print(xmlName)

    tree = etree.parse(xmlName)
    root = tree.getroot()
    return root

def loadDataCols(self, wb, sheetName):

    self.dataCols = {}
    sheetInfo = wb.get_sheet_by_name(sheetName)
    for i in range(65, 91):
        cellVal = sheetInfo.cell("%s%i" % (chr(i), 1)).value
        # if cellVal is None or com.toStr(cellVal).strip() == "":
        if cellVal is None or str(cellVal).strip() == "":
            break
        self.dataCols[cellVal] = chr(i)
    return self.dataCols

def getCellInfo(self, sheetInfo, colName, iRow):
    cellInfo = ''
    id = self.__getColId(colName, iRow)
    if sheetInfo is not None:
        cellInfo = sheetInfo.cell(id).value
    return cellInfo

def __getColId(self, colName, iRow):
    return "%s%i" % (self.dataCols[colName], iRow)

def _getDiffTime(self, endTime, startTime):
    return (datetime.strptime(endTime, '%Y%m%d %H:%M:%S.%f') -
            datetime.strptime(startTime, '%Y%m%d %H:%M:%S.%f')).total_seconds()

def getProjectIdAndName(self, projectKey):
    '''
    get projectId from testplatform_project table by projectName
    :param string projectName
    :return int rows[0]: projectId
    '''
    data = {'dbName': 'ArProject', 'fields': ['project_id', 'project_name'], 'filter': {'project_key': projectKey}}
    rows = self.sendGetInfoApiRequest(data)
    if rows is None:
        print("The query result is null since this project %s does not in DB" % (projectKey))
        return None, None
    else:
        return rows[0]['project_id'], rows[0]['project_name']

def getCaseDescription(self, caseName, moduleName=None):
    '''
    get case description from auto_casenamemeta by caseName
    :param string caseName
    :return string rows[0]
    '''
    data = {'dbName': 'ArCaseinfo',
            'fields': ['case_description'],
            'filter': {
                'case_name': caseName
            }}
    if moduleName is not None:
        data['filter']['case_module'] = moduleName
    rows = self.sendGetInfoApiRequest(data)
    if rows is None or rows == []:
        print("The query result is null since this case %s does not in DB" % (caseName))
        return None
    else:
        return rows[0]['case_description']

def insertCaseNameMeta(self, caseNameXml):
    xmlFile = os.path.join(os.getcwd(), "caseNameXml") % (caseNameXml)
    tree = etree.parse(xmlFile)
    root = tree.getroot()
    for child in root:
        name = child.get("name")
        value = child.get("value")
        data = {'dbName': 'ArCaseinfo',
                'data': [{'case_name': name, 'case_description': value}]}
        self.sendAddInfoApiRequest(data)


def insertCaseDescToDb(self, caseFilePath):
    print("insert CaseDesc to DB...")
    for caseFilePath1 in caseFilePath:
        print(caseFilePath1)
        if os.path.isdir(caseFilePath1):
            print("list directory...")
            for caseFile in self.getListFiles(caseFilePath1):
                self.getCaseDescFromFileThenInsertToDb(caseFile)
        else:
            self.getCaseDescFromFileThenInsertToDb(caseFilePath1)

def _insertCaseDescToDb(self, caseName, caseDesc, moduleName):
    rowCase = self.getCaseDescription(caseName, moduleName)
    print("insert or update caseName %s to DB ..." % (caseName))
    data = {'dbName': 'ArCaseinfo', 'condition': ['case_name', 'case_module'],
            'data': [{'case_description': caseDesc, 'case_name': caseName, 'case_module': moduleName,
                      'create_time': datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),
                      'update_time': datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')}]}
    self.sendAddInfoApiRequest(data)

def getCaseDescFromFileThenInsertToDb(self, caseFilePath):
    print("parse PY file %s..." % (caseFilePath))
    rowCount = 0

    fileName = os.path.basename(caseFilePath)

    if (fileName.startswith('test') and fileName.endswith('.py')):
        print("parse test case file %s..." % (caseFilePath))
        f = open(caseFilePath, 'r')
        lines = f.read().splitlines()
        casesList = []
        for row in lines:
            rowCount = rowCount + 1
            defText = row.lstrip()
            if (defText.startswith("def test")):
                # caseName = defText.strip("def ")[:-7]
                caseName = defText[4:defText.find('(')]
                # caseModule = caseFilePath.split("testcase\\")[1].replace("\\", ".").replace(".py", "").replace(
                #     "../", '')
                # caseModule = caseModule.split('.')[-1]
                caseModule = caseFilePath.replace('\\', '.').replace('/', '.').replace('.py', '')
                caseModule = caseModule[caseModule.find('XXX.'):]

                caseValue = (lines[rowCount - 2].lstrip()[1:]).lstrip()
                casesList.append({'case_name': caseName, 'case_description': caseValue, 'case_module': caseModule})
        data = {'dbName': 'ArCaseinfo',
                'condition': ['case_name', 'case_module'],
                'data': casesList}
        self.sendAddInfoApiRequest(data)
        f.close()

def getListFiles(path):
    '''
        get file list in path
        :return list
    '''

    ret = []
    for root, dirs, files in os.walk(path):
        for filespath in files:
            ret.append(os.path.join(root, filespath))
    return ret
