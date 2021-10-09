# -*- coding: cp936 -*-
# coding = utf8
import logging,datetime,time
from common import dbService
from testconfig import config

logger = logging.getLogger(__name__)

'''
get all sale class list
@return list saleClassList
'''
def GetTypeGuidBySystypeGuid(dic_type,Sys_dic_guidList):
    logger.info("get all typeguid list...")
    in_p = ', '.join(list(map(lambda x: '%s', Sys_dic_guidList)))
    ALLCompanyTypeGuidList = []
    conn = dbService.connectMySqlServerDb(config['dbbaseServerHost'],config['basedbName'],config['dbUser'],config['dbPassword'])
    cursor = dbService.getCursor(conn)
    query = '''SELECT
                    dic_guid 
                FROM
                    base_information_relation 
                WHERE dic_type= '%s' and sys_dic_guid in (%s) ''' %(dic_type,in_p)
    cursor.execute(query,tuple(Sys_dic_guidList))
    rows =cursor.fetchall()

    for row in rows:
        ALLCompanyTypeGuidList.append(row[0])

    dbService.closeDbConn(conn)
    return ALLCompanyTypeGuidList




def GetSysGuidListBySystype(dic_type):
    logger.info("get all sys_dic_guid list...")
    sysGuidinfo = {}
    conn = dbService.connectMySqlServerDb(config['dbbaseServerHost'],config['basedbName'],config['dbUser'],config['dbPassword'])
    cursor = dbService.getCursor(conn)
    query = '''SELECT
                    distinct sys_dic_guid,dic_value
                FROM
                    base_information_relation 
                WHERE dic_type= '%s' and sys_dic_guid <>'' ''' %(dic_type)
    cursor.execute(query)
    rows =cursor.fetchall()

    for row in rows:
        if row[0] not in sysGuidinfo.keys():
            sysGuidinfo[row[0]]=[row[1]]
        else:
           sysGuidinfo[row[0]].append(row[1])

    dbService.closeDbConn(conn)
    return sysGuidinfo

def GetChargeData(dic_type):
    logger.info("get 成才类cCategory的信息...")
    sysGuidinfo = {}
    conn = dbService.connectMySqlServerDb(config['dbbaseServerHost'], config['basedbName'], config['dbUser'],
                                        config['dbPassword'])
    cursor = conn.cursor()
    query = ''' select DISTINCT a.sys_dic_guid,a.dic_guid,a.dic_Value from base_information_relation a
                left join sys_dic b on a.sys_dic_guid = b.dic_key WHERE b.Type='CHENG_CAI_KE_CHENG' AND a.dic_type ='%s' '''  %(dic_type)
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        if row[0] not in sysGuidinfo.keys():
            sysGuidinfo[row[0]]=[row[1]]
        else:
           sysGuidinfo[row[0]].append(row[1])
    dbService.closeDbConn(conn)
    return sysGuidinfo

#根据sys_dic_guid查询dic_guid
def GetDicGuidBySysdicGuid(Sys_dic_guidList):
    logger.info("根据sysdicguidList查课程dic_guid...")
    in_p = ', '.join(list(map(lambda x: '%s', Sys_dic_guidList)))
    tmplist=[]
    conn = dbService.connectMySqlServerDb(config['dbbaseServerHost'], config['basedbName'], config['dbUser'],
                                        config['dbPassword'])
    cursor = conn.cursor()
    query = ''' select DISTINCT a.dic_guid,a.dic_Value from base_information_relation a
                WHERE a.sys_dic_guid in(%s) '''  %(in_p)
    cursor.execute(query,tuple(Sys_dic_guidList))
    rows = cursor.fetchall()
    for row in rows:
        tmplist.append(row[0])
    dbService.closeDbConn(conn)
    return tmplist