# -*- coding: utf-8 -*-
# coding=utf-8
import time
import smtplib                         # 发送邮件模块
from email.mime.text import MIMEText   # 定义邮件内容
from email.header import Header        # 定义邮件标题
import os, sys

target_mail = sys.argv[1]
report_dir = sys.argv[2]
cur_env = sys.argv[3]

def send_mail(latest_report, target_mail, report_url, cur_env):
    f = open(latest_report, 'rb')
    str1 = f.readline().decode()
    str2 = str1
    while str1:
        str1 = f.readline().decode()
        if str1.find('Overview') > -1:
            continue
        str2 += str1
        if str1.find('<body>') > -1:
            str2 += '    <h1><a href="%s">点击查看详情</a><h1>\n' % report_url
        if str1.find('</section>') > -1:
            break
    str2 += '</body>\n</html>'
    mail_content = str2.encode()
    f.close()

    smtpserver = 'smtp.learningbee.net'
    # 发送邮箱用户名密码
    user = 'testmaster@learningbee.net'
    password = '!234qwer'
    # 发送和接收邮箱
    sender = 'testmaster@learningbee.net'
    target_mail = target_mail.split(',')
    receivers = target_mail
    # 发送邮件主题和内容
    subject = "【%s】API自动化测试报告" % cur_env
    # HTML邮件正文
    msg = MIMEText(mail_content, 'html', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = sender
    msg['To'] = ','.join(receivers)

    smtp = smtplib.SMTP_SSL(smtpserver, 465)
    # HELO 向服务器标识用户身份
    smtp.helo(smtpserver)
    # 服务器返回结果确认
    smtp.ehlo(smtpserver)
    # 登录邮箱服务器用户名和密码
    smtp.login(user, password)

    print("Send email start...")
    smtp.sendmail(sender, receivers, msg.as_string())
    smtp.quit()
    print("Email send end!")


if __name__ == '__main__':
    import requests,re
    server_host = 'http://192.168.12.2:8083/'
    # 上传文件到服务器
    file = {'file': open(report_dir, 'rb')}
    r = requests.post(server_host + 'upload', files=file)
    report_name = re.match('.*:\s(\d+\.html)', r.text).group(1)
    # 发送邮件报告
    send_mail(report_dir, target_mail, server_host+report_name, cur_env)