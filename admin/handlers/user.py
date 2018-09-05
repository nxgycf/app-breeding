# -*- coding: utf-8 -*-

'''
Created on 2018年7月26日

@author: shuai.chen
'''

from __future__ import absolute_import

import os
import time

from towgo.handler import TornadoHttpHandler
from towgo.msetting import settings
from towgo.utils.extend import Odict

from admin.common.result import returns
from app.models.goods import GoodsInfo
from app.models.user import UserInfo, UserDeliverAddress, UserGoods, WechatUser
from app.services.goods import GoodsService
from app.services.user import UserInfoService, UserDeliverAddressService, UserGoodsService, \
    WechatUserService


class LookUsertHandler(TornadoHttpHandler):

    @returns(need_login=True)  
    def _get(self):
        return self.render_html('admin/look_user.html', uid='',account='',msg=u'请输入用户ID或用户账号!') 
            
    @returns(need_login=True)  
    def _post(self):
        user_id =  self.get_argument("uid", '')
        account = self.get_argument("account", '')
        user_info = None
        if len(user_id) > 0:
            user_info = UserInfoService(UserInfo).get(id=int(user_id))
        elif len(account) > 0:
            user_info = UserInfoService(UserInfo).get(account=account)
        else:
            return self.render_html('admin/look_user.html', uid='',account='',msg=u'请输入用户ID或用户账号!')      
            
        if user_info:
            uinfo = {}
            uinfo['user_id'] = user_info.id
            uinfo['account'] = user_info.account
            uinfo['nickname'] = user_info.nickname
            uinfo['phone'] = user_info.phone
            uinfo['deliver_address_id'] = user_info.deliver_address_id

            user_id = user_info.id
            user_adress = UserDeliverAddressService(UserDeliverAddress).gets(user_id=user_id, status=1)
            user_goods = UserGoodsService(UserGoods).gets(user_id=user_id)
                        
            ugl = []
            if user_goods:
                for item in user_goods:
                    d = {}
                    d['goods_id'] = item.goods_id
                    d['goods_name'] = item.goods_name
                    d['number'] = item.number
                    d['deliver_date'] = item.deliver_date
                    d['status'] = {1:u'待发货',2:u'已发货',3:u'已完成'}.get(item.status)
                    ugl.append(Odict(d))
                
            udal = []  
            if user_adress:
                for item in  user_adress:
                    d = {} 
                    d['name'] = item.name
                    d['phone'] = item.phone
                    d['address'] = u'{0}{1}'.format(item.region_name, item.address)
                    d['region_name'] = item.region_name
                    d['region_id'] = item.region_id
                    udal.append(Odict(d))
                
            uinfo['goods'] = ugl
            uinfo['address'] = udal    
    
            return self.render_html('admin/look_user.html',uid=user_id,msg=None,**uinfo) 
            
        return self.render_html('admin/look_user.html', uid=user_id,account=account,msg=u'该用户不存在!') 

class WechatUserHandler(TornadoHttpHandler):

    @returns(need_login=True)  
    def _get(self):
        return self.render_html('admin/wechat_user.html', uid='',msg=u'请输入用户ID!') 
            
    @returns(need_login=True)  
    def _post(self):
        user_id =  self.get_argument("uid", '')
        user_info = None
        if len(user_id) > 0:
            user_info = WechatUserService(WechatUser).get(id=int(user_id))
        else:
            return self.render_html('admin/wechat_user.html', uid='',msg=u'请输入用户ID!')      
            
        if user_info:
            uinfo = {}
            uinfo['user_id'] = user_info.id
            uinfo['nickname'] = user_info.nickname
            uinfo['deliver_address_id'] = user_info.deliver_address_id

            user_id = user_info.id
            user_adress = UserDeliverAddressService(UserDeliverAddress).gets(user_id=user_id, status=1)
            user_goods = UserGoodsService(UserGoods).gets(user_id=user_id)
                        
            ugl = []
            if user_goods:
                for item in user_goods:
                    d = {}
                    d['goods_id'] = item.goods_id
                    d['goods_name'] = item.goods_name
                    d['number'] = item.number
                    d['deliver_date'] = item.deliver_date
                    d['status'] = {1:u'待发货',2:u'已发货',3:u'已完成'}.get(item.status)
                    ugl.append(Odict(d))
                
            udal = []  
            if user_adress:
                for item in  user_adress:
                    d = {} 
                    d['name'] = item.name
                    d['phone'] = item.phone
                    d['address'] = u'{0}{1}'.format(item.region_name, item.address)
                    d['region_name'] = item.region_name
                    d['region_id'] = item.region_id
                    udal.append(Odict(d))
                
            uinfo['goods'] = ugl
            uinfo['address'] = udal    
    
            return self.render_html('admin/wechat_user.html',uid=user_id,msg=None,**uinfo) 
            
        return self.render_html('admin/wechat_user.html', uid=user_id,msg=u'该用户不存在!')         
            
class AdPicUploadHandler(TornadoHttpHandler):  

    def get_pics(self):
        ad_dir = os.path.join(settings.STATIC_PATH, 'image/ads/')
        pm = {}
        fs = os.listdir(ad_dir)
        for f in fs:
            fp = f.split('.')
            if fp[-1] in ['png', 'jpg', 'jpeg']:
                sp= fp[0].split('_')
                pm[int(sp[0])] = (f, int(sp[1]))
        
        pics = []
        for x in xrange(0, 5):
            if x in pm:
                pics.append((x, '../../static/image/ads/{0}'.format(pm[x][0]), pm[x][1], 1))
            else:
                pics.append((x, '../../static/image/null.png', 0, 0))    
        return pics        
       
    @returns(need_login=True)  
    def _get(self):
        pics = self.get_pics()
        return self.render_html('admin/ad_pics.html', pics=pics, msg=None) 
            
    @returns(need_login=True)  
    def _post(self):
        if self.admin.level < 2:
            return self.render_html('admin/error.html',msg="no permission!") 
        
        pics = self.get_pics()
        
        sign = int(self.get_argument("sign", 0))
        if sign == 1: #delete
            pic = self.get_argument("pic", '')
            if pic:
                pn = pic.split('/')[-1]
                os.remove(os.path.join(settings.STATIC_PATH, 'image/ads/{0}'.format(pn)))
        elif sign == 2: #upload
            pid = self.get_argument("pid", 0)
            gid = int(self.get_argument("gid", 0).strip() or 0)
            if gid != 0:
                goods = GoodsService(GoodsInfo).get(id=gid) 
                if not goods:
                    return self.render_string('admin/ad_pics.html', msg=u"该商品不存在!", pics=pics)    
            
            upload_file = self.request.files.get('file',None)
            if upload_file is None:
                return self.render_string('admin/ad_pics.html', msg=u"请选择要上传的文件!", pics=pics)   
    
            file_name = upload_file[0].get('filename')
            tp = file_name.split('.')[-1]
            if tp not in ['jpg', 'png', 'jpeg']:
                return self.render_string('admin/ad_pics.html', msg=u"需要上传 jpg/png/jpeg 文件!", pics=pics)   
    
            body =  upload_file[0].get('body')
            ts = time.time()
            f = os.path.join(settings.STATIC_PATH, 'image/ads/{0}_{1}_{2}.{3}'.format(pid, gid, str(int(ts)), tp))
            fname = os.path.join(settings.AVATAR_PATH, f)
            with open(fname,'w+') as _f:
                _f.write(body)
                _f.close()
        
        self.redirect('/admin/ad_pics')

            