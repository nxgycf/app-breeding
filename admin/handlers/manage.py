#coding:utf-8

'''
Created on 2017年2月13日
@author: shuai.chen
'''

from __future__ import absolute_import

import json
from towgo.handler import TornadoHttpHandler

from admin.models.admin import Admin
from admin.services.admin import AdminService

from admin.common.result import returns
from utils import check


class ModifyPasswordHandler(TornadoHttpHandler):
    
    @returns(need_login=True) 
    def _get(self):
        return self.render_html('admin/mod_pass.html', 
                    account = self.admin.account, name=self.admin.name,msg=None)
    
    @returns(need_login=True)        
    def _post(self):
        password = self.get_argument("password","")  
        password1 = self.get_argument("password1","")   
        password2 = self.get_argument("password2","")    
        
        if password == "" or password1 == "" or password2 == "":
            return self.render_html('admin/mod_pass.html', account = self.admin.account,
                                         name=self.admin.name, msg=u'密码不能为空!')             

        if password1 != password2:
            return self.render_html('admin/mod_pass.html', account = self.admin.account,
                                         name=self.admin.name, msg=u'两次密码不一致!')

        admin_service = AdminService(Admin)
        if check.get_password(password) != self.admin.password:
            return self.render_html('admin/mod_pass.html', account = self.admin.account,
                                         name=self.admin.name, msg=u'原密码不正确!') 
        
        p = check.get_password(password1)        
        admin_service.update({'password':p},id=self.admin.id)
        
        #update session
        self.admin.password = p
        self.set_session(json.dumps(self.admin), self.session.session_id)    
        
        return self.render_html('admin/mod_pass.html', account = self.admin.account, name = self.admin.name,
                    msg='OK!')
        
class AddAdminHandler(TornadoHttpHandler):

    @returns(need_login=True)  
    def _get(self):
        if self.admin.level < 3:
            return self.render_html('admin/error.html',msg="no permission!",
                        account='',password1='',password2='',name='',level='') 
        return self.render_html('admin/add_admin.html',msg=None,
                    account='',password1='',password2='',name='',level='') 
        
    @returns(need_login=True)  
    def _post(self):
        if self.admin.level < 3:
            return self.render_html('admin/error.html',msg="no permission!",
                        account='',password1='',password2='',name='',level='') 
        
        account = self.get_argument("account","")
        password1 = self.get_argument("password1","")  
        password2 = self.get_argument("password2","")  
        level = self.get_argument("level","")  
        name = self.get_argument("name","")  
        if account == "" or password1 == "" or password2 == "" or level == "":
            return self.render_html('admin/add_admin.html',msg=u"字段不能为空！",
                        account=account or '',password1= password1 or '',password2=password2 or '',
                        name=name or '',level=level or '') 
        
        if len(password1)< 6 or len(password1)>16:
            return self.render_html('admin/add_admin.html',msg=u"密码长度要求6-16位之间！",
                        account=account or '',password1= '',password2='',
                        name=name or '',level=level or '')           
        
        if password1 != password2:
            return self.render_html('admin/add_admin.html',msg=u"两次密码不一致！",
                        account=account or '',password1= '',password2='',
                        name=name or '',level=level or '')       

        if not check.check_account(account):
            return self.render_html('admin/add_admin.html',msg=u"账号必须为手机号！",
                        account=account or '',password1= password1 or '',password2=password2 or '',
                        name=name or '',level=level or '')         
            
        admin_service = AdminService(Admin)
        ad = admin_service.get(account=account)  
        if not ad:
            admin_service.insert({'account':account, 'password':check.get_password(password1), 
                       'level':int(level), 'name':name})
        else:
            return self.render_html('admin/add_admin.html', msg=u"该用户已存在!",
                        account=account or '',password1= password1 or '',password2=password2 or '',
                        name=name or '',level=level or '')   
        
        return self.render_html('admin/add_admin.html', msg="OK!",
                    account='',password1='',password2='',name='',level='') 
    
    
class LookAdminHandler(TornadoHttpHandler):

    def _post(self):
        return self._get()
            
    @returns(need_login=True)  
    def _get(self):
        if self.admin.level < 2:
            return self.render_html('admin/error.html',msg="no permission!") 
    
        admin_service = AdminService(Admin)
        li = admin_service.gets()

        return self.render_html('admin/look_admins.html', li=li,own=self.admin.account,
                                        level=self.admin.level) 
    
    
class DelAdminHandler(TornadoHttpHandler):

    def _get(self):
        return self._post()
            
    @returns(need_login=True) 
    def _post(self):
        if self.admin.level < 3:
            return self.render_html('admin/error.html',msg="no permission!") 
        
        admin_service = AdminService(Admin)
        account = self.get_argument("account","")
        if account != "":
            if account != self.admin.account:
                ad = admin_service.get(account=account)
                if ad:
                    admin_service.delete(ad)
        
        li = admin_service.gets()
        return self.render_html('admin/look_admins.html', li=li,own=self.admin.account,
                                        level=self.admin.level) 
        