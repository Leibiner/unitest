# -*- coding:utf-8 -*-
from common.commonBase import env

class UserData(object):

    # CloudAuth账户1
    @property
    @env(use_default_mapping=True)
    def CloudAuthAccount1(self):
        return {
            "qa": {'userName': 'xianbb', 'passWord': 'test_xianbb_123!', 'nickName': '自动化测试'},
        }



userData = UserData()