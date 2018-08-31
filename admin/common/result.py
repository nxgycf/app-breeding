#coding:utf-8

'''
Created on 2017年2月13日
@author: shuai.chen
'''

import traceback
import json
import functools

from towgo.utils.extend import Odict
from towgo.log.log_util import CommonLog

def returns(need_login=False):
    '''
    @param need_login: 是否需要登录验证
    '''
    def _deco(func):
        @functools.wraps(func)
        def __deco(self):
            try:
                if need_login:
                    admin = self.get_session()
                    if not admin:
                        self.redirect('/admin')
                    else:
                        self.admin = Odict(json.loads(admin))
                        return func(self)
                else:
                    return func(self)        
            except:
                class_name = self.__class__.__name__.split('_')[0]
                CommonLog.error('%s error:%s'%(class_name,traceback.format_exc()))
                return self.render_html('admin/error.html',msg='server error!')
        return __deco
    return _deco
