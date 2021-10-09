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
def getOrderListByUserOpenid(userOpenid):
    logger.info("get all order list...")
    OrderList = []
    conn = dbService.connectMySqlServerDb(config['dbServerHost'],config['dbName'],config['dbUser'],config['dbPassword'])
    cursor = dbService.getCursor(conn)
    query = '''select order_code from wx_talkbee_order where open_id  = '%s' ''' %(userOpenid)
    cursor.execute(query)
    rows =cursor.fetchall()

    for row in rows:
        OrderList.append(row[0])

    dbService.closeDbConn(conn)
    return OrderList

#��ȡĳ�Ͽ�Ƶ�ʵ����пγ̰�ID
def getpackageIdList(frequency_id=None):
    logger.info("get all packageIdList...")
    IdList = []
    conn = dbService.connectMySqlServerDb(config['dbServerHost'],config['dbName'],config['dbUser'],config['dbPassword'])
    cursor = dbService.getCursor(conn)
    if frequency_id!=None:
        query = '''select a.package_id,class_frequency_id from package_class_frequency a, package_product b where a.class_frequency_id  ='%s' and a.flag = 1 and a.package_id=b.package_id and b.flag=1 ''' %(frequency_id)
    else:
        query = '''select a.package_id,class_frequency_id from package_class_frequency a,package_product b where a.flag=1 and a.package_id=b.package_id and b.flag=1 limit 0,2 '''
    cursor.execute(query)
    rows =cursor.fetchall()

    for row in rows:
        IdList.append(row)
    dbService.closeDbConn(conn)
    return IdList

#��ȡĳ�γ̰���ѧϰ��ٵĴ��IDƴ�������ַ���
def getPackageOutline(package_id=None,serial_id=None):
    logger.info("get all PackageOutline...")
    PackageOutlineIdList = []
    conn = dbService.connectMySqlServerDb(config['dbServerHost'],config['dbName'],config['dbUser'],config['dbPassword'])
    cursor = dbService.getCursor(conn)
    if serial_id==None:
        query = '''select id from package_outline where package_id  ='%s' ''' % (package_id)
    else:
        query = '''select id from package_outline where package_id  ='%s' and serial_id = '%s' ''' %(package_id,serial_id)
    cursor.execute(query)
    rows =cursor.fetchall()
    for row in rows:
        PackageOutlineIdList.append(row[0])
    dbService.closeDbConn(conn)
    return PackageOutlineIdList


#����course��ȡ���¿νڶ�Ӧ��videoID
def getVideoByCourseid(Courseid=None):
    logger.info("get all videoid  by courseid...")
    videoIdList = []
    conn = dbService.connectMySqlServerDb(config['dbServerHost'],config['dbName'],config['dbUser'],config['dbPassword'])
    cursor = dbService.getCursor(conn)
    if Courseid==None:
        query = '''select video_id from new_course_lesson_video where flag=1 '''
    else:
        query = '''select video_id from new_course_lesson_video where flag=1 and lesson_id in(select id from new_course_lesson where course_id ='%s')  ''' % (Courseid)
    cursor.execute(query)
    rows =cursor.fetchall()
    for row in rows:
        videoIdList.append(row[0])
    dbService.closeDbConn(conn)
    return videoIdList

#���ݼ���ID��ȡ���¿γ�course_id List
def getCourseIdBySerialid(Serialid=None):
    logger.info("get all CourseId  by Serialid...")
    CourseidList = []
    conn = dbService.connectMySqlServerDb(config['dbServerHost'],config['dbName'],config['dbUser'],config['dbPassword'])
    cursor = dbService.getCursor(conn)
    if Serialid==None:
        query = '''select course_id from new_course where flag=1 '''
    else:
        query = '''select course_id from new_course where flag=1 and books_serial_id ='%s' ''' % (Serialid)
    cursor.execute(query)
    rows =cursor.fetchall()
    for row in rows:
        CourseidList.append(row[0])
    dbService.closeDbConn(conn)
    return CourseidList

#����course��ȡ���¿ν�lessonID
def getLessonIdByCourseid(Courseid=None):
    logger.info("get all LessonId  by courseid...")
    LessonIdList = []
    conn = dbService.connectMySqlServerDb(config['dbServerHost'],config['dbName'],config['dbUser'],config['dbPassword'])
    cursor = dbService.getCursor(conn)
    if Courseid==None:
        query = '''select id from new_course_lesson where flag=1 '''
    else:
        query = '''select id from new_course_lesson where flag=1 and course_id ='%s' ''' % (Courseid)
    cursor.execute(query)
    rows =cursor.fetchall()
    for row in rows:
        LessonIdList.append(row[0])
    dbService.closeDbConn(conn)
    return LessonIdList


#��ȡ��Ч��ƴ��ID
def getGrouponIdByStatus(groupon_status=None):
    logger.info("get all GrouponId  by status ......")
    GrouponIdList = []
    conn = dbService.connectMySqlServerDb(config['dbServerHost'],config['dbName'],config['dbUser'],config['dbPassword'])
    cursor = dbService.getCursor(conn)
    if groupon_status==None:
        query = '''select groupon_id from groupon where flag=1 and groupon_status<>1 order by create_time desc limit 1'''
    else:
        query = '''select groupon_id from groupon where flag=1 and groupon_status =%i  order by create_time desc limit 1 ''' % (groupon_status)
    cursor.execute(query)
    rows =cursor.fetchall()
    for row in rows:
        GrouponIdList.append(row[0])
    dbService.closeDbConn(conn)
    return GrouponIdList

#����������֧����β�������״̬Ϊ2�Ĵ����ŵ���ID��
def getWaitOpenedGrouponIdByStatusAndPayedFlag(payedflag=True):
    logger.info("get all GrouponId  by payedflag......")
    GrouponIdList = []
    conn = dbService.connectMySqlServerDb(config['dbServerHost'],config['dbName'],config['dbUser'],config['dbPassword'])
    cursor = dbService.getCursor(conn)
    if payedflag:
        query = '''select groupon_id from groupon where flag=1 and groupon_status=2 and groupon_id in 
                   ( SELECT groupon_id FROM wx_talkbee_order WHERE order_status = 2 AND order_genre = 3 group by groupon_id ) limit 1'''
    else:
        query ='''select groupon_id from groupon where flag=1 and groupon_status=2 and groupon_id not in 
                   ( SELECT groupon_id FROM wx_talkbee_order WHERE order_status = 2 AND order_genre = 3 group by groupon_id ) limit 1'''
    cursor.execute(query)
    rows =cursor.fetchall()
    for row in rows:
        GrouponIdList.append(row[0])
    dbService.closeDbConn(conn)
    return GrouponIdList

#����ָ������ָ���γ̰��µĲ�������ɸѡ
def getGrouponIdByMaxUserCount(MaxUserCount=None,packageid=None):
    logger.info("get all GrouponId  by maxUserCount......")
    GrouponIdList = []
    conn = dbService.connectMySqlServerDb(config['dbServerHost'],config['dbName'],config['dbUser'],config['dbPassword'])
    cursor = dbService.getCursor(conn)
    query ='''select groupon_id from groupon where package_id='%s' and groupon_status='2' and groupon_id in (select groupon_id from groupon_user where speed='1' and user_state='1' group by  groupon_id HAVING count(ln_user_id)=%i)''' %(packageid,MaxUserCount)
    cursor.execute(query)
    rows =cursor.fetchall()
    for row in rows:
        GrouponIdList.append(row[0])
    dbService.closeDbConn(conn)
    return GrouponIdList

#�����ŵ��û�����user�����group�еĹ���ID
def getGrouponUserIdByGrouponStatus(GrouponStatus=None,packageid=None,sourceGrouponId=None):
    logger.info("get all GrouponUserId  by GrouponStatus......")
    GrouponUserIdList = []
    conn = dbService.connectMySqlServerDb(config['dbServerHost'],config['dbName'],config['dbUser'],config['dbPassword'])
    cursor = dbService.getCursor(conn)
    if GrouponStatus==None:
        query = '''select id from groupon_user where flag=1 and user_state='1' and groupon_id in (select groupon_id from groupon where flag=1 and package_id='%s' and groupon_id<>'%s')  limit 5''' %(packageid,sourceGrouponId)
    else:
        query ='''select  id from groupon_user where flag=1 and user_state='1' and groupon_id in (select groupon_id from groupon where flag=1 and package_id='%s' and groupon_status=%i and groupon_id<>'%s') limit 5''' %(packageid,GrouponStatus,sourceGrouponId)
    cursor.execute(query)
    rows =cursor.fetchall()
    for row in rows:
        GrouponUserIdList.append(row[0])
    dbService.closeDbConn(conn)
    return GrouponUserIdList


#���Ҵ���״̬��ֱ��ȯID
def getVoucherIdByVoucherStatus(VoucherStatus='1',overdueflag=0):
    logger.info("get VoucherId  by VoucherStatus......")
    VoucherIdList = []
    conn = dbService.connectMySqlServerDb(config['dbServerHost'],config['dbName'],config['dbUser'],config['dbPassword'])
    cursor = dbService.getCursor(conn)
    if overdueflag==0:
        query = '''select voucher_id from ln_user_voucher where flag=1 and voucher_status=%s and failure_time>now() limit 1''' %(VoucherStatus)  #����δ����ȯ
    else:
        query = '''select voucher_id from ln_user_voucher where flag=1 and voucher_status=%s and failure_time<now() limit 1''' % (VoucherStatus)  #���ҹ���ȯ
    cursor.execute(query)
    rows =cursor.fetchall()
    for row in rows:
        VoucherIdList.append(row[0])
    dbService.closeDbConn(conn)
    return VoucherIdList

#���Ҵ���״̬���Ż�ȯID
def getCouponsIdByStatus(is_use='0',rule_type=1,is_new=2,overdueflag=0):
    logger.info("get CouponsId  by Status......")
    CouponsIdList = []
    conn = dbService.connectMySqlServerDb(config['dbServerHost'],config['dbName'],config['dbUser'],config['dbPassword'])
    cursor = dbService.getCursor(conn)
    if overdueflag==0:
        query = '''select id from wx_coupons_info where flag=1 and is_use=%s and rule_type=%i and is_new=%i and failure_time>now() limit 1''' %(is_use,rule_type,is_new)  #����flag=1Ϊ��Ч���Ż�ȯ
    else:
        query = '''select id from wx_coupons_info where flag=1 and is_use=%s and rule_type=%i and is_new=%i and failure_time<now() limit 1''' % (is_use, rule_type, is_new)  # ����flag=1Ϊ��Ч���Ż�ȯ
    cursor.execute(query)
    rows =cursor.fetchall()
    for row in rows:
        CouponsIdList.append(row[0])
    dbService.closeDbConn(conn)
    return CouponsIdList

#���ݴ���������ѯ�Ƿ��ѱ����۹���ԤԼID��
def getAppointmentIdByStatus(Wx_open_id,Status,commentedflag):
    logger.info("get appointmentID  by Status......")
    IdList = []
    conn = dbService.connectMySqlServerDb(config['dbServerHost'],config['dbName'],config['dbUser'],config['dbPassword'])
    cursor = dbService.getCursor(conn)
    if commentedflag==1: #�����ѱ����۵�
        query = '''select id from appointment where ln_user_id = (select ln_user_id from ln_user_wx_relation where wx_open_id='%s')
                   and  status=%i and id in (select appointment_id from classes_schedules_comment WHERE comment_type=1 and appointment_id is not null)  limit 2''' %(Wx_open_id,Status)  #Status=2Ϊ�Ѿ��Ͽε�ԤԼ��
    else:  #����δ�����۵�
        query = '''select id from appointment where ln_user_id = (select ln_user_id from ln_user_wx_relation where wx_open_id='%s')
                      and  status=%i and id not in (select appointment_id from classes_schedules_comment WHERE comment_type=1 and appointment_id is not null)  limit 2''' % (Wx_open_id, Status)  # Status=2Ϊ�Ѿ��Ͽε�ԤԼ��
    cursor.execute(query)
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)
    return IdList

#��ѯ�ҵ�ԤԼ��¼����
def getAppointmentCountByStatus(Wx_open_id,Status,start_time,end_time):
    logger.info("get appointmentID  by Status......")
    IdList = []
    conn = dbService.connectMySqlServerDb(config['dbServerHost'],config['dbName'],config['dbUser'],config['dbPassword'])
    cursor = dbService.getCursor(conn)
    query = '''select count(id) from appointment where ln_user_id = (select ln_user_id from ln_user_wx_relation where wx_open_id='%s')
                   and  status=%i and start_time>='%s' and start_time<='%s' ''' %(Wx_open_id,Status,start_time,end_time)  #Status=2Ϊ�Ѿ��Ͽε�ԤԼ��
    cursor.execute(query)
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)
    return IdList

#���ݴ���������ѯֱ���εĿν�ID����Ӧ��teacher_id
def getScheduleIdByTimePeriod(starttime):
    logger.info("get schedule_id, teacher_id by Status......")
    IdList = []
    conn = dbService.connectMySqlServerDb(config['dbServerHost'],config['dbName'],config['dbUser'],config['dbPassword'])
    cursor = dbService.getCursor(conn)
    query = '''select schedule_id,teacher_id from classes_schedules where flag=1 and start_time >="%s" and content_type='2' limit 2 ''' %(starttime)  #Status=2Ϊ�Ѿ��Ͽε�ԤԼ��
    cursor.execute(query)

    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row)
    dbService.closeDbConn(conn)
    return IdList


#���ݴ���������ѯ��ʦ�������
def getTeacherAttendanceDetailByStatus(startTime,isWork=None,isLate=None,exitCount=1):
    logger.info("get TeacherAttendance by Status......")
    IdList = []
    conn = dbService.connectMySqlServerDb(config['dbServerHost'],config['dbName'],config['dbUser'],config['dbPassword'])
    cursor = dbService.getCursor(conn)
    if (isWork==2 and isLate== None) :
        query = '''select  count(*) from classes_schedules a,eeo_member_time_details b  
                   where a.schedule_id = b.schedule_id and b.type=2 and b.flag=1
                   and a.start_time >="%s" and b.id in (select mid from eeo_member_time_details_all)''' % (startTime)
    elif isWork==1:#δ���ڵ�����£�����ֱ�Ӳ�ѯ���ʱ���ȱ����Ϣ
        query = '''select  count(*) from classes_schedules a,eeo_member_time_details b  
                   where a.schedule_id = b.schedule_id and b.type=2 and b.flag=1
                   and a.start_time >="%s" and b.id not in (select mid from eeo_member_time_details_all)''' % (startTime)
    else: #���ڵ�����£���ϸ�ֲ�ѯ
        #isLate(isWorkΪ2ʱ���ֶβ���Ч���� isLate Ϊ1���ٵ� ��isLate Ϊ2������ ��isLate Ϊ3���ٵ�������)
        if exitCount==1:
            tmpstr=" (select mid from eeo_member_time_details_all group by mid having COUNT(mid) = %i )" %(exitCount)
        else:
            tmpstr = "( select mid from eeo_member_time_details_all group by mid having COUNT(mid) >= %i )" % (exitCount)

        if isLate==1:

            query = '''select  count(*) from classes_schedules a,eeo_member_time_details b  
                       where b.valid_time > DATE_ADD(a.start_time ,INTERVAL 1 MINUTE)  and a.schedule_id = b.schedule_id and b.type=2 and b.flag=1
                       and a.start_time >="%s" and b.id in %s ''' %(startTime,tmpstr)  #type=2Ϊ��ʦ�Ŀ�����Ϣ

        elif isLate==2:
            query = '''select  count(*) from classes_schedules a,eeo_member_time_details b  
                       where b.last_exit_time < a.end_time and a.schedule_id = b.schedule_id and b.type=2 and b.flag=1
                       and a.start_time >="%s" and b.id in %s''' %(startTime,tmpstr)
        elif isLate==3:
            query = '''select  count(*) from classes_schedules a,eeo_member_time_details b  
                       where a.schedule_id = b.schedule_id and b.type=2 and b.flag=1
                       and a.start_time >="%s"  and (b.last_exit_time < a.end_time or  b.valid_time > DATE_ADD(a.start_time ,INTERVAL 1 MINUTE) ) 
                       and id in %s '''  %(startTime,tmpstr)


    cursor.execute(query)
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)
    return IdList


#ɾ�����۹���ԤԼ��¼��������ԤԼ���Է�������
def DelCommentByAppointmentId(appointment_id=None):
    logger.info("��ʼɾ�����۹���ԤԼ��¼��������ԤԼ���Է�������......")
    conn = dbService.connectMySqlServerDb(config['dbServerHost'],config['dbName'],config['dbUser'],config['dbPassword'])
    cursor = dbService.getCursor(conn)
    query = '''delete from classes_schedules_comment where appointment_id='%s' '''  %(appointment_id)  #Status=2Ϊ�Ѿ��Ͽε�ԤԼ��
    cursor.execute(query)
    conn.commit()
    dbService.closeDbConn(conn)



#������Ч��classID
def getClassIdByParam(class_type=1,start_time=None):
    logger.info("get classId by class_type,start_time......")
    IdList = []
    conn = dbService.connectMySqlServerDb(config['dbServerHost'],config['dbName'],config['dbUser'],config['dbPassword'])
    cursor = dbService.getCursor(conn)
    query = '''select class_id from classes where flag=1 and begin_date >="%s" and class_type=%i limit 2 ''' %(start_time,class_type)  #class_type='1.1v1 2.1v4 3.lvn',
    cursor.execute(query)
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)
    return IdList

#������Ч�༶�ĵ�һ�ڿ�(���ۿν���Ч��Ч)�Ŀ�ʼʱ��
def getClassinfoByClassid(classid):
    logger.info("get start_time by class_id......")
    IdList = []
    conn = dbService.connectMySqlServerDb(config['dbServerHost'],config['dbName'],config['dbUser'],config['dbPassword'])
    cursor = dbService.getCursor(conn)
    query = '''select start_time,end_time from classes_schedules where classid="s%" and  schedule_type <>3 order by start_time limit 1''' %(classid)  #class_type='1.1v1 2.1v4 3.lvn',
    cursor.execute(query)
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)
    return IdList

#������Ч��ERPclassID
def GetERPClassIdByParam(create_time=None):
    logger.info("get all erp_class_id...")
    IdList = []
    conn = dbService.connectMySqlServerDb(config['dbServerHost'],config['dbName'],config['dbUser'],config['dbPassword'])
    cursor = dbService.getCursor(conn)
    query = '''select erp_class_id from erp_class_online where create_time>'%s' limit 1''' %(create_time)
    cursor.execute(query)
    rows =cursor.fetchall()

    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)
    return IdList

#----------------���°༶campus�鿴���ϼ�������Ӧ�Ŀν���------------ʹ��
def GetLessonCountByShiftID(shiftId=None):
    logger.info("get all lessonCount...")
    IdList = []
    conn = dbService.connectMySqlServerDb(config['dbServerHost'],config['dbName'],config['dbUser'],config['dbPassword'])
    cursor = dbService.getCursor(conn)
    query='''select count(*) from new_course_lesson a left join new_course b  on a.course_id = b.course_id 
             where b.books_serial_id = (select books_serial_id from erp_charge_gift where union_id='%s' and flag='1') and  a.flag=1 and a.push_status ='1' ''' %(shiftId)
    cursor.execute(query)
    rows =cursor.fetchall()

    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)
    return IdList[0]

#----------------���°༶campus�鿴���ϼ�������Ӧ���Ծ���------------ʹ��
def GetSerialExercisesCountByClassId(shiftId=None):
    logger.info("get all ExercisesCount...")
    IdList = []
    conn = dbService.connectMySqlServerDb(config['dbServerHost'],config['dbName'],config['dbUser'],config['dbPassword'])
    cursor = dbService.getCursor(conn)
    query='''select  count(*) from books_serial_outline where outline_type='2' and serial_id=
          (select books_serial_id from erp_charge_gift where union_id='%s' and flag='1')''' %(shiftId)
    cursor.execute(query)
    rows =cursor.fetchall()

    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)
    return IdList[0]

#----------------���°༶�鿴-�ѿ�����������Ƿ��Ѿ�ѡ���˵�����------------ʹ��
def GetSelectedCountByPeriod(beginTime,endTime,choiceType):
    logger.info("get all selectTotal...")
    IdList = []
    conn = dbService.connectMySqlServerDb(config['dbServerHost'],config['dbName'],config['dbUser'],config['dbPassword'])
    cursor = dbService.getCursor(conn)
    query='''select  count(*) from erp_class_student_down_line where create_time>='%s' and create_time<='%s' and flag='1' and  
    class_id in (SELECT c.class_id from classes c LEFT JOIN
     (SELECT class_id,MIN(start_time) firstTime from classes_schedules WHERE flag=1 GROUP BY class_id) s on c.class_id=s.class_id
     WHERE s.firstTime<=NOW() and c.flag=1) and erp_class_id not in (select test_data_id from test_data_info where data_type=2 ) and 
     erp_student_id not in (select test_data_id from test_data_info where data_type=3)''' %(beginTime,endTime)
    cursor.execute(query)
    rows =cursor.fetchall()

    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)
    return IdList[0]

#----------------���°༶�鿴-ת���ϵ�������-��Ӧ�����°༶�б�------------ʹ��
def GetErpClassListForRetainStudentByPeriod(beginTime,endTime,flag):
    logger.info("get all ErpClassList...")
    IdList = []
    conn = dbService.connectMySqlServerDb(config['dbServerHost'],config['dbName'],config['dbUser'],config['dbPassword'])
    cursor = dbService.getCursor(conn)
    query = '''select  distinct erp_class_id from erp_class_online_student where create_time>='%s' and create_time<='%s'  and flag=%s 
    and erp_class_id not in (select test_data_id from test_data_info where data_type=2 ) and erp_student_id not in (select test_data_id from test_data_info where data_type=3)''' % (beginTime, endTime,flag)

    cursor.execute(query)
    rows =cursor.fetchall()

    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)
    return IdList

#----------------���°༶�鿴-ת���ϵ�������-��Ӧ�ġ����°༶��-����/δ����İ༶�б�------------ʹ��

#----------------���°༶�鿴-�����ѿ���/δ�����Ӧ��ѧ������ת���Ϻ��ѡ��/δѡ�������------------ʹ��
def GetJoinClassTotalByClassList(ERPClassStr,join_type):
    logger.info("get all JoinClass...")
    IdList = []
    conn = dbService.connectMySqlServerDb(config['dbServerHost'],config['dbName'],config['dbUser'],config['dbPassword'])
    cursor = dbService.getCursor(conn)
    if join_type==None: #δѡ��
        query = '''select count(distinct erp_class_id,ln_user_id) from erp_class_online_student a where erp_class_id in (%s) and flag='1' 
        and concat(erp_class_id,ln_user_id) not in (select concat(erp_class_id,ln_user_id) from erp_class_student_down_line where flag='1' group by erp_class_id,ln_user_id)
        and  erp_student_id not in (select test_data_id from test_data_info where data_type=3)  ''' % (ERPClassStr)
    elif join_type=='0': #��ѡ��
        query = '''select count(distinct erp_class_id,ln_user_id) from erp_class_student_down_line where erp_class_id in (%s)  and flag='1' and class_id is not null and 
        erp_student_id not in (select test_data_id from test_data_info where data_type=3)''' % (ERPClassStr)
    cursor.execute(query)
    rows =cursor.fetchall()

    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)
    return IdList[0]

#----------------���°༶�鿴-ת���ϵ�������-��Ӧ�ġ����°༶��-����/δ����İ༶--����------------ʹ��
def GetErpStudentCountbyClassID(beginTime, endTime,ERPClassIdStr):
    logger.info("get all StudentCount by erp class...")
    IdList = []
    conn = dbService.connectMySqlServerDb(config['dbServerHost'], config['dbName'], config['dbUser'],config['dbPassword'])
    cursor = dbService.getCursor(conn)
    query = '''select  count(distinct erp_class_id,ln_user_id) from erp_class_online_student where flag=1 and create_time>='%s' and create_time<='%s' and erp_class_id in (%s) 
    and erp_student_id not in (select test_data_id from test_data_info where data_type=3)''' % (beginTime, endTime,ERPClassIdStr)

    cursor.execute(query)
    rows =cursor.fetchall()

    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)
    return IdList


#----------------���°༶�鿴-ת����/����ת���ϵ�������------------ʹ��
def GetOnLineRetainTotalByPeriod(beginTime,endTime,flag):
    logger.info("get all onLineRetainTotal...")
    IdList = []
    conn = dbService.connectMySqlServerDb(config['dbServerHost'],config['dbName'],config['dbUser'],config['dbPassword'])
    cursor = dbService.getCursor(conn)
    if flag==None:
        query = '''select  distinct erp_class_id,ln_user_id,receipt_no from erp_class_online_student where create_time>='%s' and create_time<='%s' 
        and erp_student_id not in (select test_data_id from test_data_info where data_type=3)''' % (beginTime, endTime)
    elif flag=='1': #��ת�����ұ���ת����״̬����
        query = '''SELECT DISTINCT
                     erp_class_id,
                     ln_user_id,
                      receipt_no
                    FROM
                     erp_class_online_student a
                    WHERE
                     a.create_time >= '%s'
                    AND a.create_time <= '%s'
                    and CONCAT(receipt_no,ln_user_id) in(
                    SELECT CONCAT(receipt_no,ln_user_id) from erp_class_online_student WHERE flag='1'
                    ) and  a.erp_student_id not in (select test_data_id from test_data_info where data_type=3)''' % (beginTime, endTime )
    elif flag=='0': #��ת������������ת����״̬����
        query = '''SELECT DISTINCT
                     erp_class_id,
                     ln_user_id,
                     receipt_no 
                    FROM
                     erp_class_online_student a
                    WHERE
                     a.create_time >= '%s'
                    AND a.create_time <= '%s'
                    and CONCAT(receipt_no,ln_user_id) not in(
                    SELECT CONCAT(receipt_no,ln_user_id) from erp_class_online_student WHERE flag='1'
                    ) and a.erp_student_id not in (select test_data_id from test_data_info where data_type=3) ''' % (beginTime, endTime)
    cursor.execute(query)
    rows =cursor.fetchall()

    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)
    return IdList

#----------------���°༶�鿴-ת���Ϻ��ѡ��/δѡ�������------------ʹ��
def GetJoinClassTotalByPeriod(beginTime,endTime,join_type):
    logger.info("get all JoinClass...")
    IdList = []
    conn = dbService.connectMySqlServerDb(config['dbServerHost'],config['dbName'],config['dbUser'],config['dbPassword'])
    cursor = dbService.getCursor(conn)
    if join_type=='n': #δѡ��
        query = '''SELECT count(DISTINCT
                         erp_class_id,
                         ln_user_id )
                     FROM
                         erp_class_online_student a 
                     WHERE
                         a.create_time >= '%s' 
                         AND a.create_time <= '%s' 
                         AND CONCAT( erp_class_id, ln_user_id ) IN ( SELECT CONCAT( erp_class_id, ln_user_id ) FROM erp_class_online_student WHERE flag = 1 ) 
                         AND CONCAT( erp_class_id, ln_user_id ) not in ( SELECT CONCAT( erp_class_id, ln_user_id ) FROM erp_class_student_down_line WHERE flag = '1' AND class_id IS NOT NULL )
                         and a.erp_student_id not in (select test_data_id from test_data_info where data_type=3)''' % (beginTime, endTime)
    elif join_type=='y': #��ѡ��
        query = '''SELECT count(DISTINCT 
                        erp_class_id,
                        ln_user_id) 
                    FROM
                        erp_class_online_student a 
                    WHERE
                        a.create_time >= '%s' 
                        AND a.create_time <= '%s' 
                        AND CONCAT( erp_class_id, ln_user_id ) IN ( SELECT CONCAT( erp_class_id, ln_user_id ) FROM erp_class_online_student WHERE flag = 1 ) 
                        AND CONCAT( erp_class_id, ln_user_id ) IN ( SELECT CONCAT( erp_class_id, ln_user_id ) FROM erp_class_student_down_line WHERE flag = '1' AND class_id IS NOT NULL )
                        and  a.erp_student_id not in (select test_data_id from test_data_info where data_type=3)''' % (beginTime, endTime)
    cursor.execute(query)
    rows =cursor.fetchall()

    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)
    return IdList[0]

#----------------���°༶�鿴-ת���Ϻ��ѡ��-����״̬������ͳ��------------ʹ��
def GetJoinOnlineClassByClassStatus(beginTime,endTime,ClassStatus,flag):
    #classStatus=noStart,going,end �ֱ��ʾδ���Σ��Ͽ��У��ѽ��
    logger.info("get all JoinOnlineClassByClassStatus...")
    IdList = []
    conn = dbService.connectMySqlServerDb(config['dbServerHost'],config['dbName'],config['dbUser'],config['dbPassword'])
    cursor = dbService.getCursor(conn)
    if ClassStatus=='noStart': #δ����
        query = ''' 
         SELECT
             count( DISTINCT ( %s ) ) 
         FROM
             erp_class_online_student s
             LEFT JOIN (
             SELECT
                 l.class_id,
                 l.erp_class_id,
                 l.erp_student_id,
                 c.firstTime,
                 c.lastTime 
             FROM
                 erp_class_student_down_line l
                 LEFT JOIN (
                 SELECT
                     s.class_id,
                     MIN( s.start_time ) firstTime,
                     MAX( s.end_time ) lastTime 
                 FROM
                     classes_schedules s
                     LEFT JOIN classes c ON s.class_id = c.class_id 
                 WHERE
                     s.flag = 1 
                 GROUP BY
                     s.class_id 
                 ) c ON l.class_id = c.class_id where l.flag=1
             ) c ON CONCAT( s.erp_class_id, s.erp_student_id ) = CONCAT( c.erp_class_id, c.erp_student_id ) 
         WHERE
             s.create_time >= '%s' 
             AND s.create_time <= '%s' 
             AND s.flag = 1 
             AND c.firstTime > NOW( )  and 
             c.erp_class_id not in (select test_data_id from test_data_info where data_type=2)''' % (flag,beginTime, endTime)
    elif ClassStatus=='going': #�ѿ���δ����
        query = ''' 
         SELECT
             count( DISTINCT ( %s ) ) 
         FROM
             erp_class_online_student s
             LEFT JOIN (
             SELECT
                 l.class_id,
                 l.erp_class_id,
                 l.erp_student_id,
                 c.firstTime,
                 c.lastTime 
             FROM
                 erp_class_student_down_line l
                 LEFT JOIN (
                 SELECT
                     s.class_id,
                     MIN( s.start_time ) firstTime,
                     MAX( s.end_time ) lastTime 
                 FROM
                     classes_schedules s
                     LEFT JOIN classes c ON s.class_id = c.class_id 
                 WHERE
                     s.flag = 1 
                 GROUP BY
                     s.class_id 
                 ) c ON l.class_id = c.class_id where l.flag=1
             ) c ON CONCAT( s.erp_class_id, s.erp_student_id ) = CONCAT( c.erp_class_id, c.erp_student_id ) 
         WHERE
             s.create_time >= '%s' 
             AND s.create_time <= '%s' 
             AND s.flag = 1 
             AND c.firstTime <= NOW( ) and c.lastTime >=NOW( ) and 
             c.erp_class_id not in (select test_data_id from test_data_info where data_type=2) ''' % (flag,beginTime, endTime)
    elif ClassStatus=='end': #�ѽ��
        query = ''' 
         SELECT
             count( DISTINCT ( %s ) ) 
         FROM
             erp_class_online_student s
             LEFT JOIN (
             SELECT
                 l.class_id,
                 l.erp_class_id,
                 l.erp_student_id,
                 c.firstTime,
                 c.lastTime 
             FROM
                 erp_class_student_down_line l
                 LEFT JOIN (
                 SELECT
                     s.class_id,
                     MIN( s.start_time ) firstTime,
                     MAX( s.end_time ) lastTime 
                 FROM
                     classes_schedules s
                     LEFT JOIN classes c ON s.class_id = c.class_id 
                 WHERE
                     s.flag = 1 
                 GROUP BY
                     s.class_id 
                 ) c ON l.class_id = c.class_id where l.flag=1
             ) c ON CONCAT( s.erp_class_id, s.erp_student_id ) = CONCAT( c.erp_class_id, c.erp_student_id ) 
         WHERE
             s.create_time >= '%s' 
             AND s.create_time <= '%s' 
             AND s.flag = 1 
             AND c.lastTime <= NOW( ) and 
             c.erp_class_id not in (select test_data_id from test_data_info where data_type=2) ''' % (flag,beginTime, endTime)
    cursor.execute(query)
    rows =cursor.fetchall()

    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)
    return IdList[0]

#----------------���°༶ת���Ϲ���-ѧ�����ڰ༶���------------ʹ��
def GetErpclassinfoByUserId():
    logger.info("get erpclass by id")
    IdList = []
    conn = dbService.connectMySqlServerDb(config['dbServerHost'],config['dbName'],config['dbUser'],config['dbPassword'])
    cursor = dbService.getCursor(conn)

    query = ''' select erp_class_id,erp_student_id,ln_user_id from erp_class_student_down_line where flag=1 limit 1'''

    cursor.execute(query)
    rows =cursor.fetchall()

    for row in rows:
        IdList.append(row)
    dbService.closeDbConn(conn)
    return IdList[0]

#------------------------��������-----------------------------#
#��ѯ�ҵ�ԤԼ��ȴ��û�Ϲ���������(��ǰ��Ȩ�޵ļ���Χ,��ԤԼ���û�����ȡ����ȱ�ڵ��Ͽ�����)
def getLackAppointmentScheduleCountByStatus(Wx_open_id):
    logger.info("get AppointmentScheduleCount  by Status......")
    IdList = []
    conn = dbService.connectMySqlServerDb(config['dbServerHost'],config['dbName'],config['dbUser'],config['dbPassword'])
    cursor = dbService.getCursor(conn)
    query = '''SELECT count(DISTINCT b.schedule_lesson_id)
                    FROM
                     appointment a
                    LEFT JOIN classes_schedules b ON b.schedule_id = a.schedule_id
                    left join ln_user_vip_serial e on CONCAT(a.ln_user_id,a.serial_id) = concat(e.ln_user_id,e.books_serial_id)
                    WHERE
                     a.ln_user_id = (
                      SELECT
                       ln_user_id
                      FROM
                       ln_user_wx_relation
                      WHERE
                       wx_open_id = '%s'
                     )
                    AND a. STATUS IN ('3', '4')
                    and ((a.cancel_reason is null or a.cancel_reason =null) or a.cancel_reason=2)
                    AND a.flag = 1
                    AND a.type = 2
                    and e.effective_time >=now()
                    AND trim(b.schedule_lesson_id) NOT IN (
                     (
                      SELECT
                       trim(d.schedule_lesson_id)
                      FROM
                       appointment c
                      LEFT JOIN classes_schedules d ON d.schedule_id = c.schedule_id
                      WHERE
                       c.ln_user_id = (
                        SELECT
                         ln_user_id
                        FROM
                         ln_user_wx_relation
                        WHERE
                         wx_open_id = '%s'
                       )
                      AND c. STATUS IN ('1', '2')
                      AND c.flag = 1
                    AND c.type = 2
                     )
                    )'''  %(Wx_open_id,Wx_open_id)  #Status='ԤԼ״̬ 1.���Ͽ� 2.���Ͽ� 3.ȱϯ
    cursor.execute(query)
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)
    return IdList

#��ѯ�ҵ�δ�������Ծ���(��ǰ��Ȩ�޵ļ���Χ,��ԤԼ���û�����ȡ����ȱ�ڵ��Ͽ�����)
def getUserLackPapers(Wx_open_id):
    logger.info("get UserLackPapers  by Status......")
    IdList = []
    conn = dbService.connectMySqlServerDb(config['dbServerHost'],config['dbName'],config['dbUser'],config['dbPassword'])
    cursor = dbService.getCursor(conn)
    query = '''SELECT  count(distinct(object_id))  FROM ln_user_study_speed a
               left join (select papers_id,count(0) num from papers_user_answer  
                           where ln_user_id = (
                                              SELECT
                                               ln_user_id
                                              FROM
                                               ln_user_wx_relation
                                              WHERE
                                               wx_open_id = '%s'
                                             )
                           group by papers_id) b on a.object_id =b.papers_id
                WHERE
                    a.ln_user_id =(
                                              SELECT
                                               ln_user_id
                                              FROM
                                               ln_user_wx_relation
                                              WHERE
                                               wx_open_id = '%s'
                                             )      
                    AND a.flag = 1
                    AND a.type = 2 
                    and a.start_time <=now() 
                    and  (b.num=0 or b.num=null or b.num is null) '''  %(Wx_open_id,Wx_open_id)  # type=2��ʾ�Ծ�
    cursor.execute(query)
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)
    return IdList

#----------------΢�Ŷ˸������ĵ�ĳ�γ̴���µ��Ծ���������ѯ���ǿγ̴�ٵ��Ծ����Ǹ��˹������Ծ�------------ʹ��
def GetExercisesCountBySerialId(SerialId=None):
    logger.info("get all ExercisesCount...")
    IdList = []
    conn = dbService.connectMySqlServerDb(config['dbServerHost'],config['dbName'],config['dbUser'],config['dbPassword'])
    cursor = dbService.getCursor(conn)
    query='''select  count(*) from books_serial_outline where outline_type='2' and serial_id='%s' ''' %(SerialId)
    cursor.execute(query)
    rows =cursor.fetchall()

    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)
    return IdList[0]

#----------------΢�Ŷ˸������ĵ�ĳ�γ̴���µ��Ծ����������ѯ���ǿγ̴�ٵ��Ծ����Ǹ��˹������Ծ�------------ʹ��
def GetFinishedExercisesCountByUser(Wx_open_id,SerialId=None):
    logger.info("get all ExercisesCount...")
    IdList = []
    conn = dbService.connectMySqlServerDb(config['dbServerHost'],config['dbName'],config['dbUser'],config['dbPassword'])
    cursor = dbService.getCursor(conn)

    query = '''select  count(*) from books_serial_outline  where outline_type='2' and serial_id='%s' and object_id in 
    (select distinct papers_id from papers_user_answer where flag=1 and ln_user_id=(
                                              SELECT
                                               ln_user_id
                                              FROM
                                               ln_user_wx_relation
                                              WHERE
                                               wx_open_id = '%s'
                                             ))  ''' % (SerialId,Wx_open_id)

    cursor.execute(query)
    rows =cursor.fetchall()

    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)
    return IdList[0]

#----------------΢�Ŷ˸������ĵĲ鿴�Լ����°༶��Ӧ�����ϰ༶���������------------ʹ��
def GetleaveCountByUser(Wx_open_id,status):
    logger.info("get all cancel appointment")
    IdList = []
    conn = dbService.connectMySqlServerDb(config['dbServerHost'],config['dbName'],config['dbUser'],config['dbPassword'])
    cursor = dbService.getCursor(conn)
    if status=='4':
        query = ''' select COALESCE(SUM(a.leaveCount),0) from 
                    ( select ln_user_id,class_id,COUNT((`status`='%s' and cancel_reason=2) or null) leaveCount,count(`status` !=4 or null) validCount
                    from appointment where flag=1 and cancel_reason='2' and status='%s' 
                    and class_id in  ( select a.class_id from erp_class_student_down_line a 
 left join classes b on a.class_id=b.class_id where a.ln_user_id=(
                                                  SELECT
                                                   ln_user_id
                                                  FROM
                                                   ln_user_wx_relation
                                                  WHERE
                                                   wx_open_id = '%s'
                                                 )  and b.class_source='2') and ln_user_id=(
                                                  SELECT
                                                   ln_user_id
                                                  FROM
                                                   ln_user_wx_relation
                                                  WHERE
                                                   wx_open_id = '%s'
                                                 ) ) a where a.validCount>0 ''' % (status,status,Wx_open_id,Wx_open_id)
    else:
        query = ''' select COALESCE(SUM(a.lackCount),0) from 
                    (  select ln_user_id,class_id,COUNT((`status`='%s' ) or null) lackCount,count(`status` !=4 or null) validCount
                    from appointment where flag=1 
                    and class_id in ( select a.class_id from erp_class_student_down_line a 
 left join classes b on a.class_id=b.class_id where a.ln_user_id=(
                                                  SELECT
                                                   ln_user_id
                                                  FROM
                                                   ln_user_wx_relation
                                                  WHERE
                                                   wx_open_id = '%s'
                                                 )  and b.class_source='2') and ln_user_id=(
                                                  SELECT
                                                   ln_user_id
                                                  FROM
                                                   ln_user_wx_relation
                                                  WHERE
                                                   wx_open_id = '%s'
                                                 )   
 group by class_id ) a where a.validCount>0 ''' % (status,Wx_open_id,Wx_open_id)
    cursor.execute(query)
    rows =cursor.fetchall()

    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)
    return IdList[0]

#----------------����������------------ʹ��
#��ȡ���й���ʱ��Σ��԰�СʱΪ��λ
def getTeacherTotalWorkTimeCount(sStartTime,sEndTime,isFull):
    logger.info("get TeacherTotalWorkTime  by time......")
    IdList = []
    conn = dbService.connectMySqlServerDb(config['dbServerHost'],config['dbName'],config['dbUser'],config['dbPassword'])
    cursor = dbService.getCursor(conn)
    if isFull == None:
         query = '''select count(*) as worktime from teacher_work_time_stocks where start_time>='%s' and start_time<'%s' and flag=1 and teacher_id not in (select test_data_id from test_data_info where data_type=1) '''  %(sStartTime,sEndTime)
    else:
        query = '''select count(*) as worktime from teacher_work_time_stocks where start_time>='%s' and start_time<'%s' and is_full=%s and flag=1 and teacher_id not in (select test_data_id from test_data_info where data_type=1) ''' % (sStartTime, sEndTime,isFull)
    cursor.execute(query)
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)
    return IdList

#��ȡ�����ʦ����״̬��Сʱ�������Сʱ��
def getTeacherHoursCountByStatus(sStartTime,sEndTime,time_status):
    logger.info("get TeacherWorkTime  by Status......")
    IdList = []
    conn = dbService.connectMySqlServerDb(config['dbServerHost'],config['dbName'],config['dbUser'],config['dbPassword'])
    cursor = dbService.getCursor(conn)
    query = '''select count(*) as worktime from teacher_work_time_stocks where start_time>='%s' and start_time<'%s'  and time_status=%s and flag=1 and teacher_id not in (select test_data_id from test_data_info where data_type=1) '''  %(sStartTime,sEndTime,time_status)
    cursor.execute(query)
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)
    return IdList

#��ȡ�����ʦ����״̬��ȫְСʱ��
def getTeacherHoursCountByStatusAndisFull(sStartTime,sEndTime,time_status):
    logger.info("get TeacherWorkTime  by Status......")
    IdList = []
    conn = dbService.connectMySqlServerDb(config['dbServerHost'],config['dbName'],config['dbUser'],config['dbPassword'])
    cursor = dbService.getCursor(conn)
    query = '''select count(*) as worktime from teacher_work_time_stocks where start_time>='%s' and start_time<'%s'  and time_status=%s and 
    is_full ='2' and teacher_id not in (select test_data_id from test_data_info where data_type=1) '''  %(sStartTime,sEndTime,time_status)
    cursor.execute(query)
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)
    return IdList

#��ȡָ���������п��Ź���ʱ��ε���ʦ����
def getTeachersCountByOrgOrNationality(sStartTime,sEndTime,Name,type):
    logger.info("get OpenWorkPlanTeachers'Count  by orgid......")
    IdList = []
    conn = dbService.connectMySqlServerDb(config['dbServerHost'],config['dbName'],config['dbUser'],config['dbPassword'])
    cursor = dbService.getCursor(conn)
    if type==1: #type=1����ʾ��ĳ�����µ���ʦ����
        query = '''select count(distinct(a.teacher_id)) as count from teacher_work_time_stocks a  
                   left join teachers b on a.teacher_id = b.teacher_id 
                   left join organization c on b.org_id =c.org_id where a.start_time>='%s' and a.start_time<'%s' and c.org_name='%s'
                   and a.teacher_id not in (select test_data_id from test_data_info where data_type=1) '''  %(sStartTime,sEndTime,Name)
    elif  type==2:#type=2����ʾ��ĳ�����µ���ʦ����
        query = '''select count(distinct(a.teacher_id)) as count from teacher_work_time_stocks a  
                   left join teachers b on a.teacher_id = b.teacher_id where a.start_time>='%s' and a.start_time<'%s' and b.nationality='%s'
                   and a.teacher_id not in (select test_data_id from test_data_info where data_type=1) '''  %(sStartTime,sEndTime,Name)
    cursor.execute(query)
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)
    return IdList


#----------------����������������------------ʹ��


#----------------ֱ���νڱ���------------ʹ��
#��ȡĳʱ�����Ч��ֱ���ν���
def getScheduleInfoByDay(sStartTime,sEndTime,class_source,schedule_type):
    logger.info("get getScheduleInfo  by day......")
    IdList = []
    conn = dbService.connectMySqlServerDb(config['dbServerHost'],config['dbName'],config['dbUser'],config['dbPassword'])
    cursor = dbService.getCursor(conn)
    if schedule_type == None:
        if class_source==None:
            query = '''select count(schedule_id) as scheduleCount from classes_schedules a 
            where a.start_time>='%s' and a.start_time<'%s' and a.flag=1 and a.content_type='2'
            and a.teacher_id not in (select test_data_id from test_data_info where data_type=1) ''' % (
            sStartTime, sEndTime)
        elif class_source=='2': #���°༶
             query = '''select count(schedule_id) as scheduleCount from classes_schedules a 
             left join classes b on a.class_id=b.class_id where a.start_time>='%s' and a.start_time<'%s' and a.flag=1 and a.content_type='2'
             and b.source_id is not null
             and a.teacher_id not in (select test_data_id from test_data_info where data_type=1) '''  %(sStartTime,sEndTime)
        elif class_source=='1':
             query = '''select count(schedule_id) as scheduleCount from classes_schedules a 
             left join classes b on a.class_id=b.class_id where a.start_time>='%s' and a.start_time<'%s' and a.flag=1 and a.content_type='2'
             and (b.source_id is null or b.source_id='')
             and a.teacher_id not in (select test_data_id from test_data_info where data_type=1) '''  %(sStartTime,sEndTime)
    else:
        if class_source==None:
           query = '''select count(schedule_id) as scheduleCount from classes_schedules where start_time>='%s' and start_time<'%s' 
           and schedule_type=%s and flag=1 and content_type='2' and 
           teacher_id not in (select test_data_id from test_data_info where data_type=1) ''' % (sStartTime, sEndTime,schedule_type)
        elif class_source=='2': #���°༶
            query = '''select count(schedule_id) as scheduleCount from classes_schedules a 
            left join classes b on a.class_id=b.class_id where a.start_time>='%s' and a.start_time<'%s' 
            and a.schedule_type=%s and a.flag=1 and a.content_type='2' and b.source_id is not null and 
            a.teacher_id not in (select test_data_id from test_data_info where data_type=1) ''' % (
            sStartTime, sEndTime, schedule_type)
        elif class_source == '1':  # ���ϰ༶
            query = '''select count(schedule_id) as scheduleCount from classes_schedules a 
            left join classes b on a.class_id=b.class_id where a.start_time>='%s' and a.start_time<'%s' 
            and a.schedule_type=%s and a.flag=1 and a.content_type='2' and (b.source_id is null or  b.source_id ='') and 
            a.teacher_id not in (select test_data_id from test_data_info where data_type=1) ''' % (
            sStartTime, sEndTime, schedule_type)

    cursor.execute(query)
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)
    return IdList


#��ȡĳʱ�����Ч��1V4ֱ���ν�ԤԼ������Ҫ��ԤԼ���л�ȡ��
def getScheduleStudentCountByDay(sStartTime,sEndTime,class_source,schedule_type):
    logger.info("get ScheduleStudentCount  by day......")
    IdList = []
    conn = dbService.connectMySqlServerDb(config['dbServerHost'],config['dbName'],config['dbUser'],config['dbPassword'])
    cursor = dbService.getCursor(conn)
    if schedule_type == None:
        if class_source==None:
            query = '''select count(ln_user_id) as StudentCount from appointment a left join classes_schedules b
            on a.schedule_id =b.schedule_id 
            where a.flag=1 and a.status <>4 and b.start_time>='%s' and b.start_time<'%s' and b.flag=1 and b.content_type='2'
            and b.teacher_id not in (select test_data_id from test_data_info where data_type=1) ''' % (sStartTime, sEndTime)
        elif class_source=='2': #���°༶
             query = '''select count(ln_user_id) as StudentCount from appointment a
             left join classes_schedules b  on a.schedule_id =b.schedule_id 
             left join classes c on b.class_id=c.class_id where a.flag=1 and a.status <>4 and b.start_time>='%s' and b.start_time<'%s' and b.flag=1 and b.content_type='2'
             and c.source_id is not null
             and b.teacher_id not in (select test_data_id from test_data_info where data_type=1) '''  %(sStartTime,sEndTime)
        elif class_source=='1':
             query = '''select count(ln_user_id) as StudentCount from appointment a 
             left join classes_schedules b  on a.schedule_id =b.schedule_id 
             left join classes c on b.class_id=c.class_id 
             where a.flag=1 and a.status <>4 and b.start_time>='%s' and b.start_time<'%s' and b.flag=1 and b.content_type='2'
             and (c.source_id is null or c.source_id='')
             and b.teacher_id not in (select test_data_id from test_data_info where data_type=1) '''  %(sStartTime,sEndTime)
    else:
        if class_source==None:
            query = '''select count(ln_user_id) as StudentCount from appointment a 
            left join classes_schedules b on a.schedule_id =b.schedule_id 
            where a.flag=1 and a.status <>4 and b.start_time>='%s' and b.start_time<'%s' and b.flag=1 and b.content_type='2'
            and b.schedule_type='%s' and b.teacher_id not in (select test_data_id from test_data_info where data_type=1) ''' % (sStartTime, sEndTime,schedule_type)
        elif class_source=='2': #���°༶
             query = '''select count(ln_user_id) as StudentCount from appointment a 
             left join classes_schedules b  on a.schedule_id =b.schedule_id 
             left join classes c on b.class_id=c.class_id where a.flag=1 and a.status <>4 and b.start_time>='%s' and b.start_time<'%s' and b.flag=1 and b.content_type='2'
             and c.source_id is not null
             and b.schedule_type='%s' and b.teacher_id not in (select test_data_id from test_data_info where data_type=1) ''' % (sStartTime, sEndTime,schedule_type)
        elif class_source=='1':
             query = '''select count(ln_user_id) as StudentCount from appointment a 
             left join classes_schedules b  on a.schedule_id =b.schedule_id 
             left join classes c on b.class_id=c.class_id 
             where a.flag=1 and a.status <>4 and b.start_time>='%s' and b.start_time<'%s' and b.flag=1 and b.content_type='2'
             and (c.source_id is null or c.source_id='')
             and b.schedule_type='%s' and b.teacher_id not in (select test_data_id from test_data_info where data_type=1) ''' % (sStartTime, sEndTime,schedule_type)

    cursor.execute(query)
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)
    return IdList


#��ȡĳʱ�����Ч��1V4ֱ������λ����
def getScheduleQuotasCountByDay(sStartTime,sEndTime,class_source,schedule_type):
    logger.info("get getScheduleInfo  by day......")
    IdList = []
    conn = dbService.connectMySqlServerDb(config['dbServerHost'],config['dbName'],config['dbUser'],config['dbPassword'])
    cursor = dbService.getCursor(conn)
    if schedule_type == None:
        if class_source==None:
            query = '''select  IFNULL(sum(a.quotas),0) as ScheduleQuotasCount from classes_schedules a 
            where a.start_time>='%s' and a.start_time<'%s' and a.flag=1 and a.content_type='2'
            and a.teacher_id not in (select test_data_id from test_data_info where data_type=1) ''' % (
            sStartTime, sEndTime)
        elif class_source=='2': #���°༶
             query = '''select IFNULL(sum(a.quotas),0) as ScheduleQuotasCount  from classes_schedules a 
             left join classes b on a.class_id=b.class_id where a.start_time>='%s' and a.start_time<'%s' and a.flag=1 and a.content_type='2'
             and b.source_id is not null
             and a.teacher_id not in (select test_data_id from test_data_info where data_type=1) '''  %(sStartTime,sEndTime)
        elif class_source=='1':
             query = '''select  IFNULL(sum(a.quotas),0) as ScheduleQuotasCount  from classes_schedules a 
             left join classes b on a.class_id=b.class_id where a.start_time>='%s' and a.start_time<'%s' and a.flag=1 and a.content_type='2'
             and (b.source_id is null or b.source_id='')
             and a.teacher_id not in (select test_data_id from test_data_info where data_type=1) '''  %(sStartTime,sEndTime)
    else:
        if class_source==None:
           query = '''select IFNULL(sum(quotas),0) as ScheduleQuotasCount from classes_schedules where start_time>='%s' and start_time<'%s' 
           and schedule_type=%s and flag=1 and content_type='2' and 
           teacher_id not in (select test_data_id from test_data_info where data_type=1) ''' % (sStartTime, sEndTime,schedule_type)
        elif class_source=='2': #���°༶
            query = '''select  IFNULL(sum(a.quotas),0) as ScheduleQuotasCount from classes_schedules a 
            left join classes b on a.class_id=b.class_id where a.start_time>='%s' and a.start_time<'%s' 
            and a.schedule_type=%s and a.flag=1 and a.content_type='2' and b.source_id is not null and 
            a.teacher_id not in (select test_data_id from test_data_info where data_type=1) ''' % (
            sStartTime, sEndTime, schedule_type)
        elif class_source == '1':  # ���ϰ༶
            query = '''select  IFNULL(sum(a.quotas),0) as ScheduleQuotasCount from classes_schedules a 
            left join classes b on a.class_id=b.class_id where a.start_time>='%s' and a.start_time<'%s' 
            and a.schedule_type=%s and a.flag=1 and a.content_type='2' and (b.source_id is null or  b.source_id ='') and 
            a.teacher_id not in (select test_data_id from test_data_info where data_type=1) ''' % (
            sStartTime, sEndTime, schedule_type)

    cursor.execute(query)
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)
    return IdList

#��ȡĳʱ�����Ч����ʱ��������
def getTempScheduleStudentCountByDay(sStartTime,sEndTime,class_source,schedule_type):
    logger.info("get tempScheduleStudentCount  by day......")
    IdList = []
    conn = dbService.connectMySqlServerDb(config['dbServerHost'],config['dbName'],config['dbUser'],config['dbPassword'])
    cursor = dbService.getCursor(conn)
    if schedule_type == None:
        if class_source==None:
            query = '''select count(student_id) as StudentCount from classes_schedules_students a left join classes_schedules b
            on a.schedule_id =b.schedule_id 
            where a.flag=1 and a.identity=2 and b.start_time>='%s' and b.start_time<'%s' and b.flag=1 and b.content_type='2'  
            and b.teacher_id not in (select test_data_id from test_data_info where data_type=1) ''' % (sStartTime, sEndTime)
        elif class_source=='2': #���°༶
             query = '''select count(student_id) as StudentCount from classes_schedules_students a 
             left join classes_schedules b  on a.schedule_id =b.schedule_id 
             left join classes c on b.class_id=c.class_id where a.flag=1 and a.identity=1 and b.start_time>='%s' and b.start_time<'%s' and b.flag=1 and b.content_type='2'
             and c.source_id is not null
             and b.teacher_id not in (select test_data_id from test_data_info where data_type=1) '''  %(sStartTime,sEndTime)
        elif class_source=='1':
             query = '''select count(student_id) as StudentCount from classes_schedules_students a 
             left join classes_schedules b  on a.schedule_id =b.schedule_id 
             left join classes c on b.class_id=c.class_id 
             where a.flag=1 and a.identity=1 and b.start_time>='%s' and b.start_time<'%s' and b.flag=1 and b.content_type='2'
             and (c.source_id is null or c.source_id='')
             and b.teacher_id not in (select test_data_id from test_data_info where data_type=1) '''  %(sStartTime,sEndTime)
    else:
        if class_source==None:
            query = '''select count(student_id) as StudentCount from classes_schedules_students a left join classes_schedules b
            on a.schedule_id =b.schedule_id 
            where a.flag=1 and a.identity=1 and b.start_time>='%s' and b.start_time<'%s' and b.flag=1 and b.content_type='2'
            and b.schedule_type='%s' and b.teacher_id not in (select test_data_id from test_data_info where data_type=1) ''' % (sStartTime, sEndTime,schedule_type)
        elif class_source=='2': #���°༶
             query = '''select count(student_id) as StudentCount from classes_schedules_students a 
             left join classes_schedules b  on a.schedule_id =b.schedule_id 
             left join classes c on b.class_id=c.class_id where a.flag=1 and a.identity=1 and b.start_time>='%s' and b.start_time<'%s' and b.flag=1 and b.content_type='2'
             and c.source_id is not null
             and b.schedule_type='%s' and b.teacher_id not in (select test_data_id from test_data_info where data_type=1) ''' % (sStartTime, sEndTime,schedule_type)
        elif class_source=='1':
             query = '''select count(student_id) as StudentCount from classes_schedules_students a 
             left join classes_schedules b  on a.schedule_id =b.schedule_id 
             left join classes c on b.class_id=c.class_id 
             where a.flag=1 and a.identity=1 and b.start_time>='%s' and b.start_time<'%s' and b.flag=1 and b.content_type='2'
             and (c.source_id is null or c.source_id='')
             and b.schedule_type='%s' and b.teacher_id not in (select test_data_id from test_data_info where data_type=1) ''' % (sStartTime, sEndTime,schedule_type)

    cursor.execute(query)
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)
    return IdList


#��ȡĳʱ�����Ч�ĵ��ڶ����˵Ŀν���
def getAppointmentScheduleByStudentCount(sStartTime,sEndTime,class_source,schedule_type,StudentCount):
    logger.info("get AppointmentSchedule  by StudentCount......")
    IdList = []
    conn = dbService.connectMySqlServerDb(config['dbServerHost'],config['dbName'],config['dbUser'],config['dbPassword'])
    cursor = dbService.getCursor(conn)
    if schedule_type == None: #schedule_type �ν����ͣ�Ϊ2ʱ����ʾ1V4�Ŀν�
        if class_source==None:
            query = '''select count(ln_user_id) as StudentCount from appointment a left join classes_schedules b
            on a.schedule_id =b.schedule_id 
            where a.flag=1 and a.status <>4 and a.type=2 and b.start_time>='%s' and b.start_time<'%s' and b.flag=1 and b.content_type='2'
            and b.teacher_id not in (select test_data_id from test_data_info where data_type=1) 
            group by a.schedule_id having studentCount=%d ''' % (sStartTime, sEndTime,StudentCount)
        elif class_source=='2': #���°༶
             query = '''select count(ln_user_id) as StudentCount from appointment a
             left join classes_schedules b  on a.schedule_id =b.schedule_id 
             left join classes c on b.class_id=c.class_id where a.flag=1 and a.status <>4 and a.type=2 and b.start_time>='%s' and b.start_time<'%s' and b.flag=1 and b.content_type='2'
             and c.source_id is not null
             and b.teacher_id not in (select test_data_id from test_data_info where data_type=1) 
             group by a.schedule_id having studentCount=%d '''  %(sStartTime,sEndTime,StudentCount)
        elif class_source=='1':
             query = '''select count(ln_user_id) as StudentCount from appointment a 
             left join classes_schedules b  on a.schedule_id =b.schedule_id 
             left join classes c on b.class_id=c.class_id 
             where a.flag=1 and a.status <>4 and a.type=2 and b.start_time>='%s' and b.start_time<'%s' and b.flag=1 and b.content_type='2'
             and (c.source_id is null or c.source_id='')
             and b.teacher_id not in (select test_data_id from test_data_info where data_type=1) 
             group by a.schedule_id having studentCount=%d '''  %(sStartTime,sEndTime,StudentCount)
    else:
        if class_source==None:
            query = '''select count(ln_user_id) as StudentCount from appointment a 
            left join classes_schedules b on a.schedule_id =b.schedule_id 
            where a.flag=1 and a.status <>4 and a.type=2 and b.start_time>='%s' and b.start_time<'%s' and b.flag=1 and b.content_type='2'
            and b.schedule_type='%s' and b.teacher_id not in (select test_data_id from test_data_info where data_type=1) 
            group by a.schedule_id having studentCount=%d '''  %(sStartTime,sEndTime,schedule_type,StudentCount)
        elif class_source=='2': #���°༶
             query = '''select count(ln_user_id) as StudentCount from appointment a 
             left join classes_schedules b  on a.schedule_id =b.schedule_id 
             left join classes c on b.class_id=c.class_id where a.flag=1 and a.status <>4 and a.type=2 and b.start_time>='%s' and b.start_time<'%s' and b.flag=1 and b.content_type='2'
             and c.source_id is not null
             and b.schedule_type='%s' and b.teacher_id not in (select test_data_id from test_data_info where data_type=1) 
             group by a.schedule_id having studentCount=%d '''  %(sStartTime,sEndTime,schedule_type,StudentCount)
        elif class_source=='1':
             query = '''select count(ln_user_id) as StudentCount from appointment a 
             left join classes_schedules b  on a.schedule_id =b.schedule_id 
             left join classes c on b.class_id=c.class_id 
             where a.flag=1 and a.status <>4 and a.type=2 and b.start_time>='%s' and b.start_time<'%s' and b.flag=1 and b.content_type='2'
             and (c.source_id is null or c.source_id='')
             and b.schedule_type='%s' and b.teacher_id not in (select test_data_id from test_data_info where data_type=1) 
             group by a.schedule_id having studentCount=%d '''  %(sStartTime,sEndTime,schedule_type,StudentCount)

    cursor.execute(query)
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row)
    dbService.closeDbConn(conn)
    return len(IdList)

#��ȡĳʱ��˵�0�˿ν���
def getZeroStudentScheduleCount(sStartTime,sEndTime,class_source):
    logger.info("get AppointmentSchedule  by StudentCount......")
    IdList = []
    conn = dbService.connectMySqlServerDb(config['dbServerHost'],config['dbName'],config['dbUser'],config['dbPassword'])
    cursor = dbService.getCursor(conn)
    if class_source==None:
        query = '''select count(b.schedule_id) from classes_schedules b
        left join classes c on b.class_id=c.class_id  
        where b.start_time>='%s' and b.start_time<'%s' and b.flag=1 and b.content_type='2'
        and b.schedule_type=2 and b.teacher_id not in (select test_data_id from test_data_info where data_type=1) 
        and b.schedule_id  not in (select schedule_id  from appointment where flag=1 and status<>4 and type=2) '''  %(sStartTime,sEndTime)
    elif class_source=='2': #���°༶
        query = '''select count(b.schedule_id)  from classes_schedules b
             left join classes c on b.class_id=c.class_id  
             where b.start_time>='%s' and b.start_time<'%s' and b.flag=1 and b.content_type='2'
             and b.schedule_type=2 and b.teacher_id not in (select test_data_id from test_data_info where data_type=1) 
             and c.source_id is not null
             and b.schedule_id  not in (select schedule_id  from appointment where flag=1 and status<>4 and type=2) ''' % (sStartTime, sEndTime)

    elif class_source=='1':
         query = '''select count(b.schedule_id) from classes_schedules b
              left join classes c on b.class_id=c.class_id  
              where b.start_time>='%s' and b.start_time<'%s' and b.flag=1 and b.content_type='2'
              and b.schedule_type=2 and b.teacher_id not in (select test_data_id from test_data_info where data_type=1) 
              and  (c.source_id is null or c.source_id='')
              and b.schedule_id  not in (select schedule_id  from appointment where flag=1 and status<>4 and type=2) ''' % (sStartTime, sEndTime)
    cursor.execute(query)
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)
    return IdList
#=--------------������ֱ���νڱ���---------------ʹ��

#=--------------������ֱ��ѧԱ����---------------ʹ��
def getStudentCountFromDB(sStartTime,sEndTime,sStatus):
    logger.info("get studentCount'Count  by period......")
    IdList = []
    conn = dbService.connectMySqlServerDb(config['dbServerHost'],config['dbName'],config['dbUser'],config['dbPassword'])
    cursor = dbService.getCursor(conn)
    if sStatus=='0': #��ʾ��������ԤԼ��(ֻ��1V1��1V4)
        query = '''select count(distinct(a.ln_user_id)) as count from appointment a  
                   where a.start_time>='%s' and a.start_time<'%s'
                   and a.ln_user_id not in (select test_data_id from test_data_info where data_type=3) and (a.type=1 or a.type=2) and a.flag=1 '''  %(sStartTime,sEndTime)
    else: #��״̬��ѯ������'ԤԼ״̬ 1.���Ͽ� 2.���Ͽ� 3.ȱϯ 4.��ȡ��',��
        query = '''select count(distinct(a.ln_user_id)) as count from appointment a  
                    where a.start_time>='%s' and a.start_time<'%s'
                    and a.ln_user_id not in (select test_data_id from test_data_info where data_type=3) and (a.type=1 or a.type=2) 
                    and a.flag=1 and a.status='%s' ''' % (sStartTime, sEndTime, sStatus)

    cursor.execute(query)
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)
    return IdList


#=--------------������ֱ��ѧԱ����---------------ʹ��


#=--------------������ֱ���༶����---------------ʹ��
def getClassCountFromDB(sStartTime,sEndTime):
    logger.info("get ClassCount  by period......")
    IdList = []
    conn = dbService.connectMySqlServerDb(config['dbServerHost'],config['dbName'],config['dbUser'],config['dbPassword'])
    cursor = dbService.getCursor(conn)
    query = '''select count(distinct(a.class_id)) as count from classes a  
               where a.begin_date>='%s' and a.begin_date<'%s'
               and a.class_id not in (select test_data_id from test_data_info where data_type=4) and a.course_type=2 and a.flag=1 '''  %(sStartTime,sEndTime)
    cursor.execute(query)
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)
    return IdList

#K3�������ϻ���_getK3ConsumeCourseSummary
def getK3ConsumeCourseSummaryFromDB(sStartTime,sEndTime):
    logger.info("get K3ConsumeCourse  by period......")
    IdList = []
    conn = dbService.connectMySqlServerDb(config['dbServerHost'],config['dbName'],config['dbUser'],config['dbPassword'])
    cursor = dbService.getCursor(conn)
    query = '''SELECT
                    count( * ),
                    sum(truncate( ( total_money / c.voucher_number * b.amount ), 6 )) price  
                FROM
                    ln_user_voucher a
                    LEFT JOIN erp_class_online_student b ON a.source_id = b.id
                    LEFT JOIN erp_charge_gift c ON b.shift_id = c.union_id
                    LEFT JOIN (
                    SELECT
                        aa.appointment_id,
                        aa.voucher_id,
                        aa.flag 
                    FROM
                        appointment_time aa
                        LEFT JOIN appointment bb ON aa.appointment_id = bb.id 
                    WHERE
                        aa.flag = 1 
                        AND bb.flag = 1 
                        AND bb.STATUS IN ( 2, 3 ) 
                    GROUP BY
                        appointment_id 
                    ) d ON a.voucher_id = d.voucher_id
                    LEFT JOIN appointment e ON d.appointment_id = e.id 
                WHERE
                    a.voucher_status IN ( 3, 4, 5 ) 
                    AND a.flag = 1 
                    AND a.source_type = 5 
                    AND b.shift_type = 2 
                    AND e.start_time >= '%s' 
                    AND e.end_time <= '%s' 
                    AND c.flag = 1 '''  %(sStartTime,sEndTime)
    cursor.execute(query)
    rows =cursor.fetchall()
    for row in rows:
        IdList.append(row)
    dbService.closeDbConn(conn)
    return IdList

#=--------------������ֱ��ѧԱ����---------------ʹ��


#----------------΢�Ŷ˸������ĵĲ鿴�Լ����°༶��Ӧ�����ϰ༶ID------------ʹ��
def GetClassIdListByUser(Wx_open_id):
    logger.info("get all class by userid")
    IdList = []
    conn = dbService.connectMySqlServerDb(config['dbServerHost'],config['dbName'],config['dbUser'],config['dbPassword'])
    cursor = dbService.getCursor(conn)

    query = ''' select classe_id from classes_students where flag=1 and classe_id in ( select a.class_id from erp_class_student_down_line a 
 left join classes b on a.class_id=b.class_id where a.ln_user_id=(
                                                  SELECT
                                                   ln_user_id
                                                  FROM
                                                   ln_user_wx_relation
                                                  WHERE
                                                   wx_open_id = '%s'
                                                 )  and b.class_source='2')and student_id=(
                                              SELECT
                                               ln_user_id
                                              FROM
                                               ln_user_wx_relation
                                              WHERE
                                               wx_open_id = '%s'
                                             )  ''' % (Wx_open_id,Wx_open_id)

    cursor.execute(query)
    rows =cursor.fetchall()

    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)
    return IdList

#�����ݹ���ʹ�� ------------------------------ #�����ݹ���ʹ��
#��ȡǰ100����΢���û�ID��openID
def GetUserinfo(packageId=None):
    logger.info("get all WxUser...")
    IdList = []
    conn = dbService.connectMySqlServerDb(config['dbServerHost'],config['dbName'],config['dbUser'],config['dbPassword'])
    cursor = dbService.getCursor(conn)
    if packageId==None:
        query='''select ln_user_id,wx_open_id from ln_user_wx_relation order by rand() limit 20'''
    else:
        query = '''select ln_user_id,wx_open_id from ln_user_wx_relation where ln_user_id not in (select a.ln_user_id from groupon_user a,groupon b where a.groupon_id=b.groupon_id and b.package_id='%s' and b.flag=1) order by rand() limit 20''' %(packageId)
    cursor.execute(query)
    rows =cursor.fetchall()

    for row in rows:
        IdList.append(row)
    dbService.closeDbConn(conn)
    return IdList

def GetCouponsCodeByuserID(userId=None):
    logger.info("get all CouponsCodeByuserID...")
    IdList = []
    currenttime= time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    conn = dbService.connectMySqlServerDb(config['dbServerHost'],config['dbName'],config['dbUser'],config['dbPassword'])
    cursor = dbService.getCursor(conn)
    query = '''select id from wx_coupons_info where receive_ln_user =%s  and coupons_type=1 and rule_type=1 and is_use='0' and failure_time>'%s' limit 1''' %(userId,currenttime)
    cursor.execute(query)
    rows =cursor.fetchall()

    for row in rows:
        IdList.append(row[0])
    dbService.closeDbConn(conn)
    return IdList


#������ݹ���ʹ�� -------------------------------------- #������ݹ���ʹ��
def DelUserClassData(userId=None):
    logger.info("del user data...")
    conn = dbService.connectMySqlServerDb(config['dbServerHost'],config['dbName'],config['dbUser'],config['dbPassword'])
    cursor = dbService.getCursor(conn)
    query = '''delete from classes_schedules_students where student_id =%s  ''' %(userId)
    cursor.execute(query)

    query = '''delete from classes_schedules_students where student_id =%s  ''' %(userId)
    cursor.execute(query)



    dbService.closeDbConn(conn)


