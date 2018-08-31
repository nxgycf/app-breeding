#coding:utf-8

'''
Created on 2017年1月4日
@author: shuai.chen
'''

#这里只定义返回信息:  XXX = 0    \n    XXX_MSG = ""
SUCCESS = 0
SUCCESS_MSG = "success"

FAIL = -1
FAIL_MSG = "fail"

SERVER_ERROR = 9
SERVER_ERROR_MSG = "server error"

PARAMS_ERROR = 10000
PARAMS_ERROR_MSG = "params error"

NOT_LOGIN = 10001
NOT_LOGIN_MSG = u"尚未登录!"

INVALID_PHONE = 10002
INVALID_PHONE_MSG = u"请输入有效手机号!"

VERIFY_CODE_FAIL = 10003
VERIFY_CODE_FAIL_MSG = u"验证码发送失败!"

VERIFY_CODE_OP = 10003
VERIFY_CODE_OP_MSG = u"请勿频繁发送!"
