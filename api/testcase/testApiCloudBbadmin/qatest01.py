# coding:utf-8
import requests
import unittest
import json


class get_request(unittest.TestCase):
    def setUp(self):
        self.post_url = 'https://mapi.ireeder.com/api/account/user/login/login?username=xianbb&password=test_xianbb_123!'

    def test_post_01(self):
        url = self.post_url
        r = requests.post(url)
        print(r.text)
        token = r.json()["code"]
        print("code:", token)




    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()