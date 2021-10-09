# -*- coding: UTF-8 -*-
# Author: leibin


from api.business.apiCommonBiz.userCenter import uc
from testdata.userData import userData
from api.business.apiCloudBbadmin.apiBbAdminClassQuery import ApiBbAdminClass as ApiBb

class testBbAdminClassQuery(object):

    @classmethod
    def setupClass(self):
        self.token = uc.get_CampusUserAccess_token(userData.CloudAuthAccount1['userName'],
                                                   userData.CloudAuthAccount1['passWord'])

        # self.token = 'eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJsYl9ocSIsInVzZXJJZCI6IjM2REMwMUFCLTBBMTItMDBFRC1BMEU4LVhDMTJSTEswMTFWIiwibmFtZSI6IuiuuOaDoOe6oiIsImV4cCI6MTU4NTY2MzE4Nn0.Dcx6OU6e_jddchlh-X-fR38pCtmbElGoXYe1X_U82t7pUbM_b9-IRQUCHZMQFtyZ8SSFKQRZ0aVoxr-HReqXmX5OJe0-SIqPqdh36T9ipHSZrCI6rJAWZ3konQScTgYkiDSSd6FMD4tAx48HJb5872Vz_T_Tds9E5Ml_wPPZ0Gc'
        self.headers = {"Content-Type": "application/json", "Authorization": self.token}

    @classmethod
    def teardownClass(self):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test1012_check_query_user_video_db(self):
        data = {
            "taskId": 1,
            "sortField": 0,
            "sortType": 1,
            "currentPage": 1,
            "pageSize": 10
        }
        self._query_video_list_db_check(data)

    def _query_video_list_db_check(self,data):

        resp = ApiBb.post_query_user_video(send_data=data, headers=self.headers)
        print(resp)





