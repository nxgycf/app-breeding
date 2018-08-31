# -*- coding: utf-8 -*-

'''
Created on 2018年5月18日

@author: shuai.chen

    https://blog.csdn.net/zhangsx101/article/details/52650630
'''

from datetime import datetime
import json
import os

from towgo.handler import TornadoHttpHandler
from towgo.msetting import settings
from towgo.utils import http_util

from app.common import constant
from app.common.result import returns, Result
from app.models.goods import GoodsInfo
from app.models.other import AvatarInfo
from app.models.user import UserGoods, UserDeliverAddress, UserInfo, DeliverInfo, UserPay, \
    WechatUser
from app.services.goods import GoodsService
from app.services.other import AvatarService
from app.services.user import DeliverService
from app.services.user import UserGoodsService, UserDeliverAddressService, UserInfoService, UserPayService, \
    WechatUserService
from base.cache import Cache

from app.common import alert
from common import keys
from utils import check


class UserRegister(TornadoHttpHandler):    
    """
    user register
    """
    
    def __init__(self, *args, **kwargs):
        super(UserRegister, self).__init__(*args, **kwargs)  
        self.cache = Cache()    
                
    @returns()
    def _get(self):
        alert = {'account':'','nickname':'', 'code':'', 
                 'password':'', 'vpassword':'', 'msg':''}
        return self.render_html('app/user_register.html', **alert)     
    
    @returns()
    def _post(self):
        account = self.get_argument('account', '')  
        code = self.get_argument('code', '')  
        nickname = self.get_argument('nickname', '')  
        password = self.get_argument('password', '')  
        vpassword = self.get_argument('vpassword', '')  
        
        alert = {'account':account,'nickname':nickname, 'code':code, 
                 'password':password, 'vpassword':vpassword, 'msg':''}
        if not check.check_account(account):
            alert.update({'account':'','msg':u"请输入有效手机号!"})
            return self.render_html('app/user_register.html', **alert) 
        if not code:
            alert.update({'code':'','msg':u"请输入验证码!"})
            return self.render_html('app/user_register.html', **alert) 
        
        register_code = "0" #self.cache.get(keys.VERIFY_CODE)
        if code != register_code:
            alert.update({'code':'','msg':u"验证码不正确!"})
            return self.render_html('app/user_register.html', **alert) 
        
        if not nickname:
            alert['msg'] = u"请输入昵称!"
            return self.render_html('app/user_register.html', **alert) 
        if not (check.check_password(password) or check.check_password(vpassword)):
            alert.update({'password':'','vpassword':'', 'msg':u"密码无效!"})
            return self.render_html('app/user_register.html', **alert)    
        if password != vpassword:
            alert.update({'vpassword':'', 'msg':u"两次密码不一致!"})
            return self.render_html('app/user_register.html', **alert)  

        user_service = UserInfoService(UserInfo)  
        if user_service.get(account=account):
            alert.update({'account':'', 'msg':u"该号码已注册!"})
            return self.render_html('app/user_register.html', **alert) 
         
        user = UserInfo()  
        user.id = 0
        user.account = account
        user.phone = account
        user.nickname = nickname
        user.password = check.get_password(password)      
          
        user_service.insert(user)  
        self.redirect('/app?index=2')  

class UserLogin(TornadoHttpHandler):
    
    @returns()
    def _get(self):
        alert = {'account':'', 'password':'', 'msg':''}
        return self.render_html('app/user_login.html', **alert)
    
    @returns()
    def _post(self):
        account = self.get_argument('account', '')  
        password = self.get_argument('password', '') 
        
        alert = {'account':account, 'password':password, 'msg':''}
        if not check.check_account(account):
            alert.update({'account':'', 'msg':u"请输入有效手机号!"})
            return self.render_html('app/user_login.html', **alert)  
        if not check.check_password(password):
            alert.update({'password':'', 'msg':u"密码无效!"})
            return self.render_html('app/user_login.html', **alert)  

        user_service = UserInfoService(UserInfo) 
        user = user_service.get(account=account)
        if not user:
            alert.update({'account':'', 'password':'', 'msg':u"账号不存在!"})
            return self.render_html('app/user_login.html', **alert)  
        if user.password != check.get_password(password):
            alert.update({'password':'', 'msg':u"密码不正确!"})
            return self.render_html('app/user_login.html', **alert)  
        
        #add session
        self.set_session(user.as_json())
        self.redirect('/app?index=2')           

class PersonalInfo(TornadoHttpHandler):
    
    @returns(need_login=True)
    def _get(self):
        user = self.user
        
        info = {}
        info['id'] = user.id
        info['account'] = user.account
        info['nickname'] = user.nickname
        info['phone'] = "{0}****{1}".format(user.phone[0:3], user.phone[7:])   

        info['avatar'] = ''
        if user.avatar_id:
            avatar = AvatarService(AvatarInfo).get(id=user.avatar_id)   
            info['avatar'] = os.path.join(settings.AVATAR_URL, avatar.filename) if avatar else ''        
                
        return self.render_html('app/user_info.html', **info)          

class ResetPassword(TornadoHttpHandler):

    @returns(need_login=True)
    def _get(self):
        alert = {'opassword':'', 'password':'', 'vpassword':'', 'msg':''}
        return self.render_html('app/reset_password.html', **alert)   
    
    @returns(need_login=True)
    def _post(self):
        opassword = self.get_argument('opassword', '') 
        password = self.get_argument('password', '')  
        vpassword = self.get_argument('vpassword', '')  
        
        alert = {'opassword':opassword, 'password':password, 'vpassword':vpassword, 'msg':''}
        if not (check.check_password(opassword) or check.check_password(password) or check.check_password(vpassword)):
            alert.update({'opassword':'', 'password':'', 'vpassword':'', 'msg':u"密码无效!"})
            return self.render_html('app/reset_password.html', **alert)  
        if password != vpassword:
            alert.update({'vpassword':'', 'msg':u"两次密码不一致!"})
            return self.render_html('app/reset_password.html', **alert)  
        
        if self.user.password != check.get_password(opassword):
            alert.update({'opassword':'', 'msg':u"原密码不正确!"})
            return self.render_html('app/reset_password.html', **alert)        

        user_service = UserInfoService(UserInfo) 
        user_service.update({'password':check.get_password(password)}, id=self.user.id)
        #add session
        self.user.password = password
        self.set_session(json.dumps(self.user))
        
        self.redirect('/app?index=2')         

class ForgetPassword(UserRegister):
    
    @returns()
    def _get(self):
        alert = {'account':'','code':'', 'password':'', 'vpassword':'', 'msg':''}
        return self.render_html('app/forget_password.html', **alert)  
        
    @returns()
    def _post(self):
        account = self.get_argument('account', '')
        code = self.get_argument('code', '')  
        password = self.get_argument('password', '')  
        vpassword = self.get_argument('vpassword', '')  
             
        alert = {'account':account,'code':code, 'password':password, 'vpassword':vpassword, 'msg':''}       
        if not check.check_account(account):
            alert.update({'account':'', 'msg':u"请输入有效手机号!"})
            return self.render_html('app/forget_password.html', **alert) 
        if not code:
            alert.update({'code':'', 'msg':u"请输入验证码!"})
            return self.render_html('app/forget_password.html', **alert) 
                
        forget_code = self.cache.get(keys.VERIFY_CODE)
        if code != forget_code:
            alert.update({'code':'', 'msg':u"验证码不正确!"})
            return self.render_html('app/forget_password.html', **alert) 
        
        if not (check.check_password(password) or check.check_password(vpassword)):
            alert.update({'password':'', 'vpassword':'', 'msg':u"密码无效!"})
            return self.render_html('app/forget_password.html', **alert) 
        if password != vpassword:
            alert.update({'vpassword':'', 'msg':u"两次密码不一致!"})
            return self.render_html('app/forget_password.html', **alert) 

        user_service = UserInfoService(UserInfo) 
        user = user_service.get(account=account)
        if not user:
            alert.update({'account':'', 'msg':u"账号不存在!"})
            return self.render_html('app/forget_password.html', **alert) 
                
        user_service.update({'password':check.get_password(password)}, id=self.user.id)

        self.redirect('/app?index=2')                
            
class UserLogout(TornadoHttpHandler):
    
    @returns(need_login=True)
    def _get(self):
        if self.user:
            self.session.remove()
        self.redirect('/app?index=2')   
    
class UserAddressList(TornadoHttpHandler):
    
    @returns(need_login=True)
    def _get(self):
        address_service = UserDeliverAddressService(UserDeliverAddress)  
        address_list = address_service.gets(user_id=self.user.id, status=1)
        
        default = None
        alist = []
        for item in address_list:
            d = {}
            d['id'] = item.id
            d['name'] = item.name
            d['phone'] = item.phone
            d['address'] = u'{0}{1}'.format(item.region_name, item.address)
            d['region_name'] = ''
            d['region_id'] = item.region_id
            if item.id == self.user.deliver_address_id:
                d['default'] = 1
                default = d
            else:  
                d['default'] = 0  
                alist.append(d)
               
        return self.render_html('app/address_list.html',li=alist, default=default)  
    
class UserAddAddress(TornadoHttpHandler):
    
    @returns(need_login=True)
    def _post(self):
        name = self.get_argument('name')     
        phone = self.get_argument('phone')    
        address = self.get_argument('address')  
        zip_code = self.get_argument('zip_code',0)    
        region_id = int(self.get_argument('region',0))
        region_name = self.get_argument('trigger','') 
        
        if not all([name, phone, address]):
            return self.render_html('app/alert.html', msg=u"请输入内容!") 

        if not all([region_id, region_name]):
            return self.render_html('app/alert.html', msg=u"请选择地区!")
               
        address_service = UserDeliverAddressService(UserDeliverAddress)  
        user_address = UserDeliverAddress()
        user_address.user_id = self.user.id
        user_address.name = name 
        user_address.phone = phone
        user_address.address = address
        user_address.zip_code = zip_code
        user_address.region_id = region_id
        user_address.region_name = region_name
        aid = address_service.insert(user_address)

        default = int(self.get_argument('check_box', 0))
        if self.user.deliver_address_id == 0 or default == 1: #设置默认地址
            user_service = UserInfoService(UserInfo)
            user_service.update({'deliver_address_id':aid}, id=self.user.id)
            
            # update session
            self.user.deliver_address_id = aid
            self.set_session(json.dumps(self.user))
                    
        self.redirect('/user/address_list')              

class UserEditAddress(TornadoHttpHandler):
        
    @returns(need_login=True)
    def _get(self):
        action = int(self.get_argument('action', 0))
        if action == 1:
            info = {'name':'', 'phone':'', 'address':'', 'id':0, 'default':0, 'action':1, 'region_id':0, 'region_name':''}
            return self.render_html('app/address_edit.html', **info) 
            
        address_id = int(self.get_argument('address_id', 0))
        if not address_id:
            return self.render_html('app/alert.html', msg=u"请选择地址!") 
        
        address_service = UserDeliverAddressService(UserDeliverAddress)  
        ua = address_service.get(id=address_id, status=1)
        if not ua:
            return self.render_html('app/alert.html', msg=u"该地址不存在!") 

        info = {'name':ua.name, 'phone':ua.phone, 'address':ua.address, 'id':ua.id, 'region_id':ua.region_id, 
                'region_name':ua.region_name, 'default': ua.id == self.user.deliver_address_id, 'action':0}
        return self.render_html('app/address_edit.html', **info) 
    
    @returns(need_login=True)
    def _post(self):
        address_id = int(self.get_argument('address_id',0))
        if not address_id:
            return self.render_html('app/alert.html', msg=u"请选择地址!") 
        
        address_service = UserDeliverAddressService(UserDeliverAddress)  
        user_address = address_service.get(id = address_id, status=1)
        if not user_address:
            return self.render_html('app/alert.html', msg=u"该地址不存在!") 

        name = self.get_argument('name')     
        phone = self.get_argument('phone')    
        address = self.get_argument('address')  
#         zip_code = self.get_argument('zip_code',0)    
        region_id = int(self.get_argument('region',0))
        region_name = self.get_argument('trigger','') 

        if not all([name, phone, address]):
            return self.render_html('app/alert.html', msg=u"请填写信息!")   
        
        if not all([region_id, region_name]):
            return self.render_html('app/alert.html', msg=u"请选择地区!")
        
        update_info = {'name':name, 'phone':phone, 'address':address, 'region_id':region_id, 'region_name':region_name}                
        address_service.update(update_info, id=address_id, status=1, user_id=self.user.id)
        
        default = int(self.get_argument('check_box', 0))
        if default == 1: #设置默认地址
            user_service = UserInfoService(UserInfo)
            user_service.update({'deliver_address_id':address_id}, id=self.user.id)
            
            # update session
            self.user.deliver_address_id = address_id
            self.set_session(json.dumps(self.user))
        
        self.redirect('/user/address_list')     

class UserRemoveAddress(TornadoHttpHandler):
    
    @returns(need_login=True)
    def _post(self):
        address_id = int(self.get_argument('address_id',0))         
        if not address_id:
            return self.render_html('app/alert.html', msg=u"请选择地址!")  
        
        address_service = UserDeliverAddressService(UserDeliverAddress)  
        user_address = address_service.get(id = address_id, status=1)
        if not user_address:
            return self.render_html('app/alert.html', msg=u"该地址不存在!")  
        
        if self.user.deliver_address_id == user_address.id:
            return self.render_html('app/alert.html', msg=u"默认地址不能删除!")  
        
        address_service.update({'status':0}, id = address_id, status=1, user_id=self.user.id)
        
        self.redirect('/user/address_list')           

class OrderList(TornadoHttpHandler):
    
    @returns(need_login=True)
    def _get(self):
        '''
            % for ele in order_list:
                <div class="goods-list">
                    <a href="/user/order_detail?order_id=${ele['order_id']}">
                        <div class="order-item">                
                            <li>
                                <img class="tp" src="${ele['avatar']}" alt="商品图片" >
                                <div class="to">
                                    <p class="name">${ele['goods_name']} <span class="num">X${ele['number']}</span></p><br/>
                                    <p class="brief">${ele['ftext']}</p><br/>
                                    
                                    % if ele['status'] == 1:
                                        <p class="breeding">${ele['stext']} &nbsp;&nbsp;&nbsp;<span class="brief">${ele['after']}</span></p>
                                    % else:
                                        <p class="delivered">${ele['stext']} &nbsp;&nbsp;&nbsp;<span class="brief">${ele['after']}</span></p>
                                    % endif 
                                </div>
                            </li>
                        </div>    
                    </a>
                </div>                
            % endfor
        '''
        return self.render_html('app/order_list.html')
                                
    @returns(need_login=True, rjson=True)
    def _post(self):
        status = int(self.get_argument('status', -1))
        status_list = [status] if status in [1, 2] else [1, 2, 3]
        
        user_goods_service = UserGoodsService(UserGoods)
        orders = user_goods_service.gets(user_id=self.user.id)   
        
        order_list = []
        for order in orders:  
            if order.status not in status_list:
                continue
                      
            d = {}
            d['order_id'] = order.id
            d['user_id'] = order.user_id
            d['goods_id'] = order.goods_id
            d['goods_name'] = order.goods_name
            d['number'] = order.number
            d['feed_day'] = order.feed_day
            d['deliver_date'] = str(order.deliver_date).split()[0]
#             d['create_date'] = order.create_date
            d['status'] = order.status

            goods = GoodsService(GoodsInfo).get(id=order.goods_id)
            d['brief'] = goods.brief
            d['type'] = goods.type
            
            d['avatar'] = ''            
            if goods.avatar_id:
                avatar = AvatarService(AvatarInfo).get(id=goods.avatar_id)   
                d['avatar'] = os.path.join(settings.AVATAR_URL, avatar.filename) if avatar else ''

            if order.status != 1:
                di = DeliverService(DeliverInfo).get(user_goods_id=order.id)    
                if di:
                    d['deliver_date'] = str(di.create_date).split()[0]
            
            ftext, stext, after = self.get_text(order, d['deliver_date'], goods.type)    
            d['ftext'] = ftext
            d['stext'] = stext
            d['after'] = after
                      
            order_list.append(d)  
        
        return Result(alert.SUCCESS, data=order_list[::-1])()
            
#         order_list = sorted(order_list, key=lambda x:x['create_date'])   
#         return self.render_html('app/order_list.html',order_list=order_list)  
    
    def get_text(self, order, deliver_date, gtype):
        feed_day = order.feed_day
        feeding_day = u"%d 天" % (datetime.now() - order.create_date).days
        t = 0 if feed_day == 0 else gtype
        
        ftext_data = {0:u"现货", 1:u"喂养周期 : %d 天" % feed_day, 
                      2:u"种植周期 : %d 天" % feed_day, 3:u"种植周期 : %d 天" % feed_day} 
        stext_data = {0:u"准备中", 1:u"喂养中", 2:u"种植中", 3:u"种植中"}  
        astext_data = {0:str(order.create_date).split()[0], 1:feeding_day, 2:feeding_day, 3:feeding_day}    
        
        ftext = ftext_data[t]
        if order.status == 1:
            stext, safter = stext_data[t], astext_data[t]
        elif order.status == 0:
            stext, safter = u"待支付", order.create_date
        else:    
            stext, safter = u"已发货", deliver_date
            
        return ftext, stext, safter

class OrderDetail(OrderList):     
    """
    order detail
    """
    @returns(need_login=True)
    def _get(self):
        order_id = int(self.get_argument('order_id', 0))
        if not order_id:
            return self.render_html('app/alert.html', msg=u"请选择订单!") 
        
        user_goods_service = UserGoodsService(UserGoods)
        order = user_goods_service.get(id=order_id)
        if not order:
            return self.render_html('app/alert.html', msg=u"该订单不存在!") 
        
        info = {}
        info['order_id'] = order.id
        info['code'] = order.code
        info['user_id'] = order.user_id
        info['goods_id'] = order.goods_id
        info['goods_name'] = order.goods_name
        info['number'] = order.number
        info['feed_day'] = order.feed_day
        info['deliver_date'] = str(order.deliver_date).split()[0]
        info['create_date'] = order.create_date
        info['status'] = order.status

        udas = UserDeliverAddressService(UserDeliverAddress)
        address = udas.get(id=order.deliver_address_id, status=1) or udas.get(id=order.deliver_address_id, status=0)
        
        info['name'] = address.name
        info['phone'] = address.phone
        info['address'] = u'{0}{1}'.format(address.region_name, address.address)
        info['zip_code'] = address.zip_code   

        goods = GoodsService(GoodsInfo).get(id=order.goods_id)
        info['type'] = goods.type
        
        info['avatar'] = ''
        if goods.avatar_id:
            avatar = AvatarService(AvatarInfo).get(id=goods.avatar_id)   
            info['avatar'] = os.path.join(settings.AVATAR_URL, avatar.filename) if avatar else ''
        
        info['goods_price'] = order.goods_price   
        info['amount'] = 0
        info['pay_date'] = '' 
        info['discount'] = 0
        pay = UserPayService(UserPay).get(user_goods_id=order_id)  
        if pay:
            info['amount'] = pay.amount 
            info['pay_date'] = pay.create_date
            info['discount'] = order.goods_price*order.number - pay.amount     

        info['express_name'] = ''
        info['express_no'] = ''                             
        if order.status != 1:
            di = DeliverService(DeliverInfo).get(user_goods_id=order_id)    
            if di:
                info['deliver_date'] = str(di.create_date).split()[0]
                info['express_name'] = di.express_name
                info['express_no'] = di.express_no                  

        ftext, stext, after = self.get_text(order, info['deliver_date'], goods.type)    
        info['ftext'] = ftext
        info['stext'] = stext
        info['after'] = after
              
        return self.render_html('app/order_detail.html',**info)  


# 微信登录
class WechatUserLogin(TornadoHttpHandler):   
    '''
    https://www.cnblogs.com/0201zcr/p/5131602.html
    '''
    
    @returns()
    def _get(self):
        code = self.get_argument('code', '').strip()
        if code:
            token_url = constant.WECHAT_TOKEN.format(constant.WBC['APPID'], 
                                                     constant.WBC['APPSECRET'], code)
            tinfo  = http_util.urllib_request(token_url)
            tinfo = json.loads(tinfo)
            if 'access_token' not in tinfo:
                return self.render_html('app/alert.html', msg=u"登录失败!") 
            
            token = tinfo['access_token']
            openid = tinfo['openid']
            
            uinfo_url = constant.WECHAT_USER_INFO.format(token, openid)
            uinfo = http_util.urllib_request(uinfo_url)
            uinfo = json.loads(uinfo)
            if 'openid' not in uinfo:
                return self.render_html('app/alert.html', msg=u"登录失败!") 
            
            uservice = WechatUserService(WechatUser)
            wechat_user = uservice.get(openid=openid)
            if not wechat_user:
                wechat_user = WechatUser()
                wechat_user.openid = openid
                wechat_user.nickname = uinfo['nickname']
                wechat_user.sex = uinfo['sex']
                wechat_user.province = uinfo['province']
                wechat_user.city = uinfo['city']
                wechat_user.country = uinfo['country']
                wechat_user.headimgurl = uinfo['headimgurl']
                uservice.insert(wechat_user)
                
                #add session
                self.set_session(wechat_user.as_json())
            else:
                info = {'nickname':uinfo['nickname'], 'sex':uinfo['sex'], 'province':uinfo['province'],
                        'city':uinfo['city'], 'country':uinfo['country'], 'headimgurl':uinfo['headimgurl']}  
                uservice.update(info, openid=openid)

                info['id'] = wechat_user.id
                info['openid'] = openid
                info['deliver_address_id'] = wechat_user.deliver_address_id

                #add session
                self.set_session(json.dumps(info))
                
        self.redirect('/app?index=2') 

class WechatUserInfo(TornadoHttpHandler):   
    
    @returns(need_login=True)
    def _get(self):
        user = self.user
        
        info = {}
        info['id'] = user.id
        info['openid'] = user.openid
        info['nickname'] = user.nickname
        info['avatar'] = user.headimgurl
                
        return self.render_html('app/wechat_user_info.html', **info)     
    