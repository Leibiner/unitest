# -*- coding:utf8 -*-
# Author: leibin


from conf.lbHost import lbHost
from api.business.apiCommonBiz.lbCommon import  lbCommon




class ApiBbAdminClass(lbCommon):
    host = lbHost.CloudAuthHost

    # 背呗视频列表查询
    def post_query_user_video(self, send_data=None, headers=None, check_code=200):
        uri = '/api/item/admin/query'
        url = self.host + uri
        print(url)
        resp = self.send_json_check_code(url=url, send_data=send_data, method="Post", headers=headers,
                                             check_name="status", exp_code=check_code)
        return resp


ApiBbAdminClass = ApiBbAdminClass()

