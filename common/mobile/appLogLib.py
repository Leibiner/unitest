# -*- coding: UTF-8 -*-
from common.logLib import logLib
import inspect


class AppLoglib(logLib):
    def __init__(self, name):
        self.name = super().__init__(name)

    def raise_error(self, error_msg):
        errMsg = "<b>%s(%s)</b>   <font style='color:red;'>%s</font>" % \
                 (self.name, self.get_current_function_name(), error_msg)
        raise Exception(errMsg)

    def error(self, error_msg):
        errMsg = "<b>%s(%s)</b>   <font style='color:red;'>%s</font>" % \
                 (self.name, self.get_current_function_name(), error_msg)
        stack_init = inspect.stack()[-1][1]
        if not (stack_init.lower().find("pycharm") > -1 or stack_init.lower().find("nosetests") > -1):
            raise Exception(errMsg)
        else:
            self.logger.error(errMsg)
            try:
                if errMsg.find(r'/undefined/') < 0:
                    raise Exception(errMsg)
            except:
                raise Exception(errMsg)