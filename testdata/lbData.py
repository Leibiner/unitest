# -*- coding:utf-8 -*-
from common import envEnum
from common import commonBase as cb
from common.commonBase import env

class LbData(object):

    # learning老的talkbee数据库信息
    @property
    @env(use_default_mapping=True)
    def learningDb(self):
        return {'qa': {"dbHost": "rm-uf6a61m46w2syo1kpio.mysql.rds.aliyuncs.com",
                        "dbName": "learning",
                        "dbUser": "ln_java",
                        'dbPassword': "uUMBuJ9Bgj3HU3Jh"},
                'online':{"dbHost": "rm-uf6u9005ju25vb5xdo.mysql.rds.aliyuncs.com",
                        "dbName": "learning",
                        "dbUser": "ln_test",
                        'dbPassword': "RofnJEucAWeFi7Ab"}
        }

    # learningBase数据库信息
    @property
    @env(use_default_mapping=True)
    def learningBaseDb(self):
        return {'qa': {"dbHost": "rm-uf6a61m46w2syo1kpio.mysql.rds.aliyuncs.com",
                        "dbName": "learning_base",
                        "dbUser": "ln_java",
                        'dbPassword': "uUMBuJ9Bgj3HU3Jh"},
                'online':{"dbHost": "rm-uf60k5txb0cviq653po.mysql.rds.aliyuncs.com",
                        "dbName": "learning_base",
                        "dbUser": "ln_test",
                        'dbPassword': "RofnJEucAWeFi7Ab"}
        }

    # ln_cloud_sys数据库信息
    @property
    @env
    def ln_cloud_sys_Db(self):
        return {'qa': {"dbHost": "rm-uf6a61m46w2syo1kpio.mysql.rds.aliyuncs.com",
                        "dbName": "ln_cloud_sys",
                        "dbUser": "ln_java",
                        'dbPassword': "uUMBuJ9Bgj3HU3Jh"},
                'online': {"dbHost": "rm-uf60k5txb0cviq653po.mysql.rds.aliyuncs.com",
                           "dbName": "ln_cloud_sys",
                           "dbUser": "ln_test",
                           'dbPassword': "RofnJEucAWeFi7Ab"}
        }

    # ln_cloud_user数据库信息
    @property
    @env
    def ln_cloud_user_Db(self):
        return {'qa': {"dbHost": "rm-uf6a61m46w2syo1kpio.mysql.rds.aliyuncs.com",
                        "dbName": "ln_cloud_user",
                        "dbUser": "ln_java",
                        'dbPassword': "uUMBuJ9Bgj3HU3Jh"},
                'online': {"dbHost": "rm-uf60k5txb0cviq653po.mysql.rds.aliyuncs.com",
                           "dbName": "ln_cloud_user",
                           "dbUser": "ln_test",
                           'dbPassword': "RofnJEucAWeFi7Ab"}
        }


    # ln_cloud_teachingaffairs数据库信息
    @property
    @env
    def ln_cloud_teachingaffairs_Db(self):
        return {'qa': {"dbHost": "rm-uf6a61m46w2syo1kpio.mysql.rds.aliyuncs.com",
                        "dbName": "ln_cloud_teachingaffairs",
                        "dbUser": "ln_java",
                        'dbPassword': "uUMBuJ9Bgj3HU3Jh"},
                'qa1': {"dbHost": "rm-uf6a61m46w2syo1kpio.mysql.rds.aliyuncs.com",
                       "dbName": "ln_cloud_teachingaffairs",
                       "dbUser": "ln_java",
                       'dbPassword': "uUMBuJ9Bgj3HU3Jh"},
                'online': {"dbHost": "rm-uf6wld5n30tu6fj26co.mysql.rds.aliyuncs.com",
                           "dbName": "ln_cloud_teachingaffairs",
                           "dbUser": "ln_cloud_test",
                           'dbPassword': "eFvW@2Siy8Tnf!c@"}
        }

    # ln_cloud_oa数据库信息
    @property
    @env
    def ln_cloud_oa_Db(self):
        return {'qa': {"dbHost": "rm-uf6a61m46w2syo1kpio.mysql.rds.aliyuncs.com",
                        "dbName": "ln_cloud_oa",
                        "dbUser": "ln_java",
                        'dbPassword': "uUMBuJ9Bgj3HU3Jh"},
                'qa1': {"dbHost": "rm-uf6a61m46w2syo1kpio.mysql.rds.aliyuncs.com",
                       "dbName": "ln_cloud_oa",
                       "dbUser": "ln_java",
                       'dbPassword': "uUMBuJ9Bgj3HU3Jh"},
                'online': {"dbHost": "rm-uf6wld5n30tu6fj26co.mysql.rds.aliyuncs.com",
                           "dbName": "ln_cloud_oa",
                           "dbUser": "ln_cloud_test",
                           'dbPassword': "eFvW@2Siy8Tnf!c@"}
        }


    # ln_cloud_wechat数据库信息
    @property
    @env
    def ln_cloud_wechat_Db(self):
        return {'qa': {"dbHost": "rm-uf6a61m46w2syo1kpio.mysql.rds.aliyuncs.com",
                        "dbName": "ln_cloud_wechat",
                        "dbUser": "ln_java",
                        'dbPassword': "uUMBuJ9Bgj3HU3Jh"},
                'online': {"dbHost": "rm-uf60k5txb0cviq653po.mysql.rds.aliyuncs.com",
                           "dbName": "ln_cloud_wechat",
                           "dbUser": "ln_test",
                           'dbPassword': "RofnJEucAWeFi7Ab"}
        }


    # ln_cloud_order数据库信息
    @property
    @env
    def ln_cloud_order_Db(self):
        return {'qa': {"dbHost": "rm-uf6a61m46w2syo1kpio.mysql.rds.aliyuncs.com",
                        "dbName": "ln_cloud_order",
                        "dbUser": "ln_java",
                        'dbPassword': "uUMBuJ9Bgj3HU3Jh"},
                'online': {"dbHost": "rm-uf60k5txb0cviq653po.mysql.rds.aliyuncs.com",
                           "dbName": "ln_cloud_order",
                           "dbUser": "ln_test",
                           'dbPassword': "RofnJEucAWeFi7Ab"}
        }


    # ln_cloud_product数据库信息
    @property
    @env
    def ln_cloud_product_Db(self):
        return {'qa': {"dbHost": "rm-uf6a61m46w2syo1kpio.mysql.rds.aliyuncs.com",
                        "dbName": "ln_cloud_product",
                        "dbUser": "ln_java",
                        'dbPassword': "uUMBuJ9Bgj3HU3Jh"},
                'online': {"dbHost": "rm-uf60k5txb0cviq653po.mysql.rds.aliyuncs.com",
                           "dbName": "ln_cloud_product",
                           "dbUser": "ln_test",
                           'dbPassword': "RofnJEucAWeFi7Ab"}
        }


    # ln_cloud_beibei数据库信息
    @property
    @env
    def ln_cloud_beibei_Db(self):
        return {'qa': {"dbHost": "rm-uf6a61m46w2syo1kpio.mysql.rds.aliyuncs.com",
                       "dbName": "ln_cloud_beibei",
                       "dbUser": "ln_java",
                       'dbPassword': "uUMBuJ9Bgj3HU3Jh"},
                'online': {"dbHost": "rm-uf6wld5n30tu6fj26co.mysql.rds.aliyuncs.com",
                           "dbName": "ln_cloud_beibei",
                           "dbUser": "ln_cloud_test",
                           'dbPassword': "eFvW@2Siy8Tnf!c@"}
                }

    # ln_cloud_message数据库信息
    @property
    @env
    def ln_cloud_message_Db(self):
        return {'qa': {"dbHost": "rm-uf6a61m46w2syo1kpio.mysql.rds.aliyuncs.com",
                       "dbName": "ln_cloud_message",
                       "dbUser": "ln_java",
                       'dbPassword': "uUMBuJ9Bgj3HU3Jh"},
                'online': {"dbHost": "rm-uf6wld5n30tu6fj26co.mysql.rds.aliyuncs.com",
                           "dbName": "ln_cloud_message",
                           "dbUser": "ln_cloud_test",
                           'dbPassword': "eFvW@2Siy8Tnf!c@"}
                }

    # ln_cloud_content数据库信息
    @property
    @env
    def ln_cloud_content_Db(self):
        return {'qa': {"dbHost": "rm-uf6a61m46w2syo1kpio.mysql.rds.aliyuncs.com",
                       "dbName": "ln_cloud_content",
                       "dbUser": "ln_java",
                       'dbPassword': "uUMBuJ9Bgj3HU3Jh"},
                'online': {"dbHost": "rm-uf6wld5n30tu6fj26co.mysql.rds.aliyuncs.com",
                           "dbName": "ln_cloud_content",
                           "dbUser": "ln_cloud_test",
                           'dbPassword': "eFvW@2Siy8Tnf!c@"}
                }


    # ln_cloud_exercise数据库信息
    @property
    @env
    def ln_cloud_exercise_Db(self):
        return {'qa': {"dbHost": "rm-uf6a61m46w2syo1kpio.mysql.rds.aliyuncs.com",
                       "dbName": "ln_cloud_exercise",
                       "dbUser": "ln_java",
                       'dbPassword': "uUMBuJ9Bgj3HU3Jh"},
                'online': {"dbHost": "rm-uf6wld5n30tu6fj26co.mysql.rds.aliyuncs.com",
                           "dbName": "ln_cloud_exercise",
                           "dbUser": "ln_cloud_test",
                           'dbPassword': "eFvW@2Siy8Tnf!c@"}
                }


    # Mongo数据库信息
    @property
    @env(use_default_mapping=True)
    def lbMongoDb(self):
        return {
                'qa': {"dbHost": "dds-uf62c2207ab1f6241414-pub.mongodb.rds.aliyuncs.com",
                        "dbName": "learningdata",
                        "dbUser": "lb_readWrite",
                        'dbPassword': "tZCHmVnz3s7e8gI#",
                        'dbPort': 3717},
                'online': {"dbHost": "dds-uf64dda58f6b28d41932-pub.mongodb.rds.aliyuncs.com",
                       "dbName": "learningdata",
                       "dbUser": "lb_read",
                       'dbPassword': "$Sw02DZmyoSlzoWg",
                       'dbPort':3717}
                }


    @property
    def serialId(self):
        return cb.get_value_from_env_data_dict(
            {
              "qa":  '12376d1a5b0911e7b2a0784f435db3fa',
              "dev": '12376d1a5b0911e7b2a0784f435db3fa',
              "online": '1588e7e2c46911e788de784f435db3fa'
            }
        ,use_default_mapping=True)

    @property
    def paperId(self):
        return cb.get_value_from_env_data_dict(
            {
              "qa":  '0ef341d71aab49c8bab66e32c0524f74',
              "dev": '0ef341d71aab49c8bab66e32c0524f74',
              "online": '8ea83e1ab9d54362933d9e11104952ff'
            }
            , use_default_mapping=True)

    @property
    def execisesList(self):
        return cb.get_value_from_env_data_dict(
            {
             "qa":  [{"exercisesId":"3f188eec5ad4401f9c21cd28d67734ce","choiceId":"ca1bab2777ff4b94b967b4e9743b9597"},
                      {"exercisesId":"557e3a5b9af449a8b235ac86bcd472ff","choiceId":"c423e4280452435789b3d2e63992d171"},
                      {"exercisesId":"66968eec3bc542ef9704ab86844f4f4a","choiceId":"ab07dd3f67ec4bf38c35b5388466f98d"},
                      {"exercisesId":"83a3fea5b31f47a69866cc05a4b461a2","choiceId":"70fb97f9637c40aa8ec03d6a40bd45a6"}],
              "dev": [{"exercisesId":"3f188eec5ad4401f9c21cd28d67734ce","choiceId":"ca1bab2777ff4b94b967b4e9743b9597"},
                      {"exercisesId":"557e3a5b9af449a8b235ac86bcd472ff","choiceId":"c423e4280452435789b3d2e63992d171"},
                      {"exercisesId":"66968eec3bc542ef9704ab86844f4f4a","choiceId":"ab07dd3f67ec4bf38c35b5388466f98d"},
                      {"exercisesId":"83a3fea5b31f47a69866cc05a4b461a2","choiceId":"70fb97f9637c40aa8ec03d6a40bd45a6"}],
              "online": []
            }
            , use_default_mapping=True)

    @property
    def PackageId(self):
        return cb.get_value_from_env_data_dict(
            {
              "qa":  '62c29b95598c475e9a2895bd877c5100',
              "dev": '88486e058c334a53914cf1d3d4de6f71',
              "online": 'aaaaaaaa'
            }
            , use_default_mapping=True)


    @property
    def frequencyidListOfPackageId(self):
        return cb.get_value_from_env_data_dict(
            {
              "qa": ['714d732053734ee99dd3502ecb9c3027','c0738bd686b1466f86599871c137ceed'],
              "dev": ['714d732053734ee99dd3502ecb9c3027','c0738bd686b1466f86599871c137ceed'],
              "online": ''
            }
            , use_default_mapping=True)

    @property
    def OrderCode(self):  #订单号，查看订单详情接口使用
        return cb.get_value_from_env_data_dict(
            {
              "qa":  '153148202911904981367',
              "dev": '152454732610498526430',
              "online": '150649869430594130857'
            }
            , use_default_mapping=True)

    @property
    def ScheduleId(self):
        return cb.get_value_from_env_data_dict(
            {
              "qa":  '90c261b59216408390b8f39c068842d4',
              "dev": '90c261b59216408390b8f39c068842d4',
              "online": ''
            }
            , use_default_mapping=True)

    @property
    def AutoteacherList(self):
        return cb.get_value_from_env_data_dict({
            "qa": ['5bc40a4f877d40eaa6cb616875384737', '7b08650483314c15b8a9f7c60f25aab1','c48f535c72c0423ea787920135e17e80'],
            "dev": ['5bc40a4f877d40eaa6cb616875384737', '7b08650483314c15b8a9f7c60f25aab1','c48f535c72c0423ea787920135e17e80'],
            "online": ['0229229be50045e587c0f51368e3252b', '','']},use_default_mapping=True)

    @property
    def PackageSkuCode(self):
        return cb.get_value_from_env_data_dict(
            {
              "qa":  '20191231byzgf',
              "dev": '',
              "online": ''
            }
            , use_default_mapping=True)

    #造数据工具专用的，自动化用例不要用
    @property
    def ManualteacherList(self):
        return cb.get_value_from_env_data_dict(
            {
              "qa":  ['6c7d303d1c7e4359b530100fc4c21e81','5bc40a4f877d40eaa6cb616875384737','947230f9e68b40688b564f332f4039d3','9b33cf74c85e439e9da131b6b002c40f','a3c912fb01c1400a86ddf3da7f0f5848','bb62ed6ae9814601a00cd05a0b7b50ba'],
              "dev": ['4341e87f7ee446a09462aef40d8dce66','5bc40a4f877d40eaa6cb616875384737','947230f9e68b40688b564f332f4039d3','9b33cf74c85e439e9da131b6b002c40f','a3c912fb01c1400a86ddf3da7f0f5848','bb62ed6ae9814601a00cd05a0b7b50ba'],
              "online": ''
            }
            , use_default_mapping=True)






lbData = LbData()