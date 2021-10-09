# -*- coding: cp936 -*-
# coding = utf8
# by zgf
#所有查询线下ERP数据库，也就是sql server数据的方法在下面： create by typhoon 2018.11.
import logging,datetime,time
from common import dbService
from testconfig import config
from testdata.erpData import erpData

logger = logging.getLogger(__name__)

'''
get all sale class list
@return list saleClassList
'''
#----------------线下班级查看-转线上的留存数-对应的【线下班级】-开班/未开班的班级列表------------使用
#SQL还有错误，暂不调试
def GetOpenedErpClassByClassList(ERPClassIdStr,Opened):
    logger.info("get all ERPClass by erp class...")
    IdList = []
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['dbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    if Opened=='True':
         query = '''select (cClassId) from (select  min(cStartTime) firstTime,max(cEndTime) lastTime from tCourse where cFinished<>2 and cClassId in (%s) group by cClassId) c
         where c.firstTime <= NOW( ) and c.lastTime >=NOW( )''' % (ERPClassIdStr)
    else:
        query = '''select (distinct(cClassId)) from (select  min(cStartTime) firstTime,max(cEndTime) lastTime from tCourse where cFinished<>2 and cClassId in (%s) group by cClassId) c
            where c.firstTime > NOW( ) ''' % (ERPClassIdStr)
    cursor.execute(query)
    rows =cursor.fetchall()

    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)
    return IdList

def GetErpCampus(NotIncludeCampusId):
    logger.info("get all ERPCampus by erp class...")
    IdList = []
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['dbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    query = '''select  cID from tDepart where cisCampus=1 and cID not in (%s) ''' % (NotIncludeCampusId)
    cursor.execute(query)
    rows =cursor.fetchall()

    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)
    return IdList


#----------------查看线下班级的第一节课开始时间------------使用
def GetErpClassinfoByClassid(ERPClassId):
    logger.info("get all ERPClass by erp class...")
    IdList = []
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['dbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    query = '''select  top 1 cStartTime, cEndTime from tCourse where cFinished<>2 and cClassId ='%s' order by cStartTime ASC ''' % (ERPClassId)
    cursor.execute(query)
    rows =cursor.fetchall()

    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)
    return IdList

#----------------线下班级查看-线下已开班/未开班对应的学生，已转线上后的选班/未选班的人数------------使用
#查看线下合同表tFeeChargeRecords的收入/结转/退费的合同数量（含作废合同）
def GetFeeChargeCount(starttime,endtime,zeroflag,cflag,CampusIdList):
    logger.info("getReportContract by date...")
    IdList = []
    in_p = ', '.join(list(map(lambda x: '%s', CampusIdList)))
    if zeroflag=='F':
         query = '''SELECT count(*) FROM tFeeChargeRecords WHERE cCreateTime>='%s' AND cCreateTime<='%s' 
                 AND cFlag=%i and cPayFact<>0 And cCampusID in (%s)''' % (starttime,endtime,cflag,in_p)
    else:
        query = '''SELECT count(distinct(cID)) FROM tFeeChargeRecords WHERE cCreateTime>='%s' AND cCreateTime<='%s'
                AND cFlag=%i and cPayFact=0 And cCampusID in (%s)''' % (starttime, endtime, cflag,in_p)
    #获取直营校数据
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['dbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query,tuple(CampusIdList))
    rows =cursor.fetchall()

    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)

    # 获取加盟校数据
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['JMXdbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query,tuple(CampusIdList))
    rows =cursor.fetchall()

    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)

    return IdList[0]+IdList[1]

#查看线下合同表tFeeChargeRecords的作废合同）
def GetFeeChargeCountByStatus(starttime,endtime,cFlag,CampusIdList):
    logger.info("getReportContract by date...")
    IdList = []
    in_p = ', '.join(list(map(lambda x: '%s', CampusIdList)))
    if cFlag!=9: #取收入或结转或退费的合同数，具体根据cFlag的值判断
         query = '''SELECT count(*) FROM tFeeChargeRecords WHERE cUpdateTime>='%s' AND cUpdateTime<='%s' 
                 AND cStatus=0 AND  cFlag=%i  And cCampusID in (%s)''' % (starttime,endtime,cFlag,in_p)
    elif cFlag==9: #取包含收入+结转+退费的合同数
        query = '''SELECT count(*) FROM tFeeChargeRecords WHERE cUpdateTime>='%s' AND cUpdateTime<='%s'
                AND cStatus=0 And cCampusID in (%s)''' % (starttime, endtime,in_p)
    #获取直营校数据
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['dbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query,tuple(CampusIdList))
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)

    #获取加盟校数据
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['JMXdbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query,tuple(CampusIdList))
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)

    return IdList[0] +IdList[1]


#查看线下合同---异常合同汇总数，目前异常合同的定义是：1）交费日期在合同创建日期之前的所有记录，视为预警记录 2）
def GetExceptionContractCount(starttime,endtime,cTypeIdList,CampusIdList):
    logger.info("get ExceptionContractCount by date...")
    in_p = ', '.join(list(map(lambda x: '%s', cTypeIdList)))
    in_paramTypeid = ', '.join(list(map(lambda x: '%s', CampusIdList)))
    IdList = []
    query1 = '''SELECT count(*) FROM tFeeChargeRecords WHERE CONVERT(varchar(100), cDate, 23) < CONVERT(varchar(100), cCreateTime, 23) And cstatus=1
	AND cCreateTime>='%s' AND cCreateTime<='%s' AND cflag=1 AND cCampusID in (%s)''' % (starttime,endtime,in_p)

    query2 = '''SELECT
                a.cID,
                COUNT (DISTINCT b.cTypeID ) 
            FROM
                tFeeChargeRecords a
                LEFT JOIN tFeeChargeCustType b ON a.cID= b.cChargeID 
            WHERE
                a.cstatus= 1
                AND a.cCreateTime>='%s' AND a.cCreateTime<='%s' 
                AND a.cflag=1 
                AND a.cID NOT IN (
                                    SELECT
                                        cID 
                                    FROM
                                        tFeeChargeRecords 
                                    WHERE
                                        CONVERT ( VARCHAR ( 100 ), cDate, 23 ) < CONVERT ( VARCHAR ( 100 ), cCreateTime, 23 ) 
                                        AND cstatus = 1 
                                        AND cCreateTime>='%s' AND cCreateTime<='%s' 
                                    ) 
                AND b.cTypeID IN (%s) 
                AND a.cCampusID in (%s)                    
            GROUP BY
                a.cID 
            HAVING
                COUNT (DISTINCT b.cTypeID ) > 1 
            ''' % (starttime, endtime,starttime, endtime, in_paramTypeid,in_p)

    tmplist=cTypeIdList.copy()
    tmplist.extend(CampusIdList)

    #取直营校
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['dbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query1,tuple(CampusIdList))
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row[0])


    cursor.execute(query2,tuple(tmplist))
    cursor.fetchall()
    i=cursor.rowcount
   # i=len(result1)
    tmpcount=IdList[0]+i
    IdList[0]=tmpcount
    dbService.closeDbConn(conn)

    # 取加盟校
    conn = dbService.connectSqlServerDb(config['ERPdbServerHost'], config['ERPJMXdbName'], config['ERPdbUser'],
                                        config['ERPdbPassword'])
    cursor = conn.cursor()
    cursor.execute(query1, tuple(CampusIdList))
    rows = cursor.fetchall()
    for row in rows:
        IdList.append(row[0])

    cursor.execute(query2, tuple(tmplist))
    cursor.fetchall()
    i = cursor.rowcount
    # i=len(result1)
    tmpcount = IdList[1] + i
    IdList[1] = tmpcount
    dbService.closeDbConn(conn)

    return IdList[0] + IdList[1]


#查看线下合同--按不同收费方式的收费金额  #2019-06-11 获取金额时去掉结转的金额
def GetPayMoneyByPayChannel(starttime,endtime,CampusidList):
    logger.info("get PayMoney by date...")
    IdList = []
    in_paramCampusidList=', '.join(list(map(lambda x: '%s', CampusidList)))
    query_add = '''SELECT isnull(sum(b.cMoney),0) FROM tFeeChargeRecords a 
               LEFT JOIN tFeeChargeMode b ON a.cID=b.cChargeID 
               WHERE b.cCreateTime>='%s' AND b.cCreateTime<='%s' AND b.cName <>'电子钱包' And a.cflag<>0 
               AND a.cCampusID in (%s) ''' % (starttime,endtime,in_paramCampusidList)
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['dbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query_add,tuple(CampusidList)) #统计当天创建的所有记录的收费 + 退费的总额；
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row[0])

    query_del = '''SELECT isnull(sum(b.cMoney),0) FROM tFeeChargeRecords a 
               LEFT JOIN tFeeChargeMode b ON a.cID=b.cChargeID 
               WHERE a.cUpdateTime>='%s' AND a.cUpdateTime<='%s' AND a.cstatus=0 And a.cflag<>0 AND b.cName<>'电子钱包' AND a.cCampusID in (%s)''' % (starttime,endtime,in_paramCampusidList)
    cursor.execute(query_del,tuple(CampusidList)) #统计当天更新的作废总额
    rows = cursor.fetchall()
    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)

    #取加盟校
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['JMXdbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query_add,tuple(CampusidList)) #统计当天创建的所有记录的收费 + 退费的总额；
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row[0])

    cursor.execute(query_del,tuple(CampusidList)) #统计当天更新的作废总额
    rows = cursor.fetchall()
    for row in rows:
        IdList.append(row[0])

    return IdList #返回的第一个值是所有今天创建的收费+结转 + 退费的金额（不含作废的），第二个是所有今天作废的金额；第三、四是同样，只是加盟校的数据

#查看线下合同---线下合同-传入指定付费方式来获取这种付费下的修正金额  #2019-06-11 获取作废金额时去掉结转的金额
def GetAccChargePayChannelByCampusId(starttime,endtime,cFlag,cStatus,payChannelList,CampusidList):
    logger.info("get getAccChargePayChannel by date...")
    in_parampayChannelList=', '.join(list(map(lambda x: '%s', payChannelList)))
    in_paramCampusidList = ', '.join(list(map(lambda x: '%s', CampusidList)))
    IdList = []
    if cStatus==None: #有效记录
        query = '''SELECT b.cName,isnull(sum(b.cMoney),0),count(0) FROM tFeeChargeRecords a 
                    LEFT JOIN tFeeChargeMode b ON a.cID=b.cChargeID 
                    WHERE a.cDate>='%s' AND a.cDate<='%s' AND a.cflag=%i  And b.cName in (%s) And b.cMoney<>0
                    AND a.cCampusID in(%s) GROUP BY b.cName ''' % (starttime, endtime, cFlag, in_parampayChannelList,in_paramCampusidList)

    else:  #取作废记录
        query = '''SELECT b.cName,isnull(sum(b.cMoney),0),count(0) FROM tFeeChargeRecords a 
                   LEFT JOIN tFeeChargeMode b ON a.cID=b.cChargeID 
                   WHERE a.cUpdateTime>='%s' AND a.cUpdateTime<='%s' AND a.cStatus=%i And a.cflag<>0 And b.cName in (%s) And b.cMoney<>0
                   AND  a.cCampusID in(%s) GROUP BY b.cName ''' % (starttime, endtime,cStatus, in_parampayChannelList,in_paramCampusidList) #按渠道区分获取作废的数据

    tmplist = payChannelList.copy()
    tmplist.extend(CampusidList)
  #取直营校
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['dbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query,tuple(tmplist))
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(list(row))
        IdList.append(list(row))
    dbService.closeDbConn(conn)

    #取加盟校
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['JMXdbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query,tuple(tmplist))
    rows =cursor.fetchall()
    for row in rows:
        if IdList==[]:
            IdList.append(list(row))
        else:
            IdList[0][1]=IdList[0][1]+row[1]
            IdList[0][2]=IdList[0][2]+row[2]
    dbService.closeDbConn(conn)

    return IdList



#查看线下合同---汇总某种支付方式的收入金额，条件是按tFeeChargeMode中的创建时间段来统计  #2019-06-11 获取作废金额时去掉结转的金额
def GetIncomeTatolByPayChannel(starttime,endtime,payChannelList,cFlag,cStatus,CampusidList):
    logger.info("get IncomeTatol by date...")
    in_parampayChannelList=', '.join(list(map(lambda x: '%s', payChannelList)))
    in_paramCampusidList=', '.join(list(map(lambda x: '%s', CampusidList)))
    IdList = []
    if cStatus==None:
        if payChannelList==[]:
            query = '''SELECT isnull(sum(b.cMoney),0),count(0) FROM tFeeChargeRecords a 
                        LEFT JOIN tFeeChargeMode b ON a.cID=b.cChargeID 
                        WHERE b.cCreateTime>='%s' AND b.cCreateTime<='%s' AND a.cflag=%i  And b.cName<>'电子钱包' And b.cMoney<>0
                        AND a.cCampusID in (%s)''' % (starttime, endtime, cFlag, in_paramCampusidList)

        else:
            query = '''SELECT isnull(sum(b.cMoney),0),count(0) FROM tFeeChargeRecords a 
                       LEFT JOIN tFeeChargeMode b ON a.cID=b.cChargeID 
                       WHERE b.cCreateTime>='%s' AND b.cCreateTime<='%s'  AND a.cflag=%i And b.cMoney<>0 AND b.cName in(%s)
                       AND a.cCampusID in (%s)''' % (starttime, endtime, cFlag,in_parampayChannelList, in_paramCampusidList)
    else:
        if payChannelList==[]:
            query = '''SELECT isnull(sum(b.cMoney),0),count(0) FROM tFeeChargeRecords a 
                       LEFT JOIN tFeeChargeMode b ON a.cID=b.cChargeID 
                       WHERE a.cUpdateTime>='%s' AND a.cUpdateTime<='%s' AND a.cStatus=%i And a.cflag<>0 And b.cName<>'电子钱包' And b.cMoney<>0
                       AND a.cCampusID in (%s)''' % (starttime, endtime,cStatus, in_paramCampusidList) #按渠道区分获取作废的数据
        else:
            query = '''SELECT isnull(sum(b.cMoney),0),count(0) FROM tFeeChargeRecords a 
                       LEFT JOIN tFeeChargeMode b ON a.cID=b.cChargeID 
                       WHERE a.cUpdateTime>='%s' AND a.cUpdateTime<='%s'  AND a.cStatus=%i And a.cflag<>0  And b.cMoney<>0 AND b.cName in(%s)
                       AND a.cCampusID in (%s)''' % (starttime, endtime, cStatus, in_parampayChannelList,in_paramCampusidList) #获取所有渠道作废的数据
    if payChannelList == []:
        tmplist = CampusidList.copy()
    else:
        tmplist = payChannelList.copy()
        tmplist.extend(CampusidList)

    #取直营校
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['dbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query,tuple(tmplist))
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row)
    dbService.closeDbConn(conn)

    #取加盟校
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['JMXdbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query,tuple(tmplist))
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row)
    dbService.closeDbConn(conn)

    return IdList


#查看线下合同---汇总某种支付方式的修正金额  2019-06-11 作废金额取值，去掉结转的作废
def GetAccIncomeTatolByPayChannel(starttime,endtime,payChannelList,cFlag,cStatus,CampusidList):
    logger.info("get AccIncomeTatol by date...")
    IdList = []
    in_parampayChannelList = ', '.join(list(map(lambda x: '%s', payChannelList)))
    in_paramCampusidList = ', '.join(list(map(lambda x: '%s', CampusidList)))
    if cStatus==None:
        if payChannelList==[]:#表示查看所有的支付方式，此时应该去掉电子钱包的值
            query = '''SELECT isnull(sum(b.cMoney),0),count(0) FROM tFeeChargeRecords a 
                        LEFT JOIN tFeeChargeMode b ON a.cID=b.cChargeID 
                        WHERE a.cDate>='%s' AND a.cDate<='%s' AND a.cflag=%i  And b.cName<>'电子钱包' And b.cMoney<>0
                        AND a.cCampusID in (%s)''' % (starttime, endtime, cFlag, in_paramCampusidList)

        else:
            query = '''SELECT isnull(sum(b.cMoney),0),count(0) FROM tFeeChargeRecords a 
                       right JOIN tFeeChargeMode b ON a.cID=b.cChargeID 
                       WHERE a.cDate>='%s' AND a.cDate<='%s'  AND a.cflag=%i And b.cMoney<>0 AND b.cName in(%s)
                       AND a.cCampusID in (%s)''' % (starttime, endtime, cFlag,in_parampayChannelList, in_paramCampusidList)
    else:
        if payChannelList==[]:
            query = '''SELECT isnull(sum(b.cMoney),0),count(0) FROM tFeeChargeRecords a 
                       LEFT JOIN tFeeChargeMode b ON a.cID=b.cChargeID 
                       WHERE a.cUpdateTime>='%s' AND a.cUpdateTime<='%s' AND a.cStatus=%i AND a.cflag<>0 And b.cName<>'电子钱包' And b.cMoney<>0
                       AND a.cCampusID in (%s)''' % (starttime, endtime,cStatus, in_paramCampusidList) #按渠道区分获取作废的数据
        else:
            query = '''SELECT isnull(sum(b.cMoney),0),count(0) FROM tFeeChargeRecords a 
                       LEFT JOIN tFeeChargeMode b ON a.cID=b.cChargeID 
                       WHERE a.cUpdateTime>='%s' AND a.cUpdateTime<='%s'  AND a.cStatus=%i AND a.cflag<>0 And b.cMoney<>0 AND b.cName in (%s)
                       AND a.cCampusID in (%s)''' % (starttime, endtime,cStatus,in_parampayChannelList, in_paramCampusidList) #获取所有渠道作废的数据
    if payChannelList==[]:
        tmplist = CampusidList.copy()
    else:
        tmplist = payChannelList.copy()
        tmplist.extend(CampusidList)

    #获取直营
    conn =  dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'], erpData.ErpOnlineDb['dbName'],
                                            erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query,tuple(tmplist))
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row)
    dbService.closeDbConn(conn)

    #获取加盟校
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'], erpData.ErpOnlineDb['JMXdbName'],
                                            erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query,tuple(tmplist))
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row)
    dbService.closeDbConn(conn)
    return IdList


#查看线下合同--获取时间段内的合同类型
def GetcTypeIDByDate(starttime,endtime,NotIncludeCampusId):
    logger.info("get cTypeID by date...")
    typeIdSet = set()
    query = '''SELECT distinct b.cTypeID FROM tFeeChargeRecords a 
               LEFT JOIN tFeeChargeCustType b ON a.cID= b.cChargeID
               WHERE  a.cstatus=1 AND a.cCreateTime>='%s' AND a.cCreateTime<='%s' And a.cpayFact>0 
               AND a.cCampusID not in (%s)''' % (starttime,endtime,NotIncludeCampusId)
    # 取直营
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['dbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query)
    rows =cursor.fetchall()
    for row in rows:
        typeIdSet.add(row[0])
    dbService.closeDbConn(conn)

    #取加盟的typeid
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['JMXdbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query)
    rows =cursor.fetchall()
    for row in rows:
        typeIdSet.add(row[0]) #采用集合来保存不重复元素序列，若是元素已经存在，则不进行任何操作
    dbService.closeDbConn(conn)
    return list(typeIdSet)

#查看线下合同-依据这段时间的线下合同类型，查找关联的合同数
def GetChargeCountByDateAndTypeID(starttime,endtime,cTypeIdlist,CampusIdList):
    logger.info("get chargeCount by date...")
    in_paramTypeid= ', '.join(list(map(lambda x: '%s', cTypeIdlist)))
    in_paramCampus = ', '.join(list(map(lambda x: '%s', CampusIdList)))
    IdList = []

    tmplist =cTypeIdlist.copy()  #为了传query值
    tmplist.extend(CampusIdList)

    query = '''SELECT isnull( SUM ( a.cPayFact ), 0 ),count(distinct(a.cID)) FROM tFeeChargeRecords a LEFT JOIN tFeeChargeCustType b ON a.cID= b.cChargeID
               WHERE  a.cstatus=1 AND a.cCreateTime>='%s' AND a.cCreateTime<='%s' And a.cpayFact>0 And lower(b.cTypeID) in (%s)
               AND a.cCampusID in (%s)''' % (starttime,endtime,in_paramTypeid,in_paramCampus)
    #获取直营
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['dbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query,tuple(tmplist))
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row)
    dbService.closeDbConn(conn)

    #获取加盟
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['JMXdbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query,tuple(tmplist))
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row)
    dbService.closeDbConn(conn)
    return IdList


#查看线下合同-依据这段时间的线下合同类型，查找关联的合同人数
def GetStudentCountByDateAndTypeID(starttime,endtime,cTypeIdlist,CampusIdList):
    logger.info("get cStudentUserCount by date...")
    in_paramTypeid= ', '.join(list(map(lambda x: '%s', cTypeIdlist)))
    in_paramCampus = ', '.join(list(map(lambda x: '%s', CampusIdList)))
    IdList = []

    tmplist =cTypeIdlist.copy()  #为了传query值
    tmplist.extend(CampusIdList)

    query = '''SELECT count(distinct(a.cStudentUserID)) FROM tFeeChargeRecords a LEFT JOIN tFeeChargeCustType b ON a.cID= b.cChargeID
               WHERE  a.cstatus=1 AND a.cCreateTime>='%s' AND a.cCreateTime<='%s' And a.cpayFact>0 And lower(b.cTypeID) in(%s)
               AND a.cCampusID in (%s)''' % (starttime,endtime,in_paramTypeid,in_paramCampus)
    # 获取直营
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['dbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query,tuple(tmplist))
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)

    # 获取加盟
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['JMXdbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query,tuple(tmplist))
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)
    return IdList[0] +IdList[1]

#-------------以下是收费项目的财务报表-----------#


#收费项目-获取指定时间内的合同对应的课程的实际收费 #2019-06-11 去掉结转的金额
def GetChargingShiftCountByDateAndChargeIds(starttime,endtime,cFlag,cStatus,cChargeIdsList,CampusIdList):
    logger.info("get ChargingItemCount by date...")
    IdList = []
    in_p = ', '.join(list(map(lambda x: '%s', cChargeIdsList)))
    in_paramCampus=', '.join(list(map(lambda x: '%s', CampusIdList)))

    if cStatus==None:
        query = ''' SELECT isnull(SUM (a.cTotalMoney),0),Count(0) FROM tFeeChargeShift a LEFT JOIN tFeeChargeRecords b ON a.cChargeID= b.cID 
                    WHERE a.cCreateTime >= '%s' AND a.cCreateTime <= '%s' AND b.cflag=%i and b.cflag<>0
                        AND a.cShiftID IN (SELECT DISTINCT cID FROM tShift WHERE cCategory in (%s))  
                        AND a.cCampusID in (%s)'''  % (starttime,endtime,cFlag,in_p,in_paramCampus)


    else:
        query = ''' SELECT isnull(SUM (a.cTotalMoney),0),Count(0) FROM tFeeChargeShift a LEFT JOIN tFeeChargeRecords b ON a.cChargeID= b.cID 
                    WHERE b.cUpdateTime >= '%s' AND b.cUpdateTime <= '%s' AND b.cStatus=%i and b.cflag<>0
                        AND a.cShiftID IN (SELECT DISTINCT cID FROM tShift WHERE cCategory in (%s))  
                        AND a.cCampusID in (%s)'''  % (starttime,endtime,cStatus,in_p,in_paramCampus)
    tmplist=cChargeIdsList.copy()
    tmplist.extend(CampusIdList)

    try:
        #获取直营
        conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['dbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
        cursor = conn.cursor()
        cursor.execute(query, tuple(tmplist)) #特殊的SQL中带了in，in在一个lIST中的写法
        rows =cursor.fetchall()
        for row in rows:
            IdList.append(row)
        dbService.closeDbConn(conn)

        #获取加盟
        conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['JMXdbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
        cursor = conn.cursor()
        cursor.execute(query,tuple(tmplist))
        rows =cursor.fetchall()
        for row in rows:
            IdList.append(row)
        dbService.closeDbConn(conn)
    except:
        print("dicGUID为:"+str(cChargeIdsList)+"校区为:"+str(CampusIdList))
    return IdList


#收费项目-获取指定时间内的合同对应的物品的实际收费 #2019-06-11 去掉结转的金额
def GetChargingGoodCountByDateAndChargeIds(starttime,endtime,cFlag,cStatus,cGoodsTypeList,CampusIdList):
    logger.info("get ChargingGoodCount by date...")
    IdList = []
    in_p = ', '.join(list(map(lambda x: '%s', cGoodsTypeList)))
    in_paramCampus=', '.join(list(map(lambda x: '%s', CampusIdList)))

    if cStatus==None:
        query = ''' SELECT isnull(SUM (a.cTotalMoney),0),Count(0) FROM tFeeChargeGoods a LEFT JOIN tFeeChargeRecords b ON a.cChargeID= b.cID 
                    WHERE a.cCreateTime >= '%s' AND a.cCreateTime <= '%s' AND b.cflag=%i 
                        AND a.cGoodsID IN (SELECT DISTINCT cID FROM tGoods WHERE cGoodsTypeID in (%s))  
                        AND b.cCampusID in (%s)'''  % (starttime,endtime,cFlag,in_p ,in_paramCampus)

    else:
        query = ''' SELECT isnull(SUM (a.cTotalMoney),0),Count(0) FROM tFeeChargeGoods a LEFT JOIN tFeeChargeRecords b ON a.cChargeID= b.cID 
                    WHERE b.cUpdateTime >= '%s' AND b.cUpdateTime <= '%s' AND b.cStatus=%i AND b.cflag<>0
                        AND a.cGoodsID IN (SELECT DISTINCT cID FROM tGoods WHERE cGoodsTypeID in (%s))  
                        AND b.cCampusID in (%s)'''  % (starttime,endtime,cStatus,in_p,in_paramCampus)
    tmplist=cGoodsTypeList.copy()
    tmplist.extend(CampusIdList)
    #取直营
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['dbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query, tuple(tmplist)) #特殊的SQL中带了in，in在一个lIST中的写法
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row)
    dbService.closeDbConn(conn)

    #取加盟校
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['JMXdbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query, tuple(tmplist)) #特殊的SQL中带了in，in在一个lIST中的写法
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row)
    dbService.closeDbConn(conn)
    return IdList



#查看线下合同-依据这段时间的线下合同类型，查找预存（prestore）金额 #2019-06-11修改：所有的数据不包含结转的金额
def GetChargePrestoreAmountByDateAndTypeID(starttime,endtime,cFlag,cStatus,CampusIdList):
    logger.info("get chargeCount by date...")
    in_paramCampus=', '.join(list(map(lambda x: '%s', CampusIdList)))
    IdList = []
    if cStatus == None:
        query = '''SELECT isnull(SUM (a.cPayFactSub),0),Count(0)  FROM tFeeChargeShift a 
                   LEFT JOIN tFeeChargeCustType b ON a.cChargeID= b.cChargeID
                   LEFT JOIN tFeeChargeRecords c ON a.cChargeID= c.cID
                   WHERE a.cshiftId='00000000-0000-0000-0000-000000000000' AND c.cCreateTime>='%s' AND c.cCreateTime<='%s' and c.cflag=%i
                   AND c.cflag<>0  
                   And b.cTypeID in (select cID from tDictionary WHERE cValue = '%s')
                   AND a.cCampusID in (%s) ''' % (starttime,endtime,cFlag,'预存',in_paramCampus)
    else:
        query = '''SELECT isnull(SUM (a.cPayFactSub),0),Count(0)  FROM tFeeChargeShift a 
                   LEFT JOIN tFeeChargeCustType b ON a.cChargeID= b.cChargeID
                   LEFT JOIN tFeeChargeRecords c ON a.cChargeID= c.cID 
                   WHERE  a.cshiftId='00000000-0000-0000-0000-000000000000' AND c.cUpdateTime>='%s' AND c.cUpdateTime<='%s' And c.cStatus=%i
                   And b.cTypeID in (select cID from tDictionary WHERE cValue =   '%s') AND c.cflag<>0  
                   AND a.cCampusID in (%s) ''' % (starttime,endtime,cStatus,'预存',in_paramCampus)
   #取直营
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['dbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query,tuple(CampusIdList))
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)

    #取加盟校
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['JMXdbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query,tuple(CampusIdList))
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)
    return IdList[0]+IdList[1]

#2019-06-11 获取作废金额时去掉结转的金额
#查看线下合同-依据这段时间的线下合同的购买项目中，属于"新增"类型的收费笔数：
# 比如一个合同里面有3个购买项目，其中2门课程，1个是物品，那么这里统计的是传入cCategory类型的课程这段时间内的属于"新增"收费类型的笔数）
#1条合同记录，2条tFeeChargeShift记录（收费类型分别属于新增和扩科收费类型，那么tFeeChargeCustType中会有2条记录1条新增，1条是扩科），1条tFeeChargeGoods物品记录
def GetChargeCountMoneyByDateAndCategoryAndTypeID(starttime,endtime,cTypeIdList,cChargeIdsList,cCampustList):
    logger.info("get chargeCount by date...")
    in_paramcTypeIds = ', '.join(list(map(lambda x: '%s', cTypeIdList)))
    in_paramChargeIds = ', '.join(list(map(lambda x: '%s', cChargeIdsList)))
    in_paramCampus = ', '.join(list(map(lambda x: '%s', cCampustList)))
    IdList = []
    query = ''' SELECT isnull(SUM (a.cTotalMoney),0),count(distinct(a.cID)) FROM tFeeChargeShift a 
                    LEFT JOIN tFeeChargeRecords b ON a.cChargeID= b.cID
                    LEFT JOIN tFeeChargeCustType c ON a.cChargeID= c.cChargeID and c.cChargeSubID=a.cID
                    WHERE b.cStatus=1 and b.cflag<>0 And a.cTotalMoney>0
                    AND a.cCreateTime >= '%s' AND a.cCreateTime <= '%s' And UPPER(c.cTypeID) in(%s)
                    AND a.cShiftID IN (SELECT DISTINCT cID FROM tShift WHERE cCategory in(%s))  
                    AND a.cCampusID in (%s)''' % (starttime, endtime, in_paramcTypeIds,in_paramChargeIds, in_paramCampus)
    tmplist=cTypeIdList.copy()
    tmplist.extend(cChargeIdsList)
    tmplist.extend(cCampustList)
    #直营
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['dbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query,tuple(tmplist))
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row)
    dbService.closeDbConn(conn)

    #加盟
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'], erpData.ErpOnlineDb['JMXdbName'],
                                        erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query, tuple(tmplist))
    rows = cursor.fetchall()
    for row in rows:
        IdList.append(row)
    dbService.closeDbConn(conn)

    return IdList

#2019-06-11 获取作废金额时去掉结转的金额
#查看线下合同-依据这段时间的线下合同的购买项目中，属于"新增"类型的收费笔数：
# 比如一个合同里面有3个购买项目，其中2门课程，1个是物品，那么这里统计的是传入cCategory类型的课程这段时间内的属于"新增"收费类型的笔数）
#1条合同记录，2条tFeeChargeShift记录（收费类型分别属于新增和扩科收费类型，那么tFeeChargeCustType中会有2条记录1条新增，1条是扩科），1条tFeeChargeGoods物品记录
def GetStudentCountByDateAndCategoryAndTypeID(starttime,endtime,cTypeIdList,cChargeIdsList,cCampustList):
    logger.info("get cStudentUserCount by date...")
    IdList = []
    in_paramcTypeIds = ', '.join(list(map(lambda x: '%s', cTypeIdList)))
    in_paramChargeIds = ', '.join(list(map(lambda x: '%s', cChargeIdsList)))
    in_paramCampus = ', '.join(list(map(lambda x: '%s', cCampustList)))
    query = ''' SELECT count(distinct(a.cStudentUserID)) FROM tFeeChargeShift a 
                  LEFT JOIN tFeeChargeRecords b ON a.cChargeID= b.cID
                  LEFT JOIN tFeeChargeCustType c ON a.cChargeID= c.cChargeID and c.cChargeSubID=a.cID
                  WHERE b.cStatus=1 And  b.cflag<>0 and a.cTotalMoney>0 
                  AND a.cCreateTime >= '%s' AND a.cCreateTime <= '%s' And UPPER(c.cTypeID) in(%s)
                  AND a.cShiftID IN (SELECT DISTINCT cID FROM tShift WHERE cCategory in(%s))  
                  AND a.cCampusID in(%s)''' % (starttime, endtime, in_paramcTypeIds, in_paramChargeIds, in_paramCampus)
    tmplist=cTypeIdList.copy()
    tmplist.extend(cChargeIdsList)
    tmplist.extend(cCampustList)
    #直营
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['dbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query,tuple(tmplist))
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)

    #加盟
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['JMXdbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query,tuple(tmplist))
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)
    return IdList[0] + IdList[1]


#查看线下合同--指定某个课程类型下获取时间段内的合同类型
def GetcTypeIDBycChargeIdsAndDate(starttime,endtime,cChargeIdsList,cCampustList):
    logger.info("get cTypeID by date...")
    IdList = []
    in_paramChargeIds = ', '.join(list(map(lambda x: '%s', cChargeIdsList)))
    in_paramCampus = ', '.join(list(map(lambda x: '%s', cCampustList)))
    tmplist=cChargeIdsList.copy()
    tmplist.extend(cCampustList)
    query='''SELECT DISTINCT b.cTypeID 
    FROM
	    tFeeChargeShift a
	LEFT JOIN tFeeChargeCustType b ON a.cID= b.cChargeSubID
    WHERE
        a.cstatus= 1 
        AND a.cCreateTime>= '%s' 
        AND a.cCreateTime<= '%s' 
        AND a.cTotalMoney> 0 
        AND a.cShiftID IN ( SELECT DISTINCT cID FROM tShift WHERE cCategory in(%s))
        AND a.cCampusID IN (%s) ''' % (starttime,endtime,in_paramChargeIds,in_paramCampus)
    # 获取直营
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['dbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query,tuple(tmplist))
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)

    # 获取加盟
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['JMXdbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query,tuple(tmplist))
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)
    return IdList


#查看线下的班级-成才类课程的班级数量和人员数量
def GetERPClassAndStudentCountGroupBycCategory(ReportDay,endtime,cCampustList,leverNameList):
    logger.info("get ClassAndStudentCount by date...")
    IdList = []
    in_paramCampus = ', '.join(list(map(lambda x: '%s', cCampustList)))
    in_paramLevel = ', '.join(list(map(lambda x: '%s', leverNameList)))
    ReportDay=str(ReportDay)+' 23:59:59' #不设置的话，会默认为00:00:00
    endtime=str(endtime)+' 23:59:59'
    query='''SELECT
                c.cID,
                c.cDescribe,
                count(distinct a.cClassID) ClassCount,
                count(distinct CAST(a.cClassID AS NVARCHAR(64))+CAST(d.cStudentUserID AS NVARCHAR(64))) StudentCount
             FROM
            (
            SELECT
                cClassID,
                cShiftID,
                MIN ( cStartTime ) firstTime,
                MAX ( cEndTime ) lastTime 
            FROM
                tCourse 
            WHERE
                cFinished <> 2 
            GROUP BY
                cClassId,cShiftID
            ) a
            LEFT JOIN tShift c on a.cShiftID = c.cID
            LEFT JOIN tClass b on a.cClassID=b.cID
            LEFT JOIN tClass_Student d on a.cClassID=d.cClassID and d.cStatus=1 and d.cInDate<='%s' And d.cOutDate>'%s'
            LEFT JOIN tClassroom e on b.cClassRoomID=e.cID
            WHERE
                (a.firstTime<='%s' AND a.lastTime>= '%s' and b.cIsFinished=0)
                and c.cCategory IN ( SELECT cID FROM tDictionary WHERE cValue LIKE '%%%s%%' ) 
                and e.cStatus=1
                and b.cCampusID in (%s)
                and c.cDescribe in (%s)
            GROUP BY
                    c.cID, c.cDescribe
                 ''' % (ReportDay,ReportDay,ReportDay,endtime,'成才',in_paramCampus,in_paramLevel)
    tmplist=cCampustList.copy()
    tmplist.extend(leverNameList)
    #查看直营
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['dbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query,tuple(tmplist))
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row)
    dbService.closeDbConn(conn)


    #查看加盟
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['JMXdbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query,tuple(tmplist))
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row)
    dbService.closeDbConn(conn)

    return IdList


#查看线下的班级-成才类课程的各班级对应的人数
def GetERPStudentCountGroupBycCategoryAndClass(ReportDay,endtime,cCampustList,leverNameList):
    logger.info("get StudentCount by date group by ...")
    IdList = []
    in_paramCampus = ', '.join(list(map(lambda x: '%s', cCampustList)))
    in_paramLevel = ', '.join(list(map(lambda x: '%s', leverNameList)))
    # 4月10号修改了新规则，SQL中原来的这个条件，要去掉： AND cClassId IN ( SELECT cClassID FROM tClass_Student WHERE cStatus = 1 )
    ReportDay=str(ReportDay)+' 23:59:59' #不设置的话，会默认为00:00:00
    endtime=str(endtime)+' 23:59:59'
    query='''SELECT distinct
                c.cID,
                c.cDescribe,
                a.cClassID,
                count(distinct CAST(a.cClassID AS NVARCHAR(64))+CAST(d.cStudentUserID AS NVARCHAR(64))) StudentCount,
                e.cPersonCount
             FROM
            (
            SELECT
                cClassID,
                cShiftID,
                MIN ( cStartTime ) firstTime,
                MAX ( cEndTime ) lastTime 
            FROM
                tCourse 
            WHERE
                cFinished <> 2 
            GROUP BY
                cClassId,cShiftID
            ) a
            LEFT JOIN tShift c on a.cShiftID = c.cID
            LEFT JOIN tClass b on a.cClassID=b.cID
            LEFT JOIN tClass_Student d on a.cClassID=d.cClassID  and d.cStatus=1 and d.cInDate<='%s' And d.cOutDate>='%s'
            LEFT JOIN tClassroom e on b.cClassRoomID=e.cID
            WHERE
                (a.firstTime<='%s' AND a.lastTime>= '%s' and b.cIsFinished=0)
                and c.cCategory IN ( SELECT cID FROM tDictionary WHERE cValue LIKE '%%%s%%' ) 
                and e.cPersonCount>=10 and e.cStatus=1
                and b.cCampusID in (%s)
                and c.cDescribe in (%s)
            GROUP BY
                    c.cID, c.cDescribe,a.cClassID,e.cPersonCount
                 ''' % (ReportDay,ReportDay,ReportDay,endtime,'成才',in_paramCampus,in_paramLevel)
    tmplist = cCampustList.copy()
    tmplist.extend(leverNameList)

    #取直营
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['dbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query,tuple(tmplist))
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row)
    dbService.closeDbConn(conn)

    #取加盟
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['JMXdbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query,tuple(tmplist))
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row)
    dbService.closeDbConn(conn)

    return IdList


#查看线下的班级-成才类课程的异常人员数量
def GetERPExceptClassAndStudentCountGroupBycCategory(ReportDay,endtime,cCampustList,leverNameList):
    ReportDay=str(ReportDay)+' 23:59:59' #不设置的话，会默认为00:00:00
    endtime=str(endtime)+' 23:59:59'
    logger.info("get ClassAndStudentCount by date...")
    tmpDic = {}
    in_paramCampus = ', '.join(list(map(lambda x: '%s', cCampustList)))
    in_paramLevel = ', '.join(list(map(lambda x: '%s', leverNameList)))
    query='''SELECT
                c.cID,
                c.cDescribe,
                count(distinct CAST(a.cClassID AS NVARCHAR(64))+CAST(d.cStudentUserID AS NVARCHAR(64))) StudentCount
             FROM
            (
            SELECT
                cClassID,
                cShiftID,
                MIN ( cStartTime ) firstTime,
                MAX ( cEndTime ) lastTime 
            FROM
                tCourse 
            WHERE
                cFinished <> 2 
            GROUP BY
                cClassId,cShiftID
            ) a
            LEFT JOIN tShift c on a.cShiftID = c.cID
            LEFT JOIN tClass b on a.cClassID=b.cID
            LEFT JOIN tClass_Student d on a.cClassID=d.cClassID and d.cStatus=1 and d.cInDate<='%s' And d.cOutDate>'%s'
            LEFT JOIN tClassroom e on b.cClassRoomID=e.cID
            WHERE
                (a.firstTime<='%s' AND a.lastTime>= '%s' and b.cIsFinished=0)
                and c.cCategory IN ( SELECT cID FROM tDictionary WHERE cValue LIKE '%%%s%%' ) 
                and e.cPersonCount<10 and e.cStatus=1
                and b.cCampusID in (%s)
                and c.cDescribe in (%s)
            GROUP BY
                    c.cID, c.cDescribe
                 ''' % (ReportDay,ReportDay,ReportDay,endtime,'成才',in_paramCampus,in_paramLevel)
    tmplist=cCampustList.copy()
    tmplist.extend(leverNameList)

    #取直营
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['dbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query,tuple(tmplist))
    rows =cursor.fetchall()
    for row in rows:
        tmpDic[row[1]]=row[2]
    dbService.closeDbConn(conn)

    #取加盟
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['JMXdbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query,tuple(tmplist))
    rows =cursor.fetchall()
    for row in rows:
        if row[1] not in tmpDic.keys():
            tmpDic[row[1]]=row[2]
        else:
            tmpDic[row[1]]=tmpDic[row[1]]+row[2]
    dbService.closeDbConn(conn)
    return tmpDic
###----------------------------以下是积分商城---------------------------#
#查看我应该获得的积分（我作为客户，未成为学员之前到店访问的次数 + 我作为介绍人，介绍其他学员到店体验我应该获得的积分）
def GetMyIntegralByisVisitStatus(starttime,endtime,tel,NotIncludeCampusId):
    logger.info("get MyIntegralByisVisitStatus...")
    IdList = []
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['dbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    query='''SELECT count(distinct a.cCustomerID)
             FROM
                 tCommunicationRecords a
             LEFT JOIN tStudentCustomer b ON a.cCustomerID=b.cID	
             WHERE
                 a.cIsVisit = 1 
                 AND a.cVisitDate >= '%s' 
                 AND a.cVisitDate <= '%s' 
                 AND b.cSMSTel= '%s'
                 AND b.cCampusID NOT IN (%s) ''' % (starttime,endtime,tel,NotIncludeCampusId)
    cursor.execute(query)  #获取手机号为"tel"的人，还没成为学员之前的某段时间内的到访次数
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row[0])

    query = '''SELECT
                    count(a.cCustomerID) 
                FROM
                    tCommunicationRecords a
                LEFT JOIN tStudentCustomer b ON a.cCustomerID=b.cID	
                LEFT JOIN tStudent c ON b.cIntroducer=c.cID	
                WHERE
                    a.cIsVisit = 1 
                    AND a.cVisitDate >= '%s' 
                    AND a.cVisitDate <= '%s' 
                    AND c.cSMSTel= '%s' AND b.cCampusID NOT IN (%s) ''' % ( starttime, endtime, tel, NotIncludeCampusId)
    cursor.execute(query)  #获取手机号为"tel"的人，作为介绍人的身份，在某段时间内介绍到店体验的人次 ，所以SQL中不能加distinct a.cCustomerID
    rows = cursor.fetchall()
    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)
    return IdList

#2019-6-14 增加校管家09全日制BD和07暑假班 的+积分功能
#2019-6-17 去掉测试校区的过滤，就是测试校区也可以查到
#查看我应该获得的积分（作为报名课程或介绍别人报名课程所获得的积分）
def GetMyIntegralByShiftAndTypeID(starttime,endtime,cstudentId,cTypeIdForMeList,cTypeIdForIntroducerList,ERPSaleModeREFId):
    logger.info("get MyIntegral by myShiftAndTypeID...")
    IdList = []
    in_p_typeidForMe = ', '.join(list(map(lambda x: '%s', cTypeIdForMeList)))
    in_p_typeidForIntroducer = ', '.join(list(map(lambda x: '%s', cTypeIdForIntroducerList)))
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['dbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    query='''SELECT
                a.cStudentUserID,
                a.cID,
                d.cTypeID
            FROM
                tFeeChargeShift a
                LEFT JOIN tFeeChargeRecords b ON a.cChargeID= b.cID
                LEFT JOIN tFeeChargeCustType d ON a.cID= d.cChargeSubID 
            WHERE
                a.cCreateTime>= '%s' 
                AND a.cCreateTime<= '%s' 
                AND b.cStatus= 1 
                AND b.cFlag= 1 AND a.cShiftID IN(SELECT DISTINCT
                                                    cID 
                                                FROM
                                                    tShift 
                                                WHERE
                                                cCategory IN ( SELECT cID FROM tDictionary WHERE (cValue LIKE '%%%s%%'  OR cValue in ('09-全日制BD','07-暑假班'))))
                AND cast(d.cTypeID as varchar(36)) IN (%s) AND a.cStudentUserID='%s'  
                and b.cID not in (select distinct cInChargeID from tclass_changeRecord) ''' % (starttime,endtime,'成才',in_p_typeidForMe,cstudentId)
    cursor.execute(query,tuple(cTypeIdForMeList))  #获取学生自己购买课程应该获得的积分
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row)

    query = '''SELECT
                    a.cStudentUserID,
                    a.cID,
                    d.cTypeID
                FROM
                    tFeeChargeShift a
                    LEFT JOIN tFeeChargeRecords b ON a.cChargeID= b.cID
                    LEFT JOIN tFeeChargeCustType d ON a.cID= d.cChargeSubID 
                WHERE
                    a.cCreateTime >= '%s' 
                    AND a.cCreateTime <= '%s' 
                    AND b.cStatus= 1 
                    AND b.cFlag= 1 
                    AND a.cShiftID IN (
                                    SELECT DISTINCT
                                        cID 
                                    FROM
                                        tShift 
                                    WHERE
                                    cCategory IN ( SELECT cID FROM tDictionary WHERE (cValue LIKE '%%%s%%' OR cValue in ('09-全日制BD','07-暑假班')) )) 
                    AND cast(d.cTypeID as varchar(36)) IN (%s)
                    AND a.cStudentUserID in (select cID from tStudent WHERE cIntroducer ='%s')
                    and a.cStudentUserID in (select cStudentID  FROM tStudentCustomer_SaleMode WHERE cSaleMode IN (
                    SELECT
                        cID 
                    FROM
                        tSaleMode 
                    WHERE
                    cParentID = '%s' 
                    ) OR (cSaleMode='%s')) AND  b.cID not in (select distinct cInChargeID from tclass_changeRecord) ''' % ( starttime, endtime, '成才',in_p_typeidForIntroducer,cstudentId,ERPSaleModeREFId,ERPSaleModeREFId)
    cursor.execute(query,tuple(cTypeIdForIntroducerList))  #作为介绍人，其被介绍的人在这段时间内购买的成才课程+ 招生意向表中的渠道来源为REF，此时介绍人要加积分
    rows = cursor.fetchall()
    for row in rows:
        IdList.append(row)
    dbService.closeDbConn(conn)
    return IdList

#查看我应该获得的积分（作为报名购买特定物品或介绍别人报名特定物品所获得的积分）
def GetMyIntegralByGoodsAndTypeID(starttime,endtime,cstudentId,cGoodsid,cTypeIdForMeList,cTypeIdForIntroducerList,ERPSaleModeREFId):
    logger.info("get MyIntegral by myGoodsAndTypeID...")
    IdList = []
    in_p_typeidForMe = ', '.join(list(map(lambda x: '%s', cTypeIdForMeList)))
    in_p_typeidForIntroducer = ', '.join(list(map(lambda x: '%s', cTypeIdForIntroducerList)))
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['dbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    query='''SELECT
                DISTINCT
                a.cStudentUserID,
                a.cID,
                d.cTypeID
            FROM
                tFeeChargeGoods a
                LEFT JOIN tFeeChargeRecords b ON a.cChargeID= b.cID
                LEFT JOIN tFeeChargeCustType d ON a.cID= d.cChargeSubID 
            WHERE
                a.cCreateTime>= '%s' 
                AND a.cCreateTime<= '%s' 
                AND b.cStatus= 1 
                AND b.cFlag= 1 AND a.cGoodsID ='%s' 
                AND cast(d.cTypeID as varchar(36)) IN (%s) AND a.cStudentUserID='%s' 
                and b.cID not in (select distinct cInChargeID from tclass_changeRecord) ''' % (starttime,endtime,cGoodsid,in_p_typeidForMe,cstudentId)
    cursor.execute(query,tuple(cTypeIdForMeList))  #获取学生自己购买课程应该获得的积分
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row)

    query = '''SELECT
                    DISTINCT
                    a.cStudentUserID,
                    a.cID,
                    d.cTypeID
                FROM
                    tFeeChargeGoods a
                    LEFT JOIN tFeeChargeRecords b ON a.cChargeID= b.cID
                    LEFT JOIN tFeeChargeCustType d ON a.cID= d.cChargeSubID 
                WHERE
                    a.cCreateTime >= '%s' 
                    AND a.cCreateTime <= '%s' 
                    AND b.cStatus= 1 
                    AND b.cFlag= 1 
                    AND a.cGoodsID ='%s' 
                    AND cast(d.cTypeID as varchar(36)) IN (%s)
                    AND a.cStudentUserID in (select cID from tStudent WHERE cIntroducer ='%s')
                    and a.cStudentUserID in (select cStudentID  FROM tStudentCustomer_SaleMode WHERE cSaleMode IN (
                    SELECT
                        cID 
                    FROM
                        tSaleMode 
                    WHERE
                    cParentID = '%s' 
                    ) OR (cSaleMode='%s')) AND b.cID not in (select distinct cInChargeID from tclass_changeRecord)''' % ( starttime, endtime,cGoodsid,in_p_typeidForIntroducer,cstudentId,ERPSaleModeREFId,ERPSaleModeREFId)
    cursor.execute(query,tuple(cTypeIdForIntroducerList))  #作为介绍人，其被介绍的人在这段时间内购买的成才课程+ 招生意向表中的渠道来源为REF，此时介绍人要加积分
    rows = cursor.fetchall()
    for row in rows:
        IdList.append(row)
    dbService.closeDbConn(conn)
    return IdList


#～～～～～～～～～～～～～～～～～～～～～～以下是退费部分～～～～～～～～～～～～～～～～～～～#
#2019-6-14 增加校管家09全日制BD和07暑假班 的退积分功能
#查看我应该扣减的积分（退费+作废+结转: 我购买的课程、特定物品 或者我介绍的人购买的课程或特定物品 之后退费 引起的积分扣费）
def GetMyMinusIntegralByFlagStatus(starttime,endtime,cGoodsid,cTypeIdForMeList):
    logger.info("get MyMinusIntegral by myShiftAndGoods and flag and status...")
    IdList = []
    in_p_typeidForMe = ', '.join(list(map(lambda x: '%s', cTypeIdForMeList)))
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['dbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    #查看我退费+作废+结转的课程合同
    query='''SELECT
                DISTINCT
                 a.cStudentUserID,
                 a.cID,
                 a.cCreateTime,
                 b.cStatus,
                 b.cflag,
                 a.cShiftID
            FROM
                tFeeChargeShift a
                LEFT JOIN tFeeChargeRecords b ON a.cChargeID= b.cID
                LEFT JOIN tFeeChargeCustType d ON a.cID= d.cChargeSubID 
            WHERE
                ((a.cCreateTime>= '%s' AND a.cCreateTime<= '%s'  AND b.cStatus= 1  AND b.cFlag= -1 AND cast(d.cTypeID as varchar(36)) IN (%s) AND a.cShiftID IN(SELECT DISTINCT
                                        cID 
                                    FROM
                                        tShift 
                                    WHERE
                                    cCategory IN ( SELECT cID FROM tDictionary WHERE (cValue LIKE '%%%s%%' OR cValue in ('09-全日制BD','07-暑假班')) ))) OR 
                (b.cUpDateTime>= '%s' AND b.cUpDateTime<= '%s'  AND a.cStatus= 0  AND b.cFlag= 1 AND cast(d.cTypeID as varchar(36)) IN (%s) AND a.cShiftID IN(SELECT DISTINCT
                                        cID 
                                    FROM
                                        tShift 
                                    WHERE
                                    cCategory IN ( SELECT cID FROM tDictionary WHERE (cValue LIKE '%%%s%%' OR cValue in ('09-全日制BD','07-暑假班')) ))) OR
                (a.cCreateTime>= '%s' AND a.cCreateTime <= '%s' AND b.cStatus= 1 AND b.cFlag= 0 AND a.cShiftID <>'00000000-0000-0000-0000-000000000000' and b.cChangeClassRecordID='00000000-0000-0000-0000-000000000000' ))               
                and b.cID not in (select distinct cInChargeID from tclass_changeRecord) '''  % (starttime,endtime,in_p_typeidForMe,'成才',starttime,endtime,in_p_typeidForMe,'成才',starttime,endtime)
    tmplist =cTypeIdForMeList
    for item in range(len(cTypeIdForMeList)):
        tmplist.append(cTypeIdForMeList[item])
    cursor.execute(query,tuple(tmplist))  #获取学生自己退费课程应该扣减的积分记录数
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row)


    #--我购买的特定物品的退费合同
    query='''SELECT
                DISTINCT
                 a.cStudentUserID,
                 a.cID,
                 a.cCreateTime,
                 b.cStatus,
                 b.cflag
            FROM
                tFeeChargeGoods a
                LEFT JOIN tFeeChargeRecords b ON a.cChargeID= b.cID
                LEFT JOIN tFeeChargeCustType d ON a.cID= d.cChargeSubID 
            WHERE
                ((a.cCreateTime>= '%s' AND a.cCreateTime<= '%s'  AND b.cStatus= 1  AND b.cFlag= -1 AND cast(d.cTypeID as varchar(36)) IN (%s) AND a.cGoodsID ='%s' ) OR 
                (b.cUpDateTime>= '%s' AND b.cUpDateTime<= '%s'  AND a.cStatus= 0  AND b.cFlag= 1 AND cast(d.cTypeID as varchar(36)) IN (%s) AND a.cGoodsID ='%s' ) OR
                (a.cCreateTime>= '%s' AND a.cCreateTime <= '%s' AND b.cStatus= 1 AND b.cFlag= 0 AND a.cGoodsID ='%s' and b.cChangeClassRecordID='00000000-0000-0000-0000-000000000000' ))               
                and b.cID not in (select distinct cInChargeID from tclass_changeRecord) '''  % (starttime,endtime,in_p_typeidForMe,cGoodsid,starttime,endtime,in_p_typeidForMe,cGoodsid,starttime,endtime,cGoodsid)
    cursor.execute(query,tuple(tmplist))  #获取学生自己购买课程应该获得的积分
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row)
    dbService.closeDbConn(conn)
    return IdList