# -*- coding: utf-8 -*-
# author: typhoon

import logging
from testconfig import config
from api.business.apiCommonBiz.lbCommon import lbCom
from api.business.apiCommonBiz.userCenter import userCenter
from common.baseRequest import baseRequest
import base64

logger = logging.getLogger(__name__)

#服务端提交请求的通用方法（这是老的实现方式）
def checkAdminFun(postdata,headers):
  #  check about action works
  #  :return:
    logger.info("check get about %s infor..."  %(postdata))
    uri ="rest"
    url = config['admintestApi'] %(uri)
    req = baseRequest(url=url,data=postdata,method="post",headers=headers)
    resp = req.sendJsonRequestReturnDict()
    logger.info("The URl %s response is %s" % (url, resp))
    #request.checkResponseCorrect(resp,"status",statusExp,"the actual status in response %s \does not match the expected %s for URI %S") %(resp,statusExp,uri))
   # dataAct = commonBase.getValue(resp, "code")
    return resp

#调用服务端接口获得测试基础数据的通用方法
def getBaseList(action, check_http_status=200, check_code='200',pageNo=1):
    uri = "rest"
    url = config['admintestApi'] % (uri)
    cmb = userCenter()
    bname = base64.b64decode(config['username'])
    username = bname.decode()
    bpassword = base64.b64decode(config['password'])
    password = bpassword.decode()
    token = cmb.get_access_token(username, password)  # 获取用户token
    headers = {'Content-Type': 'application/json', 'Token': token, 'User-Agent': config['userAgent']}
    postdata={"action":action,"pageNo":pageNo}
    resp = lbCom.send_json_check_code(url=url, send_data=postdata, method="Post", headers=headers,exp_http_status=check_http_status,exp_code=check_code)
    return resp['data']

#获取分类基础信息（用户权限范围内）
def getClassificationList():
    data = getBaseList(action="getClassificationList")
    return data['list']


#获取上课频率基础信息（用户权限范围内）
def getClassFrequencyList():
    data = getBaseList(action="getClassFrequencyList")
    return data['list']



#获取系列基础信息（系列下面是级别）（用户权限范围内）
def getBooksSetList():
    data = getBaseList(action="getBooksSetList")
    return data['list']

#获取级别基础信息（用户权限范围内）
def getBooksSerialList():
    data = getBaseList(action="getBooksSerialList")
    return data['list']

#获取标签基础信息（用户权限范围内）
def getLableList():
    data = getBaseList(action="getLableList")
    return data['lableList']


#获取级别的大纲信息（用户权限范围内）
def getSerialOutlineList():
    resp = getBaseList(action="getSerialOutlineList")
    newlist = [x for x in resp['data']['list'] if x["lessonCount"] != 0]
    if newlist != []:
       return newlist

# 获取课程基础信息（用户权限范围内）
def getCourseList():
    data = getBaseList(action="getCourseList")
    return data['list']

# 获取课节基础信息（用户权限范围内）
def getCourseLessonList():
    data = getBaseList(action="getCourseLessonList")
    return data['list']

#获取试卷列表信息（用户权限范围内）
def getPapersList():
    data = getBaseList(action="getPapersList")
    if data['list'] != []:
       return data['list']

#获取课程包信息
def getPackageList(push_status=None, package_type=None):
    """
    #获取课程包列表信息（用户权限范围内）
    :param push_status: 1 or 0, None或者不填代表查询所有
    :return: 课程包列表
    """
    for num in range(1,10):
        data = getBaseList(action="getPackageList",pageNo=num)
        if data['list']:
            if push_status is not None and package_type is None:
                resp_list = [x for x in data['list'] if x["pushStatus"] == push_status]
                if resp_list!=[]:
                    return resp_list
                    break
            elif package_type is not None and push_status is None:
                resp_list = [x for x in data['list'] if x["packageType"] == package_type]
                if resp_list!=[]:
                    return resp_list
                    break
            elif package_type is not None and push_status is not None:
                resp_list = [x for x in data['list'] if x["packageType"] == package_type and x["pushStatus"] == push_status]
                if resp_list!=[]:
                    return resp_list
                    break
            else:
                return data['list']
                break


