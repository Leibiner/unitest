# -*- coding:utf8 -*-
#  Author:typhoon

from testconfig import config
from common.baseRequest import baseRequest
from common import commonBase
from api.business.apiCommonBiz.lbCommon import lbCom
from conf.lbHost import lbHost
from testdata.userData import userData

class userCenter(object):
    CloudHost = lbHost.CloudAuthHost
    def send_request(self, method, url, data=None, headers=None, cookie=None, files=None, httpStatusExp=200, **kwargs):
        # type: (object, object, object, object, object, object, object, object) -> object

        req = baseRequest(method, url, data, headers, cookie, files)
        resp = req.sendJsonRequestReturnDict(httpStatusExp)
        return resp
     #  ～～～～～～～～～～～～～～ "登录乐宁校区查询管理系统～～～～～～～～～～～～～～～～～"
    def CampusLogin(self,):

        strPsw = commonBase.decrypt(encPsw)
        uri = '/api/account/user/login/login?username=xianbb&password=test_xianbb_123!'
        url = lbHost.CloudAuthHost  + uri
        resp = lbCom.send_urlencoded_form_data(url=url,send_data=send_data,method="post", exp_code=None)
        return resp['data']

    def get_CampusUserAccess_token(self, username, password):
        "获取用户token"
        logindata = self.CampusLogin(username, password)
        if logindata is not None:
            if "token" in logindata:
                return logindata["token"]
            else:
                return None
        else:
            return None
    #  ～～～～～～～～～～～～～～ "登录乐宁校区查询管理系统～～～～～～～～～～～～～～～～～"


uc = userCenter()

