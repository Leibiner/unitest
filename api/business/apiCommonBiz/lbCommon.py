# -*- coding: utf-8 -*-
# author: dengtao

from common.baseRequest import baseRequest



class lbCommon(baseRequest):

    def send_json_check_code(self, url, send_data, method, headers=None, token=None, x_client_token=None,
                             cookie=None, exp_http_status=200, check_name='code', exp_code='200'):
        """
        发送json请求公共方法
        :param url:
        :param send_data:
        :param method:
        :param headers:
        :param token:
        :param x_client_token:
        :param cookie:
        :param exp_http_status:
        :param check_name: 检查code的字段
        :param exp_code:
        :return:
        """
        req = baseRequest(url=url, data=send_data, method=method, headers=headers, token=token, x_client_token=x_client_token,
                          cookies=cookie)
        resp = req.sendJsonRequestReturnDict(httpStatusExp=exp_http_status, statusExp=exp_code, check_name=check_name)
        return resp

    def send_urlencoded_form_data(self, url, send_data, method, check_name='code', headers=None, token=None,
                                  x_client_token=None,cookie=None, exp_code='200'):
        """
        发送x-www-form-urlencoded请求公共方法
        :param url:
        :param send_data: 字典
        :param method:
        :param check_name: 检查code的字段
        :param headers:
        :param token:
        :param x_client_token:
        :param cookie:
        :param exp_http_status:
        :param exp_code:
        :return:
        """
        req = baseRequest(url=url, data=send_data, method=method, headers=headers, x_client_token=x_client_token,
                          token=token, cookies=cookie)
        resp = req.sendUrlEncodedRequest(statusExp=exp_code, check_name=check_name)
        return resp

    def send_multipart_form_data(self, url, send_data, method, check_name='code', headers=None, token=None,
                                  x_client_token=None,cookie=None, exp_code='200'):
        """
        发送multipart-form请求公共方法
        :param url:
        :param send_data:字典，value必须为字符串
        :param method:
        :param check_name: 检查code的字段
        :param headers:
        :param token:
        :param x_client_token:
        :param cookie:
        :param exp_http_status:
        :param exp_code:
        :return:
        """
        from requests_toolbelt import MultipartEncoder
        import random
        import string
        m = MultipartEncoder(
            fields=send_data,
            boundary='------'+''.join(random.sample(string.ascii_letters + string.digits, 32))
            )
        req = baseRequest(url=url, data=send_data, method=method, headers=headers, x_client_token=x_client_token,
                          token=token, cookies=cookie, multipartEncodedContent=m)
        resp = req.sendMultipartRequest(statusExp=exp_code, check_name=check_name)
        return resp


lbCom = lbCommon()