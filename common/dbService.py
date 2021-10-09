# -*- coding: UTF-8 -*-

import pymysql,pymssql,pymongo
from .logLib import logLib

logger = logLib(__name__)

def connectSqlServerDb(server, dbName, userName, pwd, port=1433):
    """
    connect SQL Server
    @param server, str
    @param dbName, str
    @param userName, str
    @param passwd, str
    @return object conn
    """
    logger.info("Start DB %s for server %s..." %(dbName, server))
    try:
        #conn = pyodbc.connect('DRIVER={ODBC Driver 13.1 for SQL Server}; SERVER=192.168.12.3,1433; DATABASE=lb_erp_testdb; UID=sa; PWD=#server2018')
        conn = pymssql.connect(host=server,port=port, database=dbName, user=userName, password=pwd,charset="utf8") #线上端口号1344
    except:
        msg = "connect DB %s for Server %s failed" %(dbName, server)
        logger.error(msg)
        assert False, msg

    return conn

def connectMySqlServerDb(server, dbName, username, password, cursorclass=None):
    """
        connect mySql server
        :param server:
        :param dbName:
        :param username:
        :param password:
        :return:
    """
    logger.info('Start connect MySql DB - server: %s, dbName: %s' % (server, dbName))
    try:
        if cursorclass is None:
            conn = pymysql.connect(host=server, user=username, passwd=password, db=dbName, charset='utf8')
        else:
            conn = pymysql.connect(host=server, user=username, passwd=password, db=dbName, charset='utf8',
                                   cursorclass=cursorclass)
        return conn
    except Exception as e:
        msg = "connect MySql DB failed for server: %s, dbName: %s" % (server, dbName)
        logger.error(msg)
        # assert False, msg


def executeMySqlCommand(jDbConn, sqlCommand, args=None):
    """
        get db result by execute mysql query
        :param object jDbConn
        :param string sqlCommand
        :return object
    """
    conn = connectMySqlServerDb(jDbConn['dbHost'], jDbConn["dbName"],
                                jDbConn["dbUser"], jDbConn["dbPassword"])
    assert conn is not None, "Failed to connect to db %s" % jDbConn["dbHost"]
    cursor = conn.cursor(cursorclass=pymysql.cursors.DictCursor)
    if args:
        cursor.execute(sqlCommand, args)
    else:
        cursor.execute(sqlCommand)
    rows = cursor.fetchall()
    results = list(rows) if len(rows) > 1 else rows[0] if len(rows) > 0 else None
    conn.commit()
    cursor.close()
    closeDbConn(conn)
    return results

def executeMysql(conn, sqlCommand, closeFlag=False, args=None):
    """
    执行mysql命令，默认不关闭连接
    :param conn:
    :param sqlCommand:
    :param closeFlag:
    :return:
    """
    cursor = getCursor(conn)
    if args:
        cursor.execute(sqlCommand, args)
    else:
        cursor.execute(sqlCommand)
    rows = cursor.fetchall()
    results = list(rows) if len(rows) > 1 else rows[0] if len(rows) > 0 else None
    conn.commit()
    cursor.close()
    if closeFlag:
        closeDbConn(conn)
    return results

def executeSqlServer(conn, sqlCommand, closeFlag=False):
    """
        get db result by execute sqlserver query
        :param object jDbConn
        :param string sqlCommand
        :return object
    """
    cursor = conn.cursor()
    cursor.execute(sqlCommand)
    rows = cursor.fetchall()
    results = list(rows) if len(rows) > 1 else rows[0] if len(rows) > 0 else None
    conn.commit()
    cursor.close()
    if closeFlag:
        closeDbConn(conn)
    return results


def executeSqlServerCommandQuery(jDbConn, sqlCommand):
    """
        get db result by execute sqlserver query
        :param object jDbConn
        :param string sqlCommand
        :return object
    """
    conn = connectSqlServerDb(jDbConn['dbHost'], jDbConn["dbName"],
                              jDbConn["dbUser"], jDbConn["dbPassword"])
    assert conn is not None, "Failed to connect to db %s" % jDbConn["dbHost"]
    cursor = conn.cursor()
    cursor.execute(sqlCommand)

    rows = cursor.fetchall()
    results = list(rows) if len(rows) > 1 else rows[0] if len(rows) > 0 else None
    conn.commit()
    cursor.close()
    closeDbConn(conn)
    return results


def executeSqlServerQueryAsDictList(jDbConn, sqlCommand):
    """
        get db result as list format by execute sqlserver query
        :param object jDbConn
        :param string sqlCommand
        :return object
    """
    conn = connectSqlServerDb(jDbConn['dbHost'], jDbConn["dbName"],
                              jDbConn["dbUser"], jDbConn["dbPassword"])

    assert conn is not None, "Failed to connect to db %s" % jDbConn["dbHost"]
    cursor = conn.cursor()
    cursor.execute(sqlCommand)
    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    results = []
    for row in rows:
        results.append(dict(list(zip(columns, row))))
    cursor.close()
    closeDbConn(conn)
    return results if len(results) > 0 else None


def executeSqlServerCommandNonQuery(jDbConn, sqlCommand):
    """
        execute sqlserver query
        :param object jDbConn
        :param string sqlCommand
    """
    conn = connectSqlServerDb(jDbConn['dbHost'], jDbConn["dbName"],
                              jDbConn["dbUser"], jDbConn["dbPassword"])
    assert conn is not None, "Failed to connect to db %s" % jDbConn["dbHost"]
    cursor = conn.cursor()
    try:
        cursor.execute(sqlCommand)
        conn.commit()
    except:
        conn.rollback()
    finally:
        # 关闭连接
        closeDbConn(conn)



def getCursor(conn):
    '''
        get DB cursor
        :param object conn
        :return object cursor
    '''
    cursor = conn.cursor()
    return cursor



def closeDbConn(conn):
    '''
        Close DB connection
        :param object conn
    '''
    logger.info("Close DB connection")
    if conn != None:
        conn.close()


def connectMongoDB(dbHost,dbName,port=27017,userName=None, userPwd=None):
    """
    连接MongoDB数据库
    :param dbHost:主机名称或者IP
    :param port: 端口默认27017
    :param dbName: 数据库名称
    :param userName:
    :param pwd:
    :return:
    """
    client = pymongo.MongoClient(dbHost, port)
    db = client['admin']
    db.authenticate(userName, userPwd)
    conn = client[dbName]
    return conn,client

def queryMongoDB(conn, collect_name, query, limit=1):
    """
    执行查询mongoDb语句
    :param conn: obj 连接对象
    :param collect_name: string 表名
    :param query: json 查询json
    :param limit: int 限制条数，默认为1
    :return:
    """
    result_list = []
    # 连接表
    collection = conn[collect_name]
    # 访问表的数据,过滤查询
    item = collection.find(query).limit(limit)
    for x in item:
        result_list.append(x)
    if not result_list:
        return result_list
    return result_list[0] if limit == 1 else result_list

def queryMongoAggregate(conn, collect_name, query):
    """
    执行查询mongodb的Aggregate语句
    :param conn: obj 连接对象
    :param collect_name: string 表名
    :param query: 聚合查询的条件
    :return:
    """
    # 连接表
    collection = conn[collect_name]
    # 访问表的数据,过滤查询
    items = collection.aggregate(pipeline=query)
    return items

