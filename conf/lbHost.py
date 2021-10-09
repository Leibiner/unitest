# -*- coding:utf8 -*-
#  Author:leibin
from common.commonBase import env

class LbHost(object):

    @property
    @env
    def CloudAuthHost(self):
        """测试环境"""
        return {
                "qa":  'https://mapi.ireeder.com',  # 新域名
                }


lbHost = LbHost()