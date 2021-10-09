# -*- coding: utf-8 -*-
from testconfig import config

'''
    define some env type for test
'''
class envEnum(object):
    qa = "qa"
    qa1 = "qa1"
    online = "online"
    dev = "dev"

    curEnv = qa
    if "env" in config:
        curEnv = config['env']