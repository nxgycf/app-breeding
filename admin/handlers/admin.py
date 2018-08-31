#coding:utf-8

'''
Created on 2017年2月13日
@author: shuai.chen
'''
from __future__ import absolute_import

from towgo.handler import TornadoHttpHandler
from towgo.utils.extend import Odict

from admin.common.result import returns
from admin.models.admin import Admin
from admin.services.admin import AdminService
from app.services.user import UserGoodsService
from app.models.user import UserGoods

from utils import check


class IndexHandler(TornadoHttpHandler):
    
    @returns()
    def _get(self):
        return self.render_html('admin/index.html',msg=None,account='')

class LoginHandler(TornadoHttpHandler):

    @returns()
    def _get(self):
        return self.render_html('admin/index.html',msg=None,account='')
            
    @returns()
    def _post(self):   
        account = self.get_argument('account')
        password = self.get_argument('password')
        
        if not account:
            return self.render_html('admin/index.html',msg=u'请输入账号!',account='')

        if not password:
            return self.render_html('admin/index.html',msg=u'请输入密码!',account=account or '')

        admin_service = AdminService(Admin)
        admin = admin_service.get(account=account)   

        if admin is None:
            return self.render_html('admin/index.html',msg=u'该用户不存在!',account=account or '')
        
        if check.get_password(password) != admin.password:
            return self.render_html('admin/index.html',msg=u'密码错误!',account=account or '')
        
        self.set_session(admin.as_json())                
        return self.render_html('admin/login.html',msg=None)
            
class MainHandler(TornadoHttpHandler):
    '''
    统计维度：
          x商品 领养只数 领养人数 喂养中 已发货
          ['goods_id', 'goods_name', 'count', 'sum']
    '''
    @returns(need_login=True)
    def _get(self):
        
        service = UserGoodsService(UserGoods)  
        feeding, delivered = service.get_count()
        
        d = {}
        for item in feeding:
            fd = {}
            fd['goods_id'] = item.goods_id
            fd['goods_name'] = item.goods_name
            fd['goods_sum'] = item.sum
            fd['user_number'] = item.count            
            fd['feeding_num'] = item.count
            fd['deliver_num'] = 0
            d[item.goods_id] = fd
            
        for item in delivered:
            if item.goods_id in d:
                d[item.goods_id]['goods_sum'] += item.sum
                d[item.goods_id]['user_number'] += item.count
                d[item.goods_id]['deliver_num'] = item.count
            else:
                dd = {}
                dd['goods_id'] = item.goods_id
                dd['goods_name'] = item.goods_name
                dd['goods_sum'] = item.sum
                dd['user_number'] = item.count
                dd['deliver_num'] = item.count
                dd['feeding_num'] = 0
                d[item.goods_id] = dd     
        
        return self.render_html('admin/main.html',name=self.admin.name, li=map(Odict,d.itervalues()))       
        
class LeftHandler(TornadoHttpHandler):
    
    @returns(need_login=True)
    def _get(self):    
        return self.render_html('admin/left.html',para=self.admin.level)  
             
class LogoutHandler(TornadoHttpHandler):
    
    @returns(need_login=True)
    def _get(self):
        if self.admin:
            self.session.remove()
        self.redirect('/admin')
        