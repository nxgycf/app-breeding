#coding:utf-8

'''
Created on 2017年1月4日
@author: shuai.chen
'''

import traceback

import json
import functools

from tornado import escape
from towgo.utils.extend import Odict
from towgo.log.log_util import CommonLog

from app.common import alert


#获取返回码对应信息
CODE_MSG_DATA = {}

def get_msg(code):
    """
    根据code获取返回message
    """
    global CODE_MSG_DATA
    if not CODE_MSG_DATA:
        obj = alert
        for attr in dir(obj):
            if not (attr.startswith('_') or attr.endswith('_MSG')):
                con = getattr(obj,attr)
                if isinstance(con,int):
                    CODE_MSG_DATA[con] = getattr(obj,"%s_MSG" % attr)    
                  
    return CODE_MSG_DATA.get(code,'')

def returns(need_login=False, rjson=False):
    '''
    @param need_login: 是否需要登录验证
    @param rjson: 返回JSON
    '''
    def _deco(func):
        @functools.wraps(func)
        def __deco(self):
            try:
                if need_login:
                    user = self.get_session()
                    if not user:
                        self.redirect('/user/login')
                    else:
                        self.user = Odict(json.loads(user))
                        return func(self)
                else:
                    return func(self)        
            except:
                class_name = self.__class__.__name__.split('_')[0]
                CommonLog.error('%s error:%s' % (class_name,traceback.format_exc()))
                if rjson:
                    return Result(alert.SERVER_ERROR)()
                else:
                    return self.render_html('app/alert.html',msg='server error!')
        return __deco
    return _deco

class Result(object):
    '''
    create response result
    '''
    
    def __init__(self, code=0, message='', data=None):
        self.code = code 
        self.message = message or get_msg(code)
        if data is not None:
            self.data = data 
            
    def __call__(self):
        return self.as_json()        
    
    def as_json(self):
        return escape.json_encode(self.__dict__)
    