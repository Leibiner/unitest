# -*- coding:utf-8 -*-

from common import commonBase as cb
from common.commonBase import env

class erpData(object):

    # 数据库信息
    # @property
    # def ErpOnlineDb(self):
    #     return {
    #         "dbHost":"47.96.164.76",
    #         "dbName": "xgj_w1_lnjy",
    #         "JMXdbName": "XGJ_W1_LENING",
    #         "dbUser": "xgj_read",
    #         'dbPassword': "i&25lrFhups1uhdqfK"
    #         }

    # erp新库
    @property
    def ErpOnlineDb(self):
        return {
            "dbHost":"rm-uf6102omd138o2s3qro.sqlserver.rds.aliyuncs.com",
            "dbName": "xgj_w1_lnjy",
            "JMXdbName": "XGJ_W1_LENING",
            "dbUser": "ln_test",
            'dbPassword': "vLm5m&kDu4B2fJDC"
            }

    #测试校区
    @property
    @env(use_default_mapping=True)
    def ERPCampusId(self):
        return {
              "qa":  ['14D10F0F-0C58-4270-A1C8-5C64B3C5C03E','D4A53EB5-4260-42BB-AABA-4B7AAEC1A154'],  #
              "dev": ['14D10F0F-0C58-4270-A1C8-5C64B3C5C03E','D4A53EB5-4260-42BB-AABA-4B7AAEC1A154'],
              "online": ['14D10F0F-0C58-4270-A1C8-5C64B3C5C03E','D4A53EB5-4260-42BB-AABA-4B7AAEC1A154']
            }

    #测试校区
    @property
    @env(use_default_mapping=True)
    def ERPtestCampusId(self):
        return {
              "qa":  "'14D10F0F-0C58-4270-A1C8-5C64B3C5C03E','D4A53EB5-4260-42BB-AABA-4B7AAEC1A154'",  #
              "dev": "'14D10F0F-0C58-4270-A1C8-5C64B3C5C03E','D4A53EB5-4260-42BB-AABA-4B7AAEC1A154'",
              "online": "'14D10F0F-0C58-4270-A1C8-5C64B3C5C03E','D4A53EB5-4260-42BB-AABA-4B7AAEC1A154'"
            }

    #（leads转）App成功ID标记
    @property
    @env(use_default_mapping=True)
    def ERPAppSuccessId(self):
        return {
              "qa":  "'14D10F0F-0C58-4270-A1C8-5C64B3C5C03E','D4A53EB5-4260-42BB-AABA-4B7AAEC1A154'",  #
              "dev": "'14D10F0F-0C58-4270-A1C8-5C64B3C5C03E','D4A53EB5-4260-42BB-AABA-4B7AAEC1A154'",
              "online": "'14D10F0F-0C58-4270-A1C8-5C64B3C5C03E','D4A53EB5-4260-42BB-AABA-4B7AAEC1A154'"
            }

    #TMK市场标记
    @property
    @env(use_default_mapping=True)
    def leadsDepartId(self):
        return {
              "qa":  "'1D2A60094-294C-4CA9-99CA-D5D1CB45E67C','D4A53EB5-4260-42BB-AABA-4B7AAEC1A154'",  #
              "dev": "'D2A60094-294C-4CA9-99CA-D5D1CB45E67C','D4A53EB5-4260-42BB-AABA-4B7AAEC1A154'",
              "online": "'D2A60094-294C-4CA9-99CA-D5D1CB45E67C','D4A53EB5-4260-42BB-AABA-4B7AAEC1A154'"
            }

    #ERP的线下级别
    @property
    @env(use_default_mapping=True)
    def ERPlevelList(self):
        return {
              "qa":  ['C1','C2','C3','K1','K2'],  #
              "dev": ['C1','C2','C3','C4','C5','C6','K1','K2','K3','K4','Y1','Y2','Y3','Y4','Y5','Y6'],
              "online": ['C1','C2','C3','C4','C5','C6','K1','K2','K3','K4','Y1','Y2','Y3','Y4','Y5','Y6']
            }

    #线下班级及学生ID
    @property
    def ERPClassAndStudentList(self):
        return cb.get_value_from_env_data_dict({
            "qa": [{"ErpClassId":"0ABFA3DC-7A52-4911-8E94-0C7276320ADC","ErpStudentId":"F7CDBD43-1311-484C-A28A-58620F2782A0","ErpShiftId":"9F628683-50DC-4848-B2CE-C8029BFDAF69"}],
            "dev": [{"ErpClassId":"D342CE92-2BDA-4732-9BB9-BC7D587D7734","ErpStudentId":"F7CDBD43-1311-484C-A28A-58620F2782A0","ErpShiftId":"9F628683-50DC-4848-B2CE-C8029BFDAF69"}],
            "online":[{"ErpClassId":"'1111'","ErpStudentId":"1111","ErpShiftId":"9F628683-50DC-4848-B2CE-C8029BFDAF69"}]
                                               },use_default_mapping=True)
    #合同的收费类型ID（例如新增、续费、扩科、提前续班、预存），这个ID是在OPENAPI的learningbase库中base_information_relation表里面的sys_dic_guid值
    @property
    @env(use_default_mapping=True)
    def SyscTypeIdList(self):
        return {
              "qa":  ['E55E5DBF-D993-44C0-832A-3C1B9C335E1F', '1CD35487-7C7D-44D6-9C1C-A39222D89893', 'BE90C0DB-5EB2-44C0-A097-FDD5F9A46159',
                'E7B62025-A0DF-4A76-B8C4-156E767EEC10', '4F9853E8-FC98-4795-81F9-42F6E383B38C'],  #
              "dev": ['E55E5DBF-D993-44C0-832A-3C1B9C335E1F', '1CD35487-7C7D-44D6-9C1C-A39222D89893', 'BE90C0DB-5EB2-44C0-A097-FDD5F9A46159',
                'E7B62025-A0DF-4A76-B8C4-156E767EEC10', '4F9853E8-FC98-4795-81F9-42F6E383B38C'],
              "online":['E55E5DBF-D993-44C0-832A-3C1B9C335E1F', '1CD35487-7C7D-44D6-9C1C-A39222D89893', 'BE90C0DB-5EB2-44C0-A097-FDD5F9A46159',
                'E7B62025-A0DF-4A76-B8C4-156E767EEC10', '4F9853E8-FC98-4795-81F9-42F6E383B38C']
            }

    #积分商城要用的客户意向表中的客户手机号
    @property
    def ERPcCustomerTelList(self):
        return cb.get_value_from_env_data_dict({
            "qa": ['13611877485'],
            "dev": ['13611877485'],
            "online": '13611877485'},use_default_mapping=True)

    #积分商城要用的收费的学生ID号以及其介绍人的ID号，用于查某指定的这天(自动化目前只取2019年1月9号)是否有报名过
    @property
    def ERPcStudentAndCustomerIDList(self):
        return cb.get_value_from_env_data_dict({
            "qa": [{"ErpStudentId":'2CD6E956-E03E-4766-AB4B-6F19332C4C2A',"ErpIntroducerId":'9D224199-055E-4FD6-9D53-2B683B2382A8'}],
            "dev": [{"ErpStudentId":'0A1B9925-97B3-458D-BA36-B54719EADBA1',"ErpIntroducerId":'B2154399-7A19-4A24-991A-0032A94B62A5'}],
            "online": [{"ErpStudentId":'2CD6E956-E03E-4766-AB4B-6F19332C4C2A',"ErpIntroducerId":'9D224199-055E-4FD6-9D53-2B683B2382A8'}]},use_default_mapping=True)

    # B1A90631-9192-42B3-9BEC-2972B393CFE3 表示扩科
    # 109AACAE-B174-40AA-9042-58CF05154FA6 新增
    # AC3CF9E7-6E9B-43F0-BC0F-4E89C63520B2 续费
    # 7D029238-616B-408E-981D-E9E7AB6B7F62 提前续班
    # FD25CBA2-BE8B-414D-A38B-4389C5B7361F 新增
    # 845A4EDB-33C6-415E-BF00-3CE71D5BBD20 续费
    # 472642E5-EFAA-4F22-9833-400D5E450501 扩科
    #积分商城要用的 收费性质, 购买课程者自己本人购买的时候需要加积分的收费性质限定
    @property
    def ERPCustTypeForMeList(self):
        return cb.get_value_from_env_data_dict(
            {
              "qa":  ['109AACAE-B174-40AA-9042-58CF05154FA6','FD25CBA2-BE8B-414D-A38B-4389C5B7361F',
                      'AC3CF9E7-6E9B-43F0-BC0F-4E89C63520B2','845A4EDB-33C6-415E-BF00-3CE71D5BBD20',
                      'B1A90631-9192-42B3-9BEC-2972B393CFE3','472642E5-EFAA-4F22-9833-400D5E450501', '7D029238-616B-408E-981D-E9E7AB6B7F62'],
              "dev": ['109AACAE-B174-40AA-9042-58CF05154FA6','FD25CBA2-BE8B-414D-A38B-4389C5B7361F',
                      'AC3CF9E7-6E9B-43F0-BC0F-4E89C63520B2','845A4EDB-33C6-415E-BF00-3CE71D5BBD20',
                      'B1A90631-9192-42B3-9BEC-2972B393CFE3','472642E5-EFAA-4F22-9833-400D5E450501', '7D029238-616B-408E-981D-E9E7AB6B7F62'],
              "online": ['109AACAE-B174-40AA-9042-58CF05154FA6','FD25CBA2-BE8B-414D-A38B-4389C5B7361F',
                      'AC3CF9E7-6E9B-43F0-BC0F-4E89C63520B2','845A4EDB-33C6-415E-BF00-3CE71D5BBD20',
                      'B1A90631-9192-42B3-9BEC-2972B393CFE3','472642E5-EFAA-4F22-9833-400D5E450501', '7D029238-616B-408E-981D-E9E7AB6B7F62']
            }
            , use_default_mapping=True)

    #积分商城要用的 收费性质, 购买课程者自己本人购买的时候需要加积分的收费性质限定
    @property
    def ERPCustTypeForIntorducerList(self):
        return cb.get_value_from_env_data_dict(
            {
              "qa":  ['109AACAE-B174-40AA-9042-58CF05154FA6','FD25CBA2-BE8B-414D-A38B-4389C5B7361F'],
              "dev": ['109AACAE-B174-40AA-9042-58CF05154FA6','FD25CBA2-BE8B-414D-A38B-4389C5B7361F'],
              "online": ['109AACAE-B174-40AA-9042-58CF05154FA6','FD25CBA2-BE8B-414D-A38B-4389C5B7361F']
            }
            , use_default_mapping=True)

    #积分商城要用的，招商渠道类型中的转介绍REF的ID,对应		tSaleMode 表中的cParentID字段 或 cSaleMode字段
    @property
    def ERPSaleModeREFId(self):
        return cb.get_value_from_env_data_dict(
            {
              "qa":  'A0D6D64E-8018-4766-82A3-1A41578A7F38',
              "dev": 'A0D6D64E-8018-4766-82A3-1A41578A7F38',
              "online": 'A0D6D64E-8018-4766-82A3-1A41578A7F38',
            }
            )

   # 积分商城要用的特定物品ID号，只有购买这种特定物品的人，才能获得积分，或作为介绍人获得积分
    @property
    def ERPGoodsIDList(self):
        return cb.get_value_from_env_data_dict({
            "qa": ['C7637F13-EE5E-4FAE-9995-551335E2AFE3','C7637F13-EE5E-4FAE-9995-551335E2AFE3'],
            "dev":['C7637F13-EE5E-4FAE-9995-551335E2AFE3','C7637F13-EE5E-4FAE-9995-551335E2AFE3'],
            "online": ['C7637F13-EE5E-4FAE-9995-551335E2AFE3','C7637F13-EE5E-4FAE-9995-551335E2AFE3']})


    @property
    # leads表格七牛地址
    def qiniuLeadsExcel(self):
        return 'http://filetest.learningbee.net/auto/77e0122625d711e99aecacde48001122.xlsx'


    #APP跟进、leads报表要用的，表示市场部的部门ID
    @property
    def ERPTMKDeptId(self):
        return cb.get_value_from_env_data_dict(
            {
              "qa":  '75AC8F24-A957-4F96-8019-1FF724B762E4',
              "dev": '75AC8F24-A957-4F96-8019-1FF724B762E4',
              "online": '75AC8F24-A957-4F96-8019-1FF724B762E4',
            }
            )

    #APP成功状态ID
    @property
    def ERPAppNewStatusId(self):
        return cb.get_value_from_env_data_dict(
            {
              "qa":  '27008BEA-02D0-46BD-8B67-557FBA860DCB',
              "dev": '27008BEA-02D0-46BD-8B67-557FBA860DCB',
              "online": '27008BEA-02D0-46BD-8B67-557FBA860DCB',
            }
            )

    #公司ID
    @property
    def ERPCompanyId(self):
        return cb.get_value_from_env_data_dict(
            {
              "qa":  'F884DE90-F18D-419F-BE5B-AB7A2432ED9C',
              "dev": 'F884DE90-F18D-419F-BE5B-AB7A2432ED9C',
              "online": 'F884DE90-F18D-419F-BE5B-AB7A2432ED9C',
            }
            )

    #二级渠道ID
    @property
    def ERPSaleModeId(self):
        return cb.get_value_from_env_data_dict(
            {
              "qa":  '8FC627B6-51BD-4038-98E4-CC3AADA53492',
              "dev": '8FC627B6-51BD-4038-98E4-CC3AADA53492',
              "online": '8FC627B6-51BD-4038-98E4-CC3AADA53492',
            }
            )

    #一级渠道ID
    @property
    def ERPSaleModeTypeId(self):
        return cb.get_value_from_env_data_dict(
            {
              "qa":  'FBE4B6F5-E5C9-4D36-BBB2-F31EE975F076',
              "dev": 'FBE4B6F5-E5C9-4D36-BBB2-F31EE975F076',
              "online": 'FBE4B6F5-E5C9-4D36-BBB2-F31EE975F076',
            }
            )

    #员工ID(employeeId)
    @property
    def ERPEmployeeId(self):
        return cb.get_value_from_env_data_dict(
            {
              "qa":  'F7AF5C55-D3D2-426D-96C5-04455F49A7A3',# 技术部倪晓男员工账号
              "dev": 'F7AF5C55-D3D2-426D-96C5-04455F49A7A3',
              "online": 'F7AF5C55-D3D2-426D-96C5-04455F49A7A3',
            },use_default_mapping=True
            )

erpData = erpData()