# -*- coding: utf-8 -*-

import sys,os,time
import logging
from logging import handlers, config
import inspect
import importlib

try:
    # Add for dynamic log -- START
    curFilePath = os.path.dirname(os.path.abspath(__file__))
    stack_init = inspect.stack()[-1][1]
    if stack_init.lower().find("apitester-script.py") < 0:
        config.fileConfig(curFilePath + "data/automationtest_log.conf")

    # Instance one logger object
    logger = logging.getLogger('LBAuto')
    logger.setLevel(logging.INFO)
except:
    pass
importlib.reload(sys)   #没有这句，用例名称不会显示为实际运行的用例名称
#sys.setdefaultencoding('utf-8') #没有这句，日志报告打印不出内容  #Python3字符串默认编码unicode, 所以sys.setdefaultencoding也不存在了