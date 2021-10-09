# -*- coding: utf-8 -*-


import base64
import binascii
import hashlib
import inspect
import json
import os
import platform
import random
import re
import socket
import string
import time
import urllib.parse
import uuid
from datetime import datetime, timedelta
import pyDes
import copy
import yaml
from nose.tools import eq_
from .logLib import logLib
from common.envEnum import envEnum
from Crypto.Cipher import AES


logger = logLib(__name__)


# region Data conversion and search methods
BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS).encode()
unpad = lambda s: s[:-ord(s[len(s)-1:])]
key=b'talk&learningbee'
#AES加密方法中需要用到

def loadJsonData(source, bAssert=True):
    '''
        convert string to json, default assert it
        :param string source
        :param boolean bAssert
        :return json data
    '''
    resp = None
    try:
        resp = json.loads(source)
    except:
        msg = "not found JSON object, return data %s is not correct" % (source)
        logger.error(msg)
        if bAssert:
            assert False, msg
    return resp


def md5String(source):
    '''
        encrypt string by md5
        :param string source
        :return string targ
    '''
    logger.info(source)
    if not isinstance(source, str):
        source = repr(source)
    target = hashlib.md5()
    target.update(source)
    targ = target.hexdigest()
    logger.info(targ)

    return targ

#非机密数据的正式数据加密标准（DES Data Encryption Standard)
def desString(key, source):
    '''
        encrypt string by des
        :param string key
        :param string source
        :return target
    '''
    try:
        logger.info('[DES] try to get DES from key: %s and source: %s' % (key, source))
        k = pyDes.des(key, pyDes.CBC, key, pad=None, padmode=pyDes.PAD_PKCS5)
        target = k.encrypt(source)
        target = binascii.hexlify(target)
        logger.info('[DES] get DES encode string: %s' % (target))
    except Exception as e:
        logger.error('%s: %s' % (e, e.message))
        assert False, '[DES] get DES encode failed: %s' % (e.message)
    return target



def sha1String(source):
    '''
        encrypt string by sha1
        :param string source
        :return target
    '''
    if not isinstance(source, str):
        source = repr(source)
    target = hashlib.sha1(source).hexdigest()
    return target

def iv():
    """
    The initialization vector to use for encryption or decryption.
    It is ignored for MODE_ECB and MODE_CTR.
    """
    iv = chr(0) * 16
    return iv.encode()

#AES加密方法
def encrypt(message):
    """
    It is assumed that you use Python 3.0+
    , so plaintext's type must be str type(== unicode).
    """
    message = message.encode()
    raw = pad(message)
    cipher = AES.new(key, AES.MODE_CBC, iv())
    enc = cipher.encrypt(raw)
    return base64.b64encode(enc).decode('utf-8')

#AES解密方法
def decrypt(enc):
    enc = base64.b64decode(enc)
    cipher = AES.new(key, AES.MODE_CBC, iv())
    dec = cipher.decrypt(enc)
    return unpad(dec).decode('utf-8')

def sumDictKeyValue(dict_list, *args):
    """
    多个字典组成的列表，取1个或多个key的value之和返回
    :param dict_list:例如：[{"key1":5.1, "key2": 2}, {"key1":1.2, "key2": 2}]
    :param args: 例如： key1, key2
    :return: 各key对应累加值的dict
    """
    sum_dict = {}
    len_dict = len(args)
    if not len_dict:
        return None
    for i in range(len_dict):
        locals()['sum' + str(i)] = 0
    for dic in dict_list:
        for i in range(len_dict):
            locals()['sum' + str(i)] += dic[args[i]]
    for i in range(len_dict):
        sum_dict[args[i]] = locals()['sum' + str(i)]
    return sum_dict

def toStr(strItem):
    '''
        convert object to str if can, else return raw data
        :param object strItem
        :return string
    '''
    try:
        return str(strItem)
    except:
        return strItem


def toInt(item):
    '''
        convert object to int if can, else return raw data
        :param object item
        :return int
    '''
    try:
        return int(item)
    except:
        return item


def encodeToBase64(path):
    '''
        encode file to base64
        :return None
    '''
    sourceFile = open(path, 'rb')
    bytesTarget = base64.b64encode(sourceFile.read())
    sourceFile.close()
    return str(bytesTarget)


def convertStringToList(source, separator):
    '''
        convert string to list according to specified separator
        :param string source
        :param string separator
        :return list targetList
    '''
    targetList = []
    tarList = source.split(separator)

    for target in tarList:
        # delete blank space
        target = target.strip(" ")
        targetList.append(target.encode("utf-8"))

    logger.debug(targetList)
    return targetList

def now_to_timestamp(digits = 10):
    """
    获取当前时间戳
    :param digits:位数
    :return: 时间戳例如：1356789000
    """
    time_stamp = time.time()
    digits = 10 ** (digits -10)
    time_stamp = int(round(time_stamp*digits))
    return time_stamp

def convert_timestamp_to_fmt_time(timeStamp, fmt="%Y-%m-%d %H:%M:%S"):
     """
     将时间戳转换为字符格式
     :param timeStamp: 10位或者13位时间戳
     :param fmt: 默认格式
     :return: "%Y-%m-%d %H:%M:%S"
     """
     timeStamp=str(timeStamp)[:-3]
     timeArray = time.localtime(int(timeStamp))
     fmtTime = time.strftime(fmt, timeArray)
     return fmtTime

def convertStrTimeToUnixTime(strTime, digit=10):
    '''
        convert timeString to 10 or 13 bytes unixTime
        :param string strTime: like "2015-02-09T09:03:19.123" or "2015-02-09 09:03:19.1" or "2015-02-09 09:03:19"
        :return float unixTime
    '''
    logger.info("convert time from string to unixTime...")
    if len(strTime) > 20:
        strTime = strTime[0:19]
    if digit == 10:
        if "T" in strTime:
            unixTime = time.mktime(time.strptime(strTime, '%Y-%m-%dT%H:%M:%S'))
        else:
            unixTime = time.mktime(time.strptime(strTime, '%Y-%m-%d %H:%M:%S'))
        return int(unixTime)
    elif digit == 13:
        if "T" in strTime:
            unixTime = time.mktime(time.strptime(strTime, '%Y-%m-%dT%H:%M:%S'))*1000
        else:
            unixTime = time.mktime(time.strptime(strTime, '%Y-%m-%d %H:%M:%S'))*1000
        return int(unixTime)
    else:
        logger.error("digit could only be 10 or 13")


def convertStrTimeToDateTime(strTime, formatD='%Y-%m-%dT%H:%M:%S'):
    '''
        convert date string to datetime.
        :param strTime: string, date time string
        :param formatD: string, date time format
    '''
    try:
        date = datetime.strptime(strTime, formatD)
        return date
    except:
        assert False, "strTime: %s, format: %s" % (strTime, formatD)

#获取时间点的间隔
def CalDatetime(date1,date2):
    datetimeStamp1=int(time.mktime(time.strptime(date1, "%Y-%m-%d %H:%M:%S")))#
    #int(time.mktime(time.strptime(str(datetime.date.today() + datetime.timedelta(days=-10)) + ' 06:30:00.000','%Y-%m-%d %H:%M:%S.%f')) * 1000)
    datetimeStamp2 = int(time.mktime(time.strptime(date2, "%Y-%m-%d %H:%M:%S")))
    #返回两个时间戳的差值，因为时间戳是秒级，所以结果是（秒）单位
    n=(datetimeStamp1 - datetimeStamp2)
    return n

def convertListToStrWithComma(srcList):
    '''
        convert list to string with split by comma
        :param list srcList
        :return string srcStr
    '''
    logger.info("convert list to string with split by comma...")
    srcStr = ""

    for item in srcList:
        srcStr = srcStr + str(item) + ','

    listStr = srcStr[0:-1]
    return listStr


def base64DecodeAndEncode(data, baseType="encode"):
    '''
        encrypt and decrypted by base64
        :param string data
        :param boolean baseType
        :return string
    '''

    data1 = data.encode(encoding="utf-8")
    if baseType == "encode":
        # base64加
        return base64.b64encode(data1)
    else:
        # base64解
        return base64.b64decode(data1)


def searchResultfromString(rule, sourceString):
    '''
        find special string from source string according to special rule
        :param string rule
        :param string sourceString
        :return list rsList
    '''
    try:
        regex = re.compile(rule)
        rsList = regex.findall(sourceString)
    except:
        assert False, "find string failed"

    return rsList


def stripInvalidForResponse(respDict):
    for key, value in list(respDict.items()):
        valueNew = _stripNull(value)
        if 'ip_' in key and "." not in str(valueNew):
            respDict = _convertIp(respDict)
        respDict[key] = valueNew
    return respDict


def _convertIp(respDict):
    ipHex = hex(getValue(respDict, 'ip_'))
    tmpList1 = re.findall(r'(.{2})', str(ipHex).replace('0x', ''))
    tmpList2 = tmpList1[-1::-1]
    ipNew = ".".join([str(int(o, 16)) for o in tmpList2])
    respDict.update({'ip_': ipNew})
    return respDict


def _stripNull(value):
    if isinstance(value, str) and "\x00" in value:
        value = value.replace('\x00', '')
    return value


# endregion

# region Assert and check methods



def checkSameValueInDicts(dicts_list, dict_key, dict_value, b_match=True):
    """
    检查某个返回的字典串都包含某同一个key和value
    :param dicts_list: dict组成的序列
    :param dict_key: 校验的key
    :param dict_value: 校验的value
    :param b_match: 是否正则匹配
    :return:
    """
    if isinstance(dicts_list[0], dict):
        if  not b_match:
            filter_resp = filter(lambda x:x[dict_key]==dict_value, dicts_list)
        else:
            filter_resp = filter(lambda x: re.match(dict_value, x[dict_key]), dicts_list)
        checkEqual(len(dicts_list), len(list(filter_resp)))


def checkKeysInDict(keys, actualDict):
    '''
        check key is not in dict
        :param object keys
        :param dict actualDict
    '''
    notFoundKeys = [k for k in keys if k not in actualDict]
    assert len(notFoundKeys) == 0, "the keys: {0} not found: {1}".format(str(notFoundKeys), str(list(actualDict.keys())))


def checkResultEqual(actual, expected, msg=None):
    '''
        check actual result does match expected or not
        :param string/list actual
        :param string/list expected
        :param string msg
    '''

    if msg is None:
        msg = "the actual result is %s but the expected is %s" % (actual, expected)

    eq_(actual, expected, msg)


def checkEqual(actualVal, expectedVal, errMsg=None, onlyLogError=False):
    '''
        check actual result does match expected or not
        :param string/list actualVal
        :param string/list expectedVal
        :param string errMsg
        :param boolean onlyLogError
    '''
    logger.info("Check the value '%s' with '%s'" % (toStr(actualVal), toStr(expectedVal)))

    if errMsg is None:
        errMsg = "Expected <font color='red'>'%s'</font> is not as actual " \
                 "<font color='red'>'%s'</font>" % (toStr(expectedVal), toStr(actualVal))

    if actualVal != expectedVal:
        logger.error(errMsg)
        if onlyLogError:
            return False
        else:
            raise AssertionError(errMsg)
    return True

def checkNotEqual(actualVal, expectedVal, errMsg=None, onlyLogError=False):
    '''
        check actual result does not equal the expected
        :param string/list actualVal
        :param string/list expectedVal
        :param string errMsg
        :param boolean onlyLogError
    '''
    logger.info("Check the value '%s' with '%s'" % (toStr(actualVal), toStr(expectedVal)))

    if errMsg is None:
        errMsg = "Expected <font color='red'>'%s'</font> is as actual " \
                 "<font color='red'>'%s'</font>" % (toStr(expectedVal), toStr(actualVal))

    if actualVal == expectedVal:
        logger.error(errMsg)
        if onlyLogError:
            return False
        else:
            raise AssertionError(errMsg)
    return True

def checkGreaterEqual(actualVal, expectedVal, errMsg=None, onlyLogError=False):
    '''
        check actual result does match expected or not
        :param string/list actualVal
        :param string/list expectedVal
        :param string errMsg
        :param boolean onlyLogError
    '''
    logger.info("Check the value '%s' with '%s'" % (toStr(actualVal), toStr(expectedVal)))

    if errMsg is None:
        errMsg = "Expected <font color='red'>'%s'</font> is not greater equal actual " \
                 "<font color='red'>'%s'</font>" % (toStr(expectedVal), toStr(actualVal))

    if actualVal < expectedVal:
        logger.error(errMsg)
        if onlyLogError:
            return False
        else:
            raise AssertionError(errMsg)
    return True

def checkLessEqual(actualVal, expectedVal, errMsg=None, onlyLogError=False):
    '''
        check actual result does match expected or not
        :param string/list actualVal
        :param string/list expectedVal
        :param string errMsg
        :param boolean onlyLogError
    '''
    logger.info("Check the value '%s' with '%s'" % (toStr(actualVal), toStr(expectedVal)))

    if errMsg is None:
        errMsg = "Expected <font color='red'>'%s'</font> is not less equal actual " \
                 "<font color='red'>'%s'</font>" % (toStr(expectedVal), toStr(actualVal))

    if actualVal > expectedVal:
        logger.error(errMsg)
        if onlyLogError:
            return False
        else:
            raise AssertionError(errMsg)
    return True

def checkItemInList(list, item, errMsg=None, onlyLogError=False):
    '''
        check item does in list or not
        :param list list
        :param object item
        :param string errMsg
        :param boolean onlyLogError
    '''
    logger.info("Check the item '%s' is in list '%s'" % (toStr(item), toStr(list)))

    if errMsg is None:
        errMsg = "Item <font color='red'>'%s'</font> is not in " \
                 "<font color='red'>'%s'</font>" % (toStr(item), toStr(list))

    if item not in list:
        logger.error(errMsg)
        if onlyLogError:
            return False
        else:
            raise AssertionError(errMsg)
    return True


def checkMatch(strItem, pattern, bCheck=True):
    '''
        check strItem is match pattern or not
        :param string strItem
        :param string pattern
        :param boolean bCheck
        :return boolean
    '''

    if strItem == pattern:
        return True

    strPattern = re.sub(r'\s', '', toStr(pattern))
    strItem = re.sub(r'\s', '', toStr(strItem))
    if not re.match(strPattern, strItem):
        if bCheck:
            errMsg = "Pattern <font color='red'>'%s'</font> is not match as <font color='red'>'%s'</font>" % \
                     (strPattern, strItem)
            assert False, errMsg
        return False
    return True


def checkListEqual(actList, expList):
    '''
        check actual list does match expected list or not
        :param list actual
        :param list expected
    '''
    logger.info("check actual list length is equal to expected...")
    lenAct = len(actList)
    lenExp = len(expList)
    checkResultEqual(lenAct, lenExp)
    # if resExp is not null, it means to actual list is equal to expected
    resExp = set(expList) - set(actList)
    # if resAct is not null, it means to expected list is not in actual list
    resAct = set(actList) - set(expList)
    checkResultEqual(resAct, resExp)


def checkTwoDicts(bodyData, expected_data):
    '''
        check two dict is equal or not
        :param dict bodyData
        :param dict expected_data
    '''
    logger.info("Check the dict %s is as expected as dict %s" % (json.dumps(bodyData, ensure_ascii=False),
                                                                 json.dumps(expected_data, ensure_ascii=False),))

    msg = "<font color='red'>the json message should be %s , but the actual is: %s</font>" \
          % (json.dumps(expected_data, ensure_ascii=False), json.dumps(bodyData, ensure_ascii=False))
    if not bodyData == expected_data:
        logger.assertErr(False, msg)


def checkValueInDict(dict, name, expected, msg=None):
    '''
        check value in dict by key is equal to expected or not
        :param dict dict
        :param string name
        :param object exepected
        :param string msg
    '''

    logger.info("Check the '%s' value in source %s as '%s'" % (name, toStr(dict), toStr(expected)))

    resAct = getValue(dict, name)
    messageStr = " message: %s" % (dict.get("message")) if dict.get("message", "") != "" else ""
    msg = "the actual result is %s but the expected is %s." % (resAct, expected) if msg is None else msg
    msg = "<font color='red'>%s%s</font>" % (msg, messageStr)

    checkEqual(resAct, expected, msg)


# check the length of comments list data when pageT



def _checkDataLengthWithStartLimit(start, limit, lenAct, totalCount, limitD, initialIndex):
    '''
        check the length of comments list data when pageT
        :param int start
        :param int limit
        :param int lenAct
        :param int totalCount
        :param int limitD
        :param int initialIndex
    '''
    logger.info("check the data length of response by index mode")
    if limit == None or limit == "":
        limit = limitD  # default limit value is 10
    if limit <= 0:
        limit = 0
    logger.info("Total count:%s, Limit count:%s, Actual count:%s, Start:%s" \
                % (totalCount, limit, lenAct, start))
    if start > totalCount:
        msg = "start大于totalCount,期望返回数目:0条，实际返回的数目为%d" % (lenAct)
        assert lenAct == 0, msg
    else:
        lenExp = min(limit, totalCount - start + initialIndex)
        msg = "期望返回数目:%s，实际返回的数目为%s" % (lenExp, lenAct)
        assert lenAct == lenExp, msg


# check the length of comments list data when page



def _checkDataLengthWithPageType(start, limit, lenAct, totalCount, limitD, limitMax):
    '''
        check the length of comments list data when page
        :param int start
        :param int limit
        :param int lenAct
        :param int totalCount
        :param int limitD
        :param int initialIndex
    '''
    logger.info("check the data length of response when page type")
    if limit is None or limit == "":
        limit = limitD  # default limit value is 1
    elif limit < 0:
        limit = 0

    start = 1 if start is None or start == "" or start < 0 else start
    limit = min(limit, limitMax) if isinstance(limitMax, int) else limit
    logger.info("TotalCount:%s, Start:%s, Limit:%s, Actual Data count:%s" % (totalCount, start, limit, lenAct))

    if limit > 0 and start <= totalCount / limit:
        assert lenAct == limit, "期望返回数据长度为%s,实际返回数据长度%s" % (limit, lenAct)
    elif limit > 0 and start == totalCount / limit + 1:
        assert lenAct == totalCount % limit, "期望返回数据长度为%s,实际返回数据长度%s" % (totalCount % limit, lenAct)
    else:
        assert lenAct == 0, "期望返回数据长度为0,实际返回数据长度%s" % (lenAct)


def checkDataLength(start, limit, lenAct, totalCount, pageType=0, limitD=30, startD=1, initialIndex=1,
                    limitMax=None):
    '''
        check the order of data list...
        :param int start
        :param int limit
        :param int lenAct
        :param int totalCount
        :param int pageType:0 -- indexMode;1 -- pageMode
        :param int limitD: default value of limit
        :param int startD: default value of start(normal is 1)
        :param int initialIndex: first index of data
        :param int limitMax: max limit
    '''

    logger.info(
        "[checkDataLength] start:%s, limit:%s, lenAct:%s, totalCount:%s, pageType:%s, limitD:%s, startD:%s, initIndex:%s, limitMax:%s" \
        % (start, limit, lenAct, totalCount, pageType, limitD, startD, initialIndex, limitMax))
    start = startD if start is None or start < 0 else start
    limit = limitD if isinstance(limit, int) is False or limit < 0 else limit

    if totalCount < start:
        logger.info("Total:%s, Limit:%s, Actual:%s, Start:%s" % (totalCount, limit, lenAct, start))
        assert lenAct == 0, "The data should be null when start %s larger than totalCount %s,Actual dataLength :%s" % (
            start, totalCount, lenAct)
    elif pageType == 0 or (
                isinstance(pageType, str) and (pageType.lower() == "index" or pageType == "" or pageType == None)):
        logger.info("The data is show by index mode")
        _checkDataLengthWithStartLimit(start, limit, lenAct, totalCount, limitD, initialIndex)
    else:
        logger.info("The data is show by page mode")
        _checkDataLengthWithPageType(start, limit, lenAct, totalCount, limitD, limitMax)


def checkDataOrder(dataAct, order, orderKey):
    '''
        check the order of data list...
        :param list dataAct
        :param int order: 1-increase;0-decrease
        :param string orderKey
    '''
    logger.info("check the order of response data.")
    if not isinstance(dataAct, list):
        assert False, "Expect input dataAct is list,Actual is %s" % (dataAct)
    keyValueList = []
    logger.info("the data is ordered by %s" % (orderKey))
    for data in dataAct:
        keyValue = getValue(data, orderKey)
        # 以时间作为排序依据时,需要转换时间格式
        if "date" in orderKey.lower():
            t0 = str(convertStrTimeToUnixTime(keyValue)).replace(".0", ".")
            tmp = re.split("\.|\+", keyValue)
            if len(tmp) <= 1:
                ms = "0"
            else:
                ms = tmp[1]
            # 当毫秒级为0时
            if ":" in ms:
                ms = "0"
            # 当毫秒级为0时
            result = eval(t0 + ms)
        else:
            result = keyValue
        keyValueList.append(result)
    indexL = [i for i in range(len(keyValueList))]
    combDataList0 = list(zip(indexL, keyValueList))
    if order == 1:
        combDataList1 = sorted(list(dict(combDataList0).items()), key=lambda d: d[1], reverse=False)
        msg = "Expect response data sorted in ascending order,Actual response:%s" % (combDataList0)
    else:
        combDataList1 = sorted(list(dict(combDataList0).items()), key=lambda d: d[1], reverse=True)
        msg = "Expect response data sorted in descending order,Actual response:%s" % (combDataList0)
    assert combDataList0 == combDataList1, msg

def checkListOrder(data_list, order=1, key=None):
    """
    校验列表排序状态
    :param data_list: 列表
    :param order: 1:ASC,0:DESC
    :param key: 排序key值，默认为None
    :return:
    """
    reverse = False if order else True
    l1 = sorted(data_list, reverse=reverse, key=key)
    checkEqual(data_list, l1)

def checkDictionary(expectedDict, actualDict, root=None, bCheck=True):
    '''
        assert expectedDic with actualDic according to expectedDict's keys.
        :param expectedDict: dict
        :param actualDict: dict
        :param root: string message
    '''
    logger.info("Check the dict %s is in dict %s" % (json.dumps(expectedDict, ensure_ascii=False),
                                                     json.dumps(actualDict, ensure_ascii=False),))
    bResult = True
    if root == None:
        logger.info(" check the dictionary value according to expected dictionary's keys:")

    for item in list(expectedDict.items()):
        expected = item[1]
        actual = getValue(actualDict, item[0])
        if isinstance(expected, dict) and isinstance(actual, dict):
            if root != None:
                root += ("=>%s" % (item[0]))
            else:
                root = item[0]
            bResult = trackResult(bResult, checkDictionary(expected, actual, root, False))
        elif isinstance(expected, list):
            for i in range(len(expected)):
                bResult = trackResult(bResult, checkDictionary(expected[i], actual[i], root, False))
        elif isinstance(expected, float) and isinstance(actual, float):
            logger.info(" check %s=>%s(float): actual=%s, expected=%s" % (root, item[0], actual, expected))
            actualValue = "{0:4.4f}".format(actual)
            expectedValue = "{0:4.4f}".format(expected)
            if actualValue != expectedValue:
                logger.error("check %s=>%s: the actual is %s, but expected is %s" % (
                    root, item[0], actualValue, expectedValue))
                bResult = False
        else:
            logger.info(" check %s=>%s: actual=%s, expected=%s" % (root, item[0], actual, expected))
            if actual != expected:
                logger.error("the actual %s value is %s, but expected is %s" % (item[0], actual, expected))
                bResult = False
    if bCheck:
        assert bResult, "Check the dict %s is not in dict %s" % (json.dumps(expectedDict, ensure_ascii=False),
                                                                 json.dumps(actualDict, ensure_ascii=False),)
    return bResult


def trackResult(result, newResult):
    if result:
        result = newResult
    return result

def trackNewResult(result, newResult):
    return newResult if newResult is not None else result

def checkPartInDict(expectedDict, actualDict, bMatch=False, bCheck=True, check_all=False):
    '''
        check expected dict is in actual dict or not, if bMatch call checkMatch method, if bCheck use assert
        :param dict expectedDict
        :param dict actualDict
        :param boolean check_all  actualDict里如果遇到dict组成的list，True为检查所有dict，False只检查第一条
        :param boolean bMatch
        :param boolean bCheck
        :param boolean check_all
    '''

    # logger.info("Check the dict %s is in dict %s" % (json.dumps(expectedDict, ensure_ascii=False),
    #                                                  json.dumps(actualDict, ensure_ascii=False),))
    bResult = True
    for item in list(expectedDict.items()):
        expected = item[1]
        actual = getValue(actualDict, item[0])
        if isinstance(expected, dict) and isinstance(actual, dict):
            bResult = trackResult(bResult, checkPartInDict(expected, actual, bMatch, False, check_all))
        elif isinstance(expected, list) and expected:  # 201
            for i in range(len(expected)):
                if isinstance(expected[i], dict):
                    if check_all:
                        for item1 in actual:
                            bResult = trackNewResult(bResult, checkPartInDict(expected[i], item1, bMatch, False))
                            if bResult:
                                actual.remove(item1)
                                break
                        if not bResult:
                            break
                    else:
                        bResult = trackResult(bResult, checkPartInDict(expected[i], actual[i], bMatch, False))
                else:
                    bResult = trackResult(bResult, checkEqual(actual[i], expected[i], False))
        elif isinstance(expected, float) and isinstance(actual, float):
            actualValue = "{0:4.4f}".format(actual)
            expectedValue = "{0:4.4f}".format(expected)
            if actualValue != expectedValue:
                logger.info(" check %s(float)" % item[0])
                logger.error("check %s: the actual is %s, but expected is %s" % (
                    item[0], actualValue, expectedValue))
                bResult = False
        else:
            if bMatch:
                result = checkMatch(actual, expected, False)
                if result == False:
                    logger.info(" check %s"  % item[0])
                    logger.error("Pattern '%s' is not match '%s'" % (expected, actual))
                bResult = trackResult(bResult, result)
            elif actual != expected:
                logger.info(" check %s" % item[0])
                logger.error("the actual %s value is %s, but expected is %s" % (item[0], actual, expected))
                bResult = False
    if bCheck:
        assert bResult, "Check the dict %s is not in dict %s" % (json.dumps(expectedDict, ensure_ascii=False),
                                                                 json.dumps(actualDict, ensure_ascii=False),)
    return bResult


def checkListHasDuplicateItem(srcList):
    '''
        check list has duplicateItem, if has duplicate,it will fail
        :param list srcList
    '''

    logger.info("check source list has duplicate item or not...")
    dupList = []
    for item in srcList:
        countItem = srcList.count(item)
        if countItem > 1:
            dupList.append(item)
    logger.info(len(dupList))
    logger.info(dupList)
    assert dupList == [], "The actual eventIdList has duplicated %s item list %s" % (len(dupList), dupList)


# endregion

# region Time methods



def currentTime(fmt='%Y%m%d%H%M'):
    '''
        get current time by the specified format
        :param string fmt
        return datetime
    '''
    currentTime = time.strftime(fmt, time.localtime(time.time()))
    return currentTime


def currentDateTime(fmt='%Y-%m-%d %H:%M:%S.%f'):
    '''
        get current date time by the specified format
        :param string fmt
        return datetime
    '''

    return datetime.strftime(datetime.now(), fmt)


def getUUidByTimeStamp():
    '''
        get uuid by time stamp
        :return string uuidResult
    '''

    uuidResult = str(uuid.uuid1())
    return uuidResult


def getNewDiffTimeForCurrent(diffType, diff, flag='plus', currentTime=None, dateFormat=None):
    '''
        get the new time that current time + or - [%diffType%]=diff
        :param string diffType: like days, hours...
        :param int diff: like 1,10
        :param string flag: "plus" or "sub"
        :param string currentTime
        :param string dateFormat
        :return datetime newTime or string newTimeToString
    '''
    logger.info("get the new time according to date format...")
    if dateFormat == None or dateFormat == "":
        dateFormat = '%Y-%m-%d %H:%M:%S'

    if currentTime == None:
        currentTime = datetime.now()
    else:
        currentTime = datetime.strptime(currentTime, dateFormat)

    if flag.lower() == "plus":
        if diffType == "days":
            newTime = currentTime + timedelta(days=diff)
        if diffType == "hours":
            newTime = currentTime + timedelta(hours=diff)
        if diffType == "minutes":
            newTime = currentTime + timedelta(minutes=diff)
        if diffType == "seconds":
            newTime = currentTime + timedelta(seconds=diff)
    else:
        if diffType == "days":
            newTime = currentTime - timedelta(days=diff)
        if diffType == "hours":
            newTime = currentTime - timedelta(hours=diff)
        if diffType == "minutes":
            newTime = currentTime - timedelta(minutes=diff)
        if diffType == "seconds":
            newTime = currentTime - timedelta(seconds=diff)
    if currentTime == None:
        logger.debug(newTime)
        return newTime
    else:
        logger.debug(newTime)
        newTimeToString = datetime.strftime(newTime, dateFormat)
        return newTimeToString


def isValueDate(strDate, formatD='%Y-%m-%dT%H:%M:%S'):
    '''
        check is the string date is match the format when convert it to datetime
        :param string strDate
        :param string formatD
        :return boolean
    '''

    if formatD == None:
        formatD = '%Y-%m-%dT%H:%M:%S'
    try:
        time.strptime(strDate, formatD)
        return True
    except:
        return False


def isLeapYear(year):
    '''
        check the year is leap year or not
        :param int year
        :return boolean
    '''
    year = int(year)
    if (year % 4) == 0:
        if (year % 100) == 0:
            if (year % 400) == 0:
                return True
            else:
                return False
        else:
            return False
    else:
        return False


# endregion

# region Get value methods


def getAppKey(source, start=3, end=-6):
    '''
        get App Key
        :param string source
        :return string target
    '''

    target = base64.b64decode(source[start:end] + "=")
    return target


def checkResultIsNotNone(actValue, msg=None):
    '''
        check the value is not None
        :param object actValue
        :param string msg
    '''
    logger.info("check result is not None...")
    if actValue == None or actValue == "" or actValue == [] or actValue == {}:
        if msg == None:
            msg = "The actValue should be not null"
        assert False, msg


def getValue(source, name, msg=None):
    '''
        get dict key-value
        :param dict source
        :param string name: dict key
        :return string/int/boolean value: dict value
    '''
    try:
        valueMsg = "Not found (%s) in source %s" % (name, source)
        value = source.get(name, valueMsg)
        if value == valueMsg:
            logger.error(valueMsg)
            assert False, valueMsg
    except:
        if msg == None:
            msg = "cannot found name %s in source %s" % (name, source)
        logger.error(msg)
        assert False, msg

    return value


def getValueInDict(dict, name, msg=None):
    logger.info("Get the value '%s' in dict %s" % (name, str(dict)))

    for item in name.split('.'):
        try:
            dict = dict[toInt(item)]
        except:
            if msg is None:
                msg = "Cannot find the key '%s' in dict %s" % (item, str(dict))
            logger.assertErr(False, msg)
    return dict


def get_value_from_env_data_dict(data_dict, env_map_dict=None, use_default_mapping=False):
    '''
        :param dict data_dict: envEnum.qa: 159892, envEnum.online: 159893
        :param dict env_map_dict: env mapping, .i.e {"qa": "online"}
    '''
    cur_env = envEnum.curEnv
    if env_map_dict and cur_env in env_map_dict:
        cur_env = env_map_dict[cur_env]
    elif use_default_mapping:
        cur_env = {
            envEnum.qa: envEnum.qa,
            envEnum.qa1: envEnum.qa,
            envEnum.dev: envEnum.dev,
            envEnum.online: envEnum.online
        }[cur_env]
    return getValue(data_dict, cur_env)

# 区分环境装饰器
def env(func=None, use_default_mapping=False):
    def env_desc(func):
        def wrapper(self):
            return get_value_from_env_data_dict(func(self), use_default_mapping=use_default_mapping)
        return wrapper
    if func is None:
        return env_desc
    else:
        return env_desc(func)

def getUserName():
    '''
        Combine a userName for register
        :return string userName
    '''

    letters = "abcdefghijklmnopqrstuvwxyz"
    head = getRandomElem(letters)
    middle = str(time.time())
    letters = letters + "_"
    tail = getRandomElem(letters)
    userName = head + middle[1:10] + tail
    return userName


def getRandomContentByLength(length):
    '''
        get random length of content
        :param int length
        :return string
    '''

    letters = string.ascii_letters + string.digits + " ._!@#$%^&*()_+=?/<>,中国沪江上海北京浦软大厦张江"
    content = ""
    i = 0
    while i < length:
        content += random.choice(letters)
        i += 1

    return content


def getRandomElem(source):
    '''
        random one element from source
        :param string/list source
        :return string elem
    '''

    elem = random.choice(source)

    return elem


def randNumber(start, end):
    '''
        get random number between start and end
        :param int start
        :param int end
        :return int
    '''
    randNumber = str(random.randint(start, end))
    return randNumber


'''
    generate random string from letters and digit
    :param int length
'''


def getRandomString(length, prefix='', type=None):
    '''
    generate random string from letters and digit
    :param int length
    '''
    prefix = str(prefix)
    if length <= len(prefix): return prefix
    length = length - len(prefix)

    if str(type).lower() == 's':
        asciiString = string.ascii_letters
    elif str(type).lower() == 'd':
        asciiString = string.digits
    else:
        asciiString = string.ascii_letters + string.digits

    asciiLen = len(asciiString)
    randomString = ''

    if length <= asciiLen:
        randomString = randomString.join(random.sample(asciiString, length))
    else:
        count = length / asciiLen
        remainder = length % asciiLen

        randomString = randomString.join(random.sample(asciiString, remainder))
        while count > 0:
            randomString = randomString + ''.join(random.sample(asciiString, asciiLen))
            count = count - 1

    return prefix + randomString


def getIntersectionOfCoupleList(list01, list02):
    '''
        get intersection of couple list
        :param list list01
        :param list list02
    '''
    mixList = [item for item in list02 if item in list01]
    return mixList


def getMd5ForFile(absPath):
    '''
        get md5 for file
        :param string absPath
        :return string
    '''

    if os.path.exists(absPath):
        fObj = open(absPath, 'rb')
        m = hashlib.md5()
        m.update(fObj.read())
        fileMd5 = m.hexdigest()
        logger.info("MD5 for File: {}".format(fileMd5))
        print("~~~file md5~~~")
        print(fileMd5)
        fObj.close()
        return fileMd5
    else:
        assert False, "The file is not exist"


def genAbsPath(*args):
    '''
        generate abs path
        :param args:
        :return:
    '''

    if len(args) == 0:
        assert False, "Haven't give relative path"
    relPath = ''
    for item in args:
        if item.startswith('\\') or item.startswith('/'):
            item = item.replace('\\', '/', )
            item = item.replace('/', '', 1)
        relPath = os.path.join(relPath, item)
    absPath = os.path.join(os.getcwd(), relPath)
    absPath = absPath.replace('\\', '/')
    return absPath


def getTimestamp():
    '''
        get timestamp.
        :return string timestamp
    '''

    base = datetime.datetime(1, 1, 1)
    now = datetime.datetime.utcnow()
    result = "{0:.0f}".format((now - base).total_seconds() * 1e7)
    return result


def getLocalIpAddress():
    '''
        get local ip address
        :return string
    '''

    name = socket.getfqdn(socket.gethostname())
    return socket.gethostbyname(name)


def getMacAddress():
    '''
        get random mac address
        :return string
    '''
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e + 2] for e in range(0, 11, 2)])


def getResultMultiLevel(keyList, valueList):
    resultList = []
    for i, keys in enumerate(keyList):
        if i >= len(valueList):
            break
        values = valueList[i]
        values = _stripNull(values)
        respDict = dict(list(zip(keys, values)))
        if 'ip_' in respDict and "." not in str(respDict['ip_']):
            respDict = _convertIp(respDict)
        resultList.append(respDict)
    return resultList


def getResultSingleLevel(keyList, valueList):
    values = _stripNull(valueList)
    respDict = dict(list(zip(keyList, values)))
    if 'ip_' in respDict and "." not in str(respDict['ip_']):
        _convertIp(respDict)
    return respDict


def geCurrentfunctionName():
    '''
        get current function name
        :return string
    '''
    return inspect.stack()[1][3]


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


def get_formatteddate_with_delta(dateTime=datetime.now(), timeDelta=None, formatter="%Y-%m-%d %H:%M:%S"):
    '''
        get datetime by delta with the specified format
        :param datetime datetime
        :param timeDelta timeDelta
        :param string formatter
        :return datetime
    '''
    if not isinstance(dateTime, datetime):
        return None
    if timeDelta is not None and not isinstance(timeDelta, timedelta):
        return None
    if timeDelta is None:
        timeDelta = timedelta(days=0)
    return (dateTime + timeDelta).strftime(formatter)


def get_currenttime_as_timestamp(formatter="%Y%m%d%H%M%S"):
    '''
        get current time by the specified format
        :param string formatter
        return datetime
    '''
    return datetime.now().strftime(formatter)


def get_random_color_hex():
    '''
        get random color with hex format
        :return string
    '''

    return "#%s" % str(hex(random.randint(257, 16777215))).replace('0x', '')


def get_url_parameter_ignore_case(url, key):
    '''
        get value of parameter in url with ignore case
        :param string url
        :param string key
        :return string
    '''
    url = url.lower()
    key = key.lower()
    try:
        parsed = urllib.parse.urlparse(url)
        querys = urllib.parse.parse_qs(parsed.query)
        value = querys[key][0]
        return value
    except Exception:
        return None


def __getParaValues(args, index, paraValues, paraValue, kwargs):
    for item in args[index]:
        if len(args) == index + 1:
            itemValue = copy.copy(paraValue)
            itemValue.append(item)
            if "mustValue" in kwargs:
                if kwargs['mustValue'] in itemValue:
                    paraValues.append(itemValue)
            else:
                paraValues.append(itemValue)
        else:
            if index == 0:
                paraValue = []
            itemValue = copy.copy(paraValue)
            itemValue.append(item)
            __getParaValues(args, index + 1, paraValues, itemValue, kwargs)


def getAllParameterizedValues(*args, **kwargs):
    logger.info("get all possible parameterized values %s" % str(args))

    paraValues = []
    __getParaValues(args, 0, paraValues, [], kwargs)
    return paraValues


def getRandomParameterizedValues(randCount, *args, **kwargs):
    logger.info("get %d random possible parameterized values %s" % (randCount, str(args)))

    paraValues = []
    iCount = 1
    for arg in args:
        iCount *= len(arg)
    if randCount > iCount:
        logger.assertErr(False, 'randCount %d cannot be larger than possible count %d' % (randCount, iCount))

    while len(paraValues) < randCount:
        paraValue = []
        for arg in args:
            paraValue.append(arg[random.randint(0, len(arg) - 1)])
        if not paraValue in paraValues:
            if "mustValue" in kwargs:
                if kwargs['mustValue'] in paraValue:
                    paraValues.append(paraValue)
            else:
                paraValues.append(paraValue)
    return paraValues


def getValueTryRemoveTailZero(float_num):
    """
        try to remove .0 from an float number, 2.00 -> 2
        keep other float as it was, 2.02 -> 2.02
        :param float float_num
        :return float/int
    """

    int_num = int(float_num)
    if int_num == float_num:
        return int_num
    return float_num


def getMoneyFormatNumber(int_float_num):
    """
        return the value as money format, 12345 -> 12,345
        :param int/float int_float_num
        :return string
    """

    if isinstance(int_float_num, int):
        return '{:,}'.format(int(int_float_num))
    elif isinstance(int_float_num, float):
        return '{:,}'.format(float(int_float_num))


# endregion

# region Action methods



def runBatchTests(func, funcParams, paramList, apiMsg):
    """
        :param func: pint, function point.
        :param funcParams: tuple or list, function parameter list.
        :param paramList: list, tuple list
        :param apiMsg: string, test api message.
    """
    logger.info("======== Start to run batch tests for api: %s ========" % (apiMsg))
    print("======== Start to run batch tests for api: %s ========" % (apiMsg))
    if paramList is not None and len(paramList) > 0:
        result = {"index": 0, "failCount": 0, "passCount": 0, "errorCount": 0}

        msgList = []
        failMsgList = []
        for params in paramList:
            result["index"] += 1
            msg = "====>[%s] [Test: %s] " % (apiMsg, result["index"])
            try:
                func(*params)
                result["passCount"] += 1
                msg = "%s Pass" % (msg)
            except Exception as e:
                if isinstance(e, AssertionError):
                    result["failCount"] += 1
                    msg = "%s Fail:\t%s" % (msg, e)
                else:
                    result["errorCount"] += 1
                    msg = "%s Error:\t%s" % (msg, e)
                failMsgList.append(msg)
            logger.info(msg)
            print(msg)
            msgList.append(msg)

        sResult = "======== End test for api: %s => Total: %s, Pass: %s, Fail: %s, Error: %s" % (apiMsg,
                                                                                                  result["index"],
                                                                                                  result["passCount"],
                                                                                                  result["failCount"],
                                                                                                  result["errorCount"])
        sResult += ("\n" + "\n".join(failMsgList)) if len(failMsgList) > 0 else ""
        logger.info(sResult)
        print(sResult)
        assert len(failMsgList) == 0, "[Result] test API: %s => FAIL\n%s" % (apiMsg, "\n".join(failMsgList))
    else:
        print("[Error] parameter inputList length should greater than 1.")


def loadDataFromYaml(yamlPath):
    '''
        get data from yaml
        :param string yamlPath
        :return object
    '''

    yamlPath = os.path.join(os.getcwd(), yamlPath).replace('\\', '/')
    return yaml.load(file(yamlPath))


def killProcessByName(processName):
    '''
        kill process by process name at windows platform
        :param string processName
    '''

    logger.info("Kill the pcocess '%s'" % processName)

    try:
        if platform.system() == "Windows":
            os.system("taskkill /f /im %s.exe" % processName)
        else:
            os.system("killall %s" % processName)
    except:
        pass


# endregion

def __end_of_file():
    pass
