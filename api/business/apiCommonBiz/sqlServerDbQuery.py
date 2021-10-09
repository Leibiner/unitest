# -*- coding: cp936 -*-
# coding = utf8
# by zgf
#���в�ѯ����ERP���ݿ⣬Ҳ����sql server���ݵķ��������棺 create by typhoon 2018.11.
import logging,datetime,time
from common import dbService
from testconfig import config
from testdata.erpData import erpData

logger = logging.getLogger(__name__)

'''
get all sale class list
@return list saleClassList
'''
#----------------���°༶�鿴-ת���ϵ�������-��Ӧ�ġ����°༶��-����/δ����İ༶�б�------------ʹ��
#SQL���д����ݲ�����
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


#----------------�鿴���°༶�ĵ�һ�ڿο�ʼʱ��------------ʹ��
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

#----------------���°༶�鿴-�����ѿ���/δ�����Ӧ��ѧ������ת���Ϻ��ѡ��/δѡ�������------------ʹ��
#�鿴���º�ͬ��tFeeChargeRecords������/��ת/�˷ѵĺ�ͬ�����������Ϻ�ͬ��
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
    #��ȡֱӪУ����
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['dbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query,tuple(CampusIdList))
    rows =cursor.fetchall()

    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)

    # ��ȡ����У����
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['JMXdbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query,tuple(CampusIdList))
    rows =cursor.fetchall()

    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)

    return IdList[0]+IdList[1]

#�鿴���º�ͬ��tFeeChargeRecords�����Ϻ�ͬ��
def GetFeeChargeCountByStatus(starttime,endtime,cFlag,CampusIdList):
    logger.info("getReportContract by date...")
    IdList = []
    in_p = ', '.join(list(map(lambda x: '%s', CampusIdList)))
    if cFlag!=9: #ȡ������ת���˷ѵĺ�ͬ�����������cFlag��ֵ�ж�
         query = '''SELECT count(*) FROM tFeeChargeRecords WHERE cUpdateTime>='%s' AND cUpdateTime<='%s' 
                 AND cStatus=0 AND  cFlag=%i  And cCampusID in (%s)''' % (starttime,endtime,cFlag,in_p)
    elif cFlag==9: #ȡ��������+��ת+�˷ѵĺ�ͬ��
        query = '''SELECT count(*) FROM tFeeChargeRecords WHERE cUpdateTime>='%s' AND cUpdateTime<='%s'
                AND cStatus=0 And cCampusID in (%s)''' % (starttime, endtime,in_p)
    #��ȡֱӪУ����
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['dbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query,tuple(CampusIdList))
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)

    #��ȡ����У����
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['JMXdbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query,tuple(CampusIdList))
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)

    return IdList[0] +IdList[1]


#�鿴���º�ͬ---�쳣��ͬ��������Ŀǰ�쳣��ͬ�Ķ����ǣ�1�����������ں�ͬ��������֮ǰ�����м�¼����ΪԤ����¼ 2��
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

    #ȡֱӪУ
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

    # ȡ����У
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


#�鿴���º�ͬ--����ͬ�շѷ�ʽ���շѽ��  #2019-06-11 ��ȡ���ʱȥ����ת�Ľ��
def GetPayMoneyByPayChannel(starttime,endtime,CampusidList):
    logger.info("get PayMoney by date...")
    IdList = []
    in_paramCampusidList=', '.join(list(map(lambda x: '%s', CampusidList)))
    query_add = '''SELECT isnull(sum(b.cMoney),0) FROM tFeeChargeRecords a 
               LEFT JOIN tFeeChargeMode b ON a.cID=b.cChargeID 
               WHERE b.cCreateTime>='%s' AND b.cCreateTime<='%s' AND b.cName <>'����Ǯ��' And a.cflag<>0 
               AND a.cCampusID in (%s) ''' % (starttime,endtime,in_paramCampusidList)
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['dbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query_add,tuple(CampusidList)) #ͳ�Ƶ��촴�������м�¼���շ� + �˷ѵ��ܶ
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row[0])

    query_del = '''SELECT isnull(sum(b.cMoney),0) FROM tFeeChargeRecords a 
               LEFT JOIN tFeeChargeMode b ON a.cID=b.cChargeID 
               WHERE a.cUpdateTime>='%s' AND a.cUpdateTime<='%s' AND a.cstatus=0 And a.cflag<>0 AND b.cName<>'����Ǯ��' AND a.cCampusID in (%s)''' % (starttime,endtime,in_paramCampusidList)
    cursor.execute(query_del,tuple(CampusidList)) #ͳ�Ƶ�����µ������ܶ�
    rows = cursor.fetchall()
    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)

    #ȡ����У
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['JMXdbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query_add,tuple(CampusidList)) #ͳ�Ƶ��촴�������м�¼���շ� + �˷ѵ��ܶ
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row[0])

    cursor.execute(query_del,tuple(CampusidList)) #ͳ�Ƶ�����µ������ܶ�
    rows = cursor.fetchall()
    for row in rows:
        IdList.append(row[0])

    return IdList #���صĵ�һ��ֵ�����н��촴�����շ�+��ת + �˷ѵĽ��������ϵģ����ڶ��������н������ϵĽ�����������ͬ����ֻ�Ǽ���У������

#�鿴���º�ͬ---���º�ͬ-����ָ�����ѷ�ʽ����ȡ���ָ����µ��������  #2019-06-11 ��ȡ���Ͻ��ʱȥ����ת�Ľ��
def GetAccChargePayChannelByCampusId(starttime,endtime,cFlag,cStatus,payChannelList,CampusidList):
    logger.info("get getAccChargePayChannel by date...")
    in_parampayChannelList=', '.join(list(map(lambda x: '%s', payChannelList)))
    in_paramCampusidList = ', '.join(list(map(lambda x: '%s', CampusidList)))
    IdList = []
    if cStatus==None: #��Ч��¼
        query = '''SELECT b.cName,isnull(sum(b.cMoney),0),count(0) FROM tFeeChargeRecords a 
                    LEFT JOIN tFeeChargeMode b ON a.cID=b.cChargeID 
                    WHERE a.cDate>='%s' AND a.cDate<='%s' AND a.cflag=%i  And b.cName in (%s) And b.cMoney<>0
                    AND a.cCampusID in(%s) GROUP BY b.cName ''' % (starttime, endtime, cFlag, in_parampayChannelList,in_paramCampusidList)

    else:  #ȡ���ϼ�¼
        query = '''SELECT b.cName,isnull(sum(b.cMoney),0),count(0) FROM tFeeChargeRecords a 
                   LEFT JOIN tFeeChargeMode b ON a.cID=b.cChargeID 
                   WHERE a.cUpdateTime>='%s' AND a.cUpdateTime<='%s' AND a.cStatus=%i And a.cflag<>0 And b.cName in (%s) And b.cMoney<>0
                   AND  a.cCampusID in(%s) GROUP BY b.cName ''' % (starttime, endtime,cStatus, in_parampayChannelList,in_paramCampusidList) #���������ֻ�ȡ���ϵ�����

    tmplist = payChannelList.copy()
    tmplist.extend(CampusidList)
  #ȡֱӪУ
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['dbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query,tuple(tmplist))
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(list(row))
        IdList.append(list(row))
    dbService.closeDbConn(conn)

    #ȡ����У
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



#�鿴���º�ͬ---����ĳ��֧����ʽ������������ǰ�tFeeChargeMode�еĴ���ʱ�����ͳ��  #2019-06-11 ��ȡ���Ͻ��ʱȥ����ת�Ľ��
def GetIncomeTatolByPayChannel(starttime,endtime,payChannelList,cFlag,cStatus,CampusidList):
    logger.info("get IncomeTatol by date...")
    in_parampayChannelList=', '.join(list(map(lambda x: '%s', payChannelList)))
    in_paramCampusidList=', '.join(list(map(lambda x: '%s', CampusidList)))
    IdList = []
    if cStatus==None:
        if payChannelList==[]:
            query = '''SELECT isnull(sum(b.cMoney),0),count(0) FROM tFeeChargeRecords a 
                        LEFT JOIN tFeeChargeMode b ON a.cID=b.cChargeID 
                        WHERE b.cCreateTime>='%s' AND b.cCreateTime<='%s' AND a.cflag=%i  And b.cName<>'����Ǯ��' And b.cMoney<>0
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
                       WHERE a.cUpdateTime>='%s' AND a.cUpdateTime<='%s' AND a.cStatus=%i And a.cflag<>0 And b.cName<>'����Ǯ��' And b.cMoney<>0
                       AND a.cCampusID in (%s)''' % (starttime, endtime,cStatus, in_paramCampusidList) #���������ֻ�ȡ���ϵ�����
        else:
            query = '''SELECT isnull(sum(b.cMoney),0),count(0) FROM tFeeChargeRecords a 
                       LEFT JOIN tFeeChargeMode b ON a.cID=b.cChargeID 
                       WHERE a.cUpdateTime>='%s' AND a.cUpdateTime<='%s'  AND a.cStatus=%i And a.cflag<>0  And b.cMoney<>0 AND b.cName in(%s)
                       AND a.cCampusID in (%s)''' % (starttime, endtime, cStatus, in_parampayChannelList,in_paramCampusidList) #��ȡ�����������ϵ�����
    if payChannelList == []:
        tmplist = CampusidList.copy()
    else:
        tmplist = payChannelList.copy()
        tmplist.extend(CampusidList)

    #ȡֱӪУ
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['dbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query,tuple(tmplist))
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row)
    dbService.closeDbConn(conn)

    #ȡ����У
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['JMXdbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query,tuple(tmplist))
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row)
    dbService.closeDbConn(conn)

    return IdList


#�鿴���º�ͬ---����ĳ��֧����ʽ���������  2019-06-11 ���Ͻ��ȡֵ��ȥ����ת������
def GetAccIncomeTatolByPayChannel(starttime,endtime,payChannelList,cFlag,cStatus,CampusidList):
    logger.info("get AccIncomeTatol by date...")
    IdList = []
    in_parampayChannelList = ', '.join(list(map(lambda x: '%s', payChannelList)))
    in_paramCampusidList = ', '.join(list(map(lambda x: '%s', CampusidList)))
    if cStatus==None:
        if payChannelList==[]:#��ʾ�鿴���е�֧����ʽ����ʱӦ��ȥ������Ǯ����ֵ
            query = '''SELECT isnull(sum(b.cMoney),0),count(0) FROM tFeeChargeRecords a 
                        LEFT JOIN tFeeChargeMode b ON a.cID=b.cChargeID 
                        WHERE a.cDate>='%s' AND a.cDate<='%s' AND a.cflag=%i  And b.cName<>'����Ǯ��' And b.cMoney<>0
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
                       WHERE a.cUpdateTime>='%s' AND a.cUpdateTime<='%s' AND a.cStatus=%i AND a.cflag<>0 And b.cName<>'����Ǯ��' And b.cMoney<>0
                       AND a.cCampusID in (%s)''' % (starttime, endtime,cStatus, in_paramCampusidList) #���������ֻ�ȡ���ϵ�����
        else:
            query = '''SELECT isnull(sum(b.cMoney),0),count(0) FROM tFeeChargeRecords a 
                       LEFT JOIN tFeeChargeMode b ON a.cID=b.cChargeID 
                       WHERE a.cUpdateTime>='%s' AND a.cUpdateTime<='%s'  AND a.cStatus=%i AND a.cflag<>0 And b.cMoney<>0 AND b.cName in (%s)
                       AND a.cCampusID in (%s)''' % (starttime, endtime,cStatus,in_parampayChannelList, in_paramCampusidList) #��ȡ�����������ϵ�����
    if payChannelList==[]:
        tmplist = CampusidList.copy()
    else:
        tmplist = payChannelList.copy()
        tmplist.extend(CampusidList)

    #��ȡֱӪ
    conn =  dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'], erpData.ErpOnlineDb['dbName'],
                                            erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query,tuple(tmplist))
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row)
    dbService.closeDbConn(conn)

    #��ȡ����У
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'], erpData.ErpOnlineDb['JMXdbName'],
                                            erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query,tuple(tmplist))
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row)
    dbService.closeDbConn(conn)
    return IdList


#�鿴���º�ͬ--��ȡʱ����ڵĺ�ͬ����
def GetcTypeIDByDate(starttime,endtime,NotIncludeCampusId):
    logger.info("get cTypeID by date...")
    typeIdSet = set()
    query = '''SELECT distinct b.cTypeID FROM tFeeChargeRecords a 
               LEFT JOIN tFeeChargeCustType b ON a.cID= b.cChargeID
               WHERE  a.cstatus=1 AND a.cCreateTime>='%s' AND a.cCreateTime<='%s' And a.cpayFact>0 
               AND a.cCampusID not in (%s)''' % (starttime,endtime,NotIncludeCampusId)
    # ȡֱӪ
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['dbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query)
    rows =cursor.fetchall()
    for row in rows:
        typeIdSet.add(row[0])
    dbService.closeDbConn(conn)

    #ȡ���˵�typeid
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['JMXdbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query)
    rows =cursor.fetchall()
    for row in rows:
        typeIdSet.add(row[0]) #���ü��������治�ظ�Ԫ�����У�����Ԫ���Ѿ����ڣ��򲻽����κβ���
    dbService.closeDbConn(conn)
    return list(typeIdSet)

#�鿴���º�ͬ-�������ʱ������º�ͬ���ͣ����ҹ����ĺ�ͬ��
def GetChargeCountByDateAndTypeID(starttime,endtime,cTypeIdlist,CampusIdList):
    logger.info("get chargeCount by date...")
    in_paramTypeid= ', '.join(list(map(lambda x: '%s', cTypeIdlist)))
    in_paramCampus = ', '.join(list(map(lambda x: '%s', CampusIdList)))
    IdList = []

    tmplist =cTypeIdlist.copy()  #Ϊ�˴�queryֵ
    tmplist.extend(CampusIdList)

    query = '''SELECT isnull( SUM ( a.cPayFact ), 0 ),count(distinct(a.cID)) FROM tFeeChargeRecords a LEFT JOIN tFeeChargeCustType b ON a.cID= b.cChargeID
               WHERE  a.cstatus=1 AND a.cCreateTime>='%s' AND a.cCreateTime<='%s' And a.cpayFact>0 And lower(b.cTypeID) in (%s)
               AND a.cCampusID in (%s)''' % (starttime,endtime,in_paramTypeid,in_paramCampus)
    #��ȡֱӪ
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['dbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query,tuple(tmplist))
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row)
    dbService.closeDbConn(conn)

    #��ȡ����
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['JMXdbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query,tuple(tmplist))
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row)
    dbService.closeDbConn(conn)
    return IdList


#�鿴���º�ͬ-�������ʱ������º�ͬ���ͣ����ҹ����ĺ�ͬ����
def GetStudentCountByDateAndTypeID(starttime,endtime,cTypeIdlist,CampusIdList):
    logger.info("get cStudentUserCount by date...")
    in_paramTypeid= ', '.join(list(map(lambda x: '%s', cTypeIdlist)))
    in_paramCampus = ', '.join(list(map(lambda x: '%s', CampusIdList)))
    IdList = []

    tmplist =cTypeIdlist.copy()  #Ϊ�˴�queryֵ
    tmplist.extend(CampusIdList)

    query = '''SELECT count(distinct(a.cStudentUserID)) FROM tFeeChargeRecords a LEFT JOIN tFeeChargeCustType b ON a.cID= b.cChargeID
               WHERE  a.cstatus=1 AND a.cCreateTime>='%s' AND a.cCreateTime<='%s' And a.cpayFact>0 And lower(b.cTypeID) in(%s)
               AND a.cCampusID in (%s)''' % (starttime,endtime,in_paramTypeid,in_paramCampus)
    # ��ȡֱӪ
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['dbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query,tuple(tmplist))
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)

    # ��ȡ����
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['JMXdbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query,tuple(tmplist))
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)
    return IdList[0] +IdList[1]

#-------------�������շ���Ŀ�Ĳ��񱨱�-----------#


#�շ���Ŀ-��ȡָ��ʱ���ڵĺ�ͬ��Ӧ�Ŀγ̵�ʵ���շ� #2019-06-11 ȥ����ת�Ľ��
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
        #��ȡֱӪ
        conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['dbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
        cursor = conn.cursor()
        cursor.execute(query, tuple(tmplist)) #�����SQL�д���in��in��һ��lIST�е�д��
        rows =cursor.fetchall()
        for row in rows:
            IdList.append(row)
        dbService.closeDbConn(conn)

        #��ȡ����
        conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['JMXdbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
        cursor = conn.cursor()
        cursor.execute(query,tuple(tmplist))
        rows =cursor.fetchall()
        for row in rows:
            IdList.append(row)
        dbService.closeDbConn(conn)
    except:
        print("dicGUIDΪ:"+str(cChargeIdsList)+"У��Ϊ:"+str(CampusIdList))
    return IdList


#�շ���Ŀ-��ȡָ��ʱ���ڵĺ�ͬ��Ӧ����Ʒ��ʵ���շ� #2019-06-11 ȥ����ת�Ľ��
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
    #ȡֱӪ
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['dbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query, tuple(tmplist)) #�����SQL�д���in��in��һ��lIST�е�д��
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row)
    dbService.closeDbConn(conn)

    #ȡ����У
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['JMXdbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query, tuple(tmplist)) #�����SQL�д���in��in��һ��lIST�е�д��
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row)
    dbService.closeDbConn(conn)
    return IdList



#�鿴���º�ͬ-�������ʱ������º�ͬ���ͣ�����Ԥ�棨prestore����� #2019-06-11�޸ģ����е����ݲ�������ת�Ľ��
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
                   AND a.cCampusID in (%s) ''' % (starttime,endtime,cFlag,'Ԥ��',in_paramCampus)
    else:
        query = '''SELECT isnull(SUM (a.cPayFactSub),0),Count(0)  FROM tFeeChargeShift a 
                   LEFT JOIN tFeeChargeCustType b ON a.cChargeID= b.cChargeID
                   LEFT JOIN tFeeChargeRecords c ON a.cChargeID= c.cID 
                   WHERE  a.cshiftId='00000000-0000-0000-0000-000000000000' AND c.cUpdateTime>='%s' AND c.cUpdateTime<='%s' And c.cStatus=%i
                   And b.cTypeID in (select cID from tDictionary WHERE cValue =   '%s') AND c.cflag<>0  
                   AND a.cCampusID in (%s) ''' % (starttime,endtime,cStatus,'Ԥ��',in_paramCampus)
   #ȡֱӪ
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['dbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query,tuple(CampusIdList))
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)

    #ȡ����У
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['JMXdbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query,tuple(CampusIdList))
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)
    return IdList[0]+IdList[1]

#2019-06-11 ��ȡ���Ͻ��ʱȥ����ת�Ľ��
#�鿴���º�ͬ-�������ʱ������º�ͬ�Ĺ�����Ŀ�У�����"����"���͵��շѱ�����
# ����һ����ͬ������3��������Ŀ������2�ſγ̣�1������Ʒ����ô����ͳ�Ƶ��Ǵ���cCategory���͵Ŀγ����ʱ���ڵ�����"����"�շ����͵ı�����
#1����ͬ��¼��2��tFeeChargeShift��¼���շ����ͷֱ����������������շ����ͣ���ôtFeeChargeCustType�л���2����¼1��������1�������ƣ���1��tFeeChargeGoods��Ʒ��¼
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
    #ֱӪ
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['dbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query,tuple(tmplist))
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row)
    dbService.closeDbConn(conn)

    #����
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'], erpData.ErpOnlineDb['JMXdbName'],
                                        erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query, tuple(tmplist))
    rows = cursor.fetchall()
    for row in rows:
        IdList.append(row)
    dbService.closeDbConn(conn)

    return IdList

#2019-06-11 ��ȡ���Ͻ��ʱȥ����ת�Ľ��
#�鿴���º�ͬ-�������ʱ������º�ͬ�Ĺ�����Ŀ�У�����"����"���͵��շѱ�����
# ����һ����ͬ������3��������Ŀ������2�ſγ̣�1������Ʒ����ô����ͳ�Ƶ��Ǵ���cCategory���͵Ŀγ����ʱ���ڵ�����"����"�շ����͵ı�����
#1����ͬ��¼��2��tFeeChargeShift��¼���շ����ͷֱ����������������շ����ͣ���ôtFeeChargeCustType�л���2����¼1��������1�������ƣ���1��tFeeChargeGoods��Ʒ��¼
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
    #ֱӪ
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['dbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query,tuple(tmplist))
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)

    #����
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['JMXdbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query,tuple(tmplist))
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)
    return IdList[0] + IdList[1]


#�鿴���º�ͬ--ָ��ĳ���γ������»�ȡʱ����ڵĺ�ͬ����
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
    # ��ȡֱӪ
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['dbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query,tuple(tmplist))
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)

    # ��ȡ����
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['JMXdbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query,tuple(tmplist))
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)
    return IdList


#�鿴���µİ༶-�ɲ���γ̵İ༶��������Ա����
def GetERPClassAndStudentCountGroupBycCategory(ReportDay,endtime,cCampustList,leverNameList):
    logger.info("get ClassAndStudentCount by date...")
    IdList = []
    in_paramCampus = ', '.join(list(map(lambda x: '%s', cCampustList)))
    in_paramLevel = ', '.join(list(map(lambda x: '%s', leverNameList)))
    ReportDay=str(ReportDay)+' 23:59:59' #�����õĻ�����Ĭ��Ϊ00:00:00
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
                 ''' % (ReportDay,ReportDay,ReportDay,endtime,'�ɲ�',in_paramCampus,in_paramLevel)
    tmplist=cCampustList.copy()
    tmplist.extend(leverNameList)
    #�鿴ֱӪ
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['dbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query,tuple(tmplist))
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row)
    dbService.closeDbConn(conn)


    #�鿴����
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['JMXdbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query,tuple(tmplist))
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row)
    dbService.closeDbConn(conn)

    return IdList


#�鿴���µİ༶-�ɲ���γ̵ĸ��༶��Ӧ������
def GetERPStudentCountGroupBycCategoryAndClass(ReportDay,endtime,cCampustList,leverNameList):
    logger.info("get StudentCount by date group by ...")
    IdList = []
    in_paramCampus = ', '.join(list(map(lambda x: '%s', cCampustList)))
    in_paramLevel = ', '.join(list(map(lambda x: '%s', leverNameList)))
    # 4��10���޸����¹���SQL��ԭ�������������Ҫȥ���� AND cClassId IN ( SELECT cClassID FROM tClass_Student WHERE cStatus = 1 )
    ReportDay=str(ReportDay)+' 23:59:59' #�����õĻ�����Ĭ��Ϊ00:00:00
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
                 ''' % (ReportDay,ReportDay,ReportDay,endtime,'�ɲ�',in_paramCampus,in_paramLevel)
    tmplist = cCampustList.copy()
    tmplist.extend(leverNameList)

    #ȡֱӪ
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['dbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query,tuple(tmplist))
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row)
    dbService.closeDbConn(conn)

    #ȡ����
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['JMXdbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query,tuple(tmplist))
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row)
    dbService.closeDbConn(conn)

    return IdList


#�鿴���µİ༶-�ɲ���γ̵��쳣��Ա����
def GetERPExceptClassAndStudentCountGroupBycCategory(ReportDay,endtime,cCampustList,leverNameList):
    ReportDay=str(ReportDay)+' 23:59:59' #�����õĻ�����Ĭ��Ϊ00:00:00
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
                 ''' % (ReportDay,ReportDay,ReportDay,endtime,'�ɲ�',in_paramCampus,in_paramLevel)
    tmplist=cCampustList.copy()
    tmplist.extend(leverNameList)

    #ȡֱӪ
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['dbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    cursor.execute(query,tuple(tmplist))
    rows =cursor.fetchall()
    for row in rows:
        tmpDic[row[1]]=row[2]
    dbService.closeDbConn(conn)

    #ȡ����
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
###----------------------------�����ǻ����̳�---------------------------#
#�鿴��Ӧ�û�õĻ��֣�����Ϊ�ͻ���δ��ΪѧԱ֮ǰ������ʵĴ��� + ����Ϊ�����ˣ���������ѧԱ����������Ӧ�û�õĻ��֣�
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
    cursor.execute(query)  #��ȡ�ֻ���Ϊ"tel"���ˣ���û��ΪѧԱ֮ǰ��ĳ��ʱ���ڵĵ��ô���
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
    cursor.execute(query)  #��ȡ�ֻ���Ϊ"tel"���ˣ���Ϊ�����˵���ݣ���ĳ��ʱ���ڽ��ܵ���������˴� ������SQL�в��ܼ�distinct a.cCustomerID
    rows = cursor.fetchall()
    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)
    return IdList

#2019-6-14 ����У�ܼ�09ȫ����BD��07��ٰ� ��+���ֹ���
#2019-6-17 ȥ������У���Ĺ��ˣ����ǲ���У��Ҳ���Բ鵽
#�鿴��Ӧ�û�õĻ��֣���Ϊ�����γ̻���ܱ��˱����γ�����õĻ��֣�
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
                                                cCategory IN ( SELECT cID FROM tDictionary WHERE (cValue LIKE '%%%s%%'  OR cValue in ('09-ȫ����BD','07-��ٰ�'))))
                AND cast(d.cTypeID as varchar(36)) IN (%s) AND a.cStudentUserID='%s'  
                and b.cID not in (select distinct cInChargeID from tclass_changeRecord) ''' % (starttime,endtime,'�ɲ�',in_p_typeidForMe,cstudentId)
    cursor.execute(query,tuple(cTypeIdForMeList))  #��ȡѧ���Լ�����γ�Ӧ�û�õĻ���
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
                                    cCategory IN ( SELECT cID FROM tDictionary WHERE (cValue LIKE '%%%s%%' OR cValue in ('09-ȫ����BD','07-��ٰ�')) )) 
                    AND cast(d.cTypeID as varchar(36)) IN (%s)
                    AND a.cStudentUserID in (select cID from tStudent WHERE cIntroducer ='%s')
                    and a.cStudentUserID in (select cStudentID  FROM tStudentCustomer_SaleMode WHERE cSaleMode IN (
                    SELECT
                        cID 
                    FROM
                        tSaleMode 
                    WHERE
                    cParentID = '%s' 
                    ) OR (cSaleMode='%s')) AND  b.cID not in (select distinct cInChargeID from tclass_changeRecord) ''' % ( starttime, endtime, '�ɲ�',in_p_typeidForIntroducer,cstudentId,ERPSaleModeREFId,ERPSaleModeREFId)
    cursor.execute(query,tuple(cTypeIdForIntroducerList))  #��Ϊ�����ˣ��䱻���ܵ��������ʱ���ڹ���ĳɲſγ�+ ����������е�������ԴΪREF����ʱ������Ҫ�ӻ���
    rows = cursor.fetchall()
    for row in rows:
        IdList.append(row)
    dbService.closeDbConn(conn)
    return IdList

#�鿴��Ӧ�û�õĻ��֣���Ϊ���������ض���Ʒ����ܱ��˱����ض���Ʒ����õĻ��֣�
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
    cursor.execute(query,tuple(cTypeIdForMeList))  #��ȡѧ���Լ�����γ�Ӧ�û�õĻ���
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
    cursor.execute(query,tuple(cTypeIdForIntroducerList))  #��Ϊ�����ˣ��䱻���ܵ��������ʱ���ڹ���ĳɲſγ�+ ����������е�������ԴΪREF����ʱ������Ҫ�ӻ���
    rows = cursor.fetchall()
    for row in rows:
        IdList.append(row)
    dbService.closeDbConn(conn)
    return IdList


#���������������������������������������������������˷Ѳ��֡�������������������������������������#
#2019-6-14 ����У�ܼ�09ȫ����BD��07��ٰ� ���˻��ֹ���
#�鿴��Ӧ�ÿۼ��Ļ��֣��˷�+����+��ת: �ҹ���Ŀγ̡��ض���Ʒ �����ҽ��ܵ��˹���Ŀγ̻��ض���Ʒ ֮���˷� ����Ļ��ֿ۷ѣ�
def GetMyMinusIntegralByFlagStatus(starttime,endtime,cGoodsid,cTypeIdForMeList):
    logger.info("get MyMinusIntegral by myShiftAndGoods and flag and status...")
    IdList = []
    in_p_typeidForMe = ', '.join(list(map(lambda x: '%s', cTypeIdForMeList)))
    conn = dbService.connectSqlServerDb(erpData.ErpOnlineDb['dbHost'],erpData.ErpOnlineDb['dbName'],erpData.ErpOnlineDb['dbUser'], erpData.ErpOnlineDb['dbPassword'])
    cursor = conn.cursor()
    #�鿴���˷�+����+��ת�Ŀγ̺�ͬ
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
                                    cCategory IN ( SELECT cID FROM tDictionary WHERE (cValue LIKE '%%%s%%' OR cValue in ('09-ȫ����BD','07-��ٰ�')) ))) OR 
                (b.cUpDateTime>= '%s' AND b.cUpDateTime<= '%s'  AND a.cStatus= 0  AND b.cFlag= 1 AND cast(d.cTypeID as varchar(36)) IN (%s) AND a.cShiftID IN(SELECT DISTINCT
                                        cID 
                                    FROM
                                        tShift 
                                    WHERE
                                    cCategory IN ( SELECT cID FROM tDictionary WHERE (cValue LIKE '%%%s%%' OR cValue in ('09-ȫ����BD','07-��ٰ�')) ))) OR
                (a.cCreateTime>= '%s' AND a.cCreateTime <= '%s' AND b.cStatus= 1 AND b.cFlag= 0 AND a.cShiftID <>'00000000-0000-0000-0000-000000000000' and b.cChangeClassRecordID='00000000-0000-0000-0000-000000000000' ))               
                and b.cID not in (select distinct cInChargeID from tclass_changeRecord) '''  % (starttime,endtime,in_p_typeidForMe,'�ɲ�',starttime,endtime,in_p_typeidForMe,'�ɲ�',starttime,endtime)
    tmplist =cTypeIdForMeList
    for item in range(len(cTypeIdForMeList)):
        tmplist.append(cTypeIdForMeList[item])
    cursor.execute(query,tuple(tmplist))  #��ȡѧ���Լ��˷ѿγ�Ӧ�ÿۼ��Ļ��ּ�¼��
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row)


    #--�ҹ�����ض���Ʒ���˷Ѻ�ͬ
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
    cursor.execute(query,tuple(tmplist))  #��ȡѧ���Լ�����γ�Ӧ�û�õĻ���
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row)
    dbService.closeDbConn(conn)
    return IdList