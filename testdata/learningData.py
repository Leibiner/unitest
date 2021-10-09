# -*- coding:utf-8 -*-
from common import envEnum
from common import commonBase as cb
from common.commonBase import env

class LearningData(object):

    # learning数据库信息
    @property
    @env(use_default_mapping=True)
    def learningDb(self):
        return {'qa': {"dbHost": "rm-uf6a61m46w2syo1kpio.mysql.rds.aliyuncs.com",
                        "dbName": "learning",
                        "dbUser": "ln_java",
                        'dbPassword': "uUMBuJ9Bgj3HU3Jh"},
                'online':{"dbHost": "rm-uf6u9005ju25vb5xdo.mysql.rds.aliyuncs.com",
                        "dbName": "learning",
                        "dbUser": "lb_read",
                        'dbPassword': "6K!p1KqKz7yMV8O0"},
                'dev': {'dbHost': '106.14.57.53',
                        'dbName': 'learning',
                        'dbUser': 'ln_java',
                        'dbPassword': 'uUMBuJ9Bgj3HU3Jh'}
        }

    @property
    def open_id(self):
        return cb.get_value_from_env_data_dict(
            {
              "qa":  'ovSMN5AQCSNOIw7AVCoRFjTWzSgM',
              "dev": 'ovSMN5AQCSNOIw7AVCoRFjTWzSgM',
              "online": 'o07IN5AMlQNxFM0oz1qHIXhS_d7k'
            }
        ,use_default_mapping=True)

    # open_id的user_id
    @property
    def user_id(self):
        return cb.get_value_from_env_data_dict(
            {
              "qa":  111,         # qa 非乐宁学员
              "dev": 111,
              "online": 11544             # 线上乐宁学员
            }
        ,use_default_mapping=True)

    @property
    def open_id_ln(self):
        return cb.get_value_from_env_data_dict(
            {
                "qa": 'oDSR45JxGKPkkDU5NAABs6Zv4oNA',
                "dev": 'oDSR45JxGKPkkDU5NAABs6Zv4oNA',
                "online": 'o07IN5BDb_ISX1YraC29rGs61AEI'
            }
            , use_default_mapping=True)

    # open_id_ln的user_id
    @property
    def user_id_ln(self):
        return cb.get_value_from_env_data_dict(
            {
                "qa": 407,
                "dev": 407,
                "online": 4021
            }
            , use_default_mapping=True)

    @property
    def activity_id(self):
        return cb.get_value_from_env_data_dict(
            {
              "qa":  137,
              "dev": 137,
              "online": 191
            }
        ,use_default_mapping=True)

    @property
    def user_activity_id(self):
        return cb.get_value_from_env_data_dict(
            {
              "qa":  61,
              "dev": 61,
              "online": 8
            }
        ,use_default_mapping=True)


    @property
    def user_task_id(self):
        return cb.get_value_from_env_data_dict(
            {
                "qa": 388,
                "dev": 388,
                "online": 34
            }
            , use_default_mapping=True)

    @property
    def task_id(self):
        return cb.get_value_from_env_data_dict(
            {
              "qa":  303,
              "dev": 303,
              "online": 34
            }
        ,use_default_mapping=True)

    @property
    def video_id(self):
        return cb.get_value_from_env_data_dict(
            {
              "qa":  415,
              "dev": 415,
              "online": 133
            }
        ,use_default_mapping=True)


    @property
    def fb_id(self):
        return cb.get_value_from_env_data_dict(
            {
                "qa": 31,
                "dev": 31,
                "online": 54
            }
            , use_default_mapping=True)


    @property
    def serial_id(self):
        return cb.get_value_from_env_data_dict(
            {
                "qa": '5ed27a9638b74c60825a8060c580def4',
                "dev": '5ed27a9638b74c60825a8060c580def4',
                "online": 'c4aae31c50b944969f5ead5ae6032f84'
            }
            , use_default_mapping=True)

    @property
    def user_task_id_custom(self):
        return cb.get_value_from_env_data_dict(
            {
                "qa": 472,
                "dev": 472,
                "online": 44
            }
            , use_default_mapping=True)

    @property
    def task_id_custom(self):
        return cb.get_value_from_env_data_dict(
            {
                "qa": 578,
                "dev": 578,
                "online": 21
            }
            , use_default_mapping=True)

    @property
    def video_id_custom(self):
        return cb.get_value_from_env_data_dict(
            {
                "qa": 619,
                "dev": 619,
                "online": 132
            }
            , use_default_mapping=True)

    # 后台接口数据
    @property
    def set_id(self):
        return cb.get_value_from_env_data_dict(
            {
                "qa": 'cbc61486023a4443b29ed7e10a291e22',
                "dev": 'cbc61486023a4443b29ed7e10a291e22',
                "online": '56645a98f01b460683a645b102fcbc3c'
            }
            , use_default_mapping=True)


    @property
    def teacher_id(self):
        return cb.get_value_from_env_data_dict(
            {
                "qa": '7b08650483314c15b8a9f7c60f25aab1',
                "dev": '7b08650483314c15b8a9f7c60f25aab1',
                "online": '0229229be50045e587c0f51368e3252b'
            }
            , use_default_mapping=True)

    #region 预警数据
    # 学员预警id
    @property
    def warn_id(self):
        return cb.get_value_from_env_data_dict(
            {
                "qa": 'c94d835a-f9a6-48f5-a811-cc8685440b6f',
                "dev": 'c94d835a-f9a6-48f5-a811-cc8685440b6f',
                "online": '9843752c-7435-46be-b915-22f722d8c2f8'
            }
            , use_default_mapping=True)

    # endregion

    # region 背呗小程序数据
    # 挑战id
    @property
    def activity_id(self):
        return cb.get_value_from_env_data_dict(
            {
                "qa": '771937b235b611ea88b87cd30ab8ab76',
                "online": 'ec99f6ec88004542a53ad5bde6d205cb'
            }
            , use_default_mapping=True)


    # 任务id
    @property
    def task_id(self):
        return cb.get_value_from_env_data_dict(
            {
                # "qa": '027cd4615a3c4452b377ddaa9d227f0b',
                "qa": '66f717d636b442c2928a80c48b734d8f',
                # "online": 'b34d9cb671eb405cb2ecfc5830d6b653'
                "online": 'fafe6fc4dc814731b61cac1fc21f95d3'
            }
            , use_default_mapping=True)

    # 背诵视频id
    @property
    def video_id(self):
        return cb.get_value_from_env_data_dict(
            {
                "qa": 'dad9ba06c9b44294a48195b98d968935',
                "online": '8fee9594017c4caeb03dbe45d06f7dfe'
                # "online": '3b9c901d478d42f88a42a75302221862'
            }
            , use_default_mapping=True)

  # 朗读视频id

    @property
    def read_video_id(self):
        return cb.get_value_from_env_data_dict(
            {
                "qa": '62717d505c894ce9aad5964cb52745bc',
                "online": '5121d73bfeda4c519c88df4d2582ce34'
            }
            , use_default_mapping=True)

    # 已点评视频id
    @property
    def comment_video_id(self):
        return cb.get_value_from_env_data_dict(
            {
                "qa": 'db824350a2884299b3fe486b5b0e7698',
                "online": '3b9c901d478d42f88a42a75302221862'
            }
            , use_default_mapping=True)

    # 他人视频id
    @property
    def other_video_id(self):
        return cb.get_value_from_env_data_dict(
            {
                "qa": 'dad9ba06c9b44294a48195b98d968935',
                "online": '804c6922cfbb400ab576e9e54b9587fd'
            }
            , use_default_mapping=True)

    # 关键字手卡id
    @property
    def card_id(self):
        return cb.get_value_from_env_data_dict(
            {
                "qa": 71,
                "online": 12
            }
            , use_default_mapping=True)

    # 分享域名
    @property
    def app_share_url(self):
        return cb.get_value_from_env_data_dict(
            {
                "qa": 'https://qa1bb.learningbee.net/#/',
                "online": 'https://bb.learningbee.net/#/'
            }
            , use_default_mapping=True)

    # 海报二维码的参数，db记录id
    @property
    def poster_id(self):
        return cb.get_value_from_env_data_dict(
            {
                "qa": 237,
                "online": 237  # 待修改
            }
            , use_default_mapping=True)

    # endregion

    # region
    def test(self):
        pass
    # endregion


learningData = LearningData()