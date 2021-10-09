# coding:utf-8
import requests
import json
import unittest
from conf.lbHost import lbHost





class post_request(unittest.TestCase):
    host = lbHost.CloudAuthHost

    def setUp(self):
        self.uri = '/api/item/admin/query'
        self.url = self.host + self.uri
        print(self.url)
        self.header = {'Content-Type': 'application/json',
                       'token': 'NTQ3OGMTAwMDAwMDAyMDAxMDI1MF8tMV8tMV8xMDYuMTQuMTkyLjE1OF8yXzQ0XzE2MzI5NDIwMDAwMDBfMV85'}  # 根据实际内容，自己填写

    def test_post_01(self):
        data = {
                "pageId": 1,
                "pageSize": 10,
                "sortColumn": "updated_at",
                "sortDir": "DESC",
                "where": {
                    "rules": [
                        {
                            "value": 1,
                            "field": "status",
                            "op": "EQ"
                        },
                        {
                            "field": "item_type",
                            "op": "IN",
                            "value": [
                                0,
                                2,
                                7,
                                11
                            ]
                        }
                    ]
                }
            } # 根据实际内容，自己填写
        # 将data序列化为json格式数据，传递给data参数
        resp = requests.post(self.url, data=json.dumps(data), headers = self.header)
        print(resp.text)
        print(self.url)
        self.assertEqual(200,200,'测试失败')



    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main() 