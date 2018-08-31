# -*- coding: utf-8 -*-

'''
Created on 2018年7月26日

@author: shuai.chen
'''

from __future__ import absolute_import

import math
import time

from towgo.handler import TornadoHttpHandler
from towgo.utils.extend import Odict

from admin.common import constants
from admin.common.result import returns
from app.models.user import DeliverInfo, UserDeliverAddress, UserGoods, UserPay
from app.services.user import DeliverService, UserGoodsService, UserPayService
from app.services.user import UserDeliverAddressService
from utils import time_util


class DeliverListHandler(TornadoHttpHandler):
    '''
    维度:
        用户ID 商品名称 数量 订购日期 出货日期 收货人姓名 收货人电话  收货地址  邮编  修改状态
    '''
    @returns(need_login=True) 
    def _get(self):
        return self._post()
            
    @returns(need_login=True)  
    def _post(self):
        goods_id = int(self.get_argument("goods_id",0))
        p = int(self.get_argument("p",1))
        sign = self.get_argument("sign","0")
        
        now = time.time()
        startdate = self.get_argument("startdate",time_util.to_str(now,ft="%Y-%m-%d"))
        if sign == "1":
            enddate = self.get_argument("enddate",time_util.to_str(now+3600*24*7,ft="%Y-%m-%d"))
            query_filed = 'deliver_date'
            status = 1 
        else:
            enddate = self.get_argument("enddate",time_util.to_str(now,ft="%Y-%m-%d"))
            query_filed = 'create_date' 
            status = 0
        
        service = UserGoodsService(UserGoods)  
        address_service = UserDeliverAddressService(UserDeliverAddress)
        li, num = service.get_by_date(goods_id, query_filed, status, startdate, enddate, p, constants.NUM_PER_PAGE)
        nl = []
        for item in li:
            d = {}
            d['order_id'] = item.id
            d['user_id'] = item.user_id
            d['goods_id'] = item.goods_id
            d['goods_name'] = item.goods_name
            d['number'] = item.number
            d['deliver_date'] = item.deliver_date
            d['create_date'] = item.create_date
            d['status'] = item.status
            d['status_text'] = {0:u"待支付", 1:u'待发货',2:u'已发货',3:u'已完成'}.get(item.status)
            
            address = (address_service.get(id=item.deliver_address_id, status=1) 
                       or address_service.get(id=item.deliver_address_id, status=0))
            d['name'] = address.name
            d['phone'] = address.phone
            d['address'] = u'{0}{1}'.format(address.region_name, address.address)
            d['zip_code'] = address.zip_code
            nl.append(Odict(d))

        tp = int(math.ceil(num*1.0/constants.NUM_PER_PAGE))
        return self.render_html('admin/deliver_list.html', li=nl, enddate=enddate, startdate=startdate,
                                goods_id=goods_id, cp=p, pages=range(1,tp+1) if tp>0 else [1], sign=sign,
                                today=time.strftime("%Y-%m-%d")) 

            
class DeliverHandler(TornadoHttpHandler):
    '''
    show fields: 用户ID 商品名称 数量 出货日期 收货人姓名 收货人电话  收货地址
    '''   
    
    @returns(need_login=True) 
    def _get(self):
        order_id =  self.get_argument("order_id",'')
        code = self.get_argument("code", '')
        ug = None
        if len(order_id) > 0:
            ug = UserGoodsService(UserGoods).get(id=int(order_id))
        elif len(code) > 0:    
            ug = UserGoodsService(UserGoods).get_by_code(code=code)
        else:    
            return self.render_html('admin/deliver.html', order_id='',code=code, msg=u'请输入订单ID 或 订单编号!')
        
        if not ug:
            return self.render_html('admin/deliver.html', order_id='', code=code, msg=u'该订单不存在!')
                        
        info = {}
        info['order_id'] = ug.id
        info['code'] = ug.code
        info['user_id'] = ug.user_id
        info['goods_id'] = ug.goods_id
        info['goods_name'] = ug.goods_name
        info['number'] = ug.number
        info['feed_day'] = ug.feed_day
        info['deliver_date'] = ug.deliver_date
        info['create_date'] = ug.create_date
        info['status'] = ug.status

        info['amount'] = ''
        info['pay_date'] = ''
        pay = UserPayService(UserPay).get(user_goods_id=order_id)  
        if pay:
            info['amount'] = pay.amount 
            info['pay_date'] = pay.create_date
            
        udas = UserDeliverAddressService(UserDeliverAddress)
        address = udas.get(id=ug.deliver_address_id, status=1) or udas.get(id=ug.deliver_address_id, status=0)
              
        info['name'] = address.name
        info['phone'] = address.phone
        info['address'] =  u'{0}{1}'.format(address.region_name, address.address)
        
        info['express_name'] = ''
        info['express_no'] = ''  
        info['li'] = []
                
        if ug.status == 1:
            info['li'] = [u'乐牧自送',u'顺丰快递',u'圆通快递',u'申通快递',u'中通快递',u'韵达快递',u'天天快递',u'邮政包裹']
        else:
            service = DeliverService(DeliverInfo)  
            di = service.get(user_goods_id=ug.id)    
            if di:
                info['deliver_date'] = di.create_date
                info['express_name'] = di.express_name
                info['express_no'] = di.express_no   
                  
        info['deliver_date'] = str(info['deliver_date']).split()[0]                     

        return self.render_html('admin/deliver.html', msg=None, today=time.strftime("%Y-%m-%d"), **info) 
            
    @returns(need_login=True)  
    def _post(self):
        if self.admin.level < 2:
            return self.render_html('admin/error.html',msg="no permission!")    
         
        express_name = self.get_argument("express_name")
        express_no = self.get_argument("express_no")
        order_id = self.get_argument("order_id")
        if not all([express_name, express_no, order_id]):
            return self.render_html('admin/error.html',msg="fields is required!")         
        
        ugs = UserGoodsService(UserGoods)
        ug = ugs.get(id=order_id)
           
        deliver_info = DeliverInfo()
        deliver_info.user_goods_id = order_id
        deliver_info.user_id = ug.user_id
        deliver_info.goods_id = ug.goods_id
        deliver_info.goods_name  = ug.goods_name
        deliver_info.number = ug.number
        deliver_info.express_name = express_name
        deliver_info.express_no = express_no
        deliver_info.deliver_address_id = ug.deliver_address_id
        deliver_info.status = 0
        
        ugs.deliver(deliver_info, {'status':2},**{'id':order_id})
        
        self.redirect('/admin/delivered_list')    

class DeliveredListHandler(TornadoHttpHandler):
    '''
    维度:
        用户ID 商品名称 数量 出货日期 收货人姓名 收货人电话  收货地址  快递名称  快递单号  收货状态
    '''
    @returns(need_login=True) 
    def _get(self):
        return self._post()
        
    @returns(need_login=True)  
    def _post(self):
        now = time.time()
        enddate = self.get_argument("enddate",time_util.to_str(now,ft="%Y-%m-%d"))
        startdate = self.get_argument("startdate",time_util.to_str(now-3600*24*7,ft="%Y-%m-%d"))
        goods_id = int(self.get_argument("goods_id",0))
        p = int(self.get_argument("p",1))
        
        service = DeliverService(DeliverInfo)  
        address_service = UserDeliverAddressService(UserDeliverAddress)
        li, num = service.get_by_date(goods_id, startdate, enddate, p, constants.NUM_PER_PAGE)
        nl = []
        for item in li:
            d = {}
            d['order_id'] = item.id
            d['user_id'] = item.user_id
            d['goods_id'] = item.goods_id            
            d['goods_name'] = item.goods_name
            d['number'] = item.number
            d['deliver_date'] = item.create_date
            d['express_status'] ={0:u'发货中',1:u'已完成'}.get(item.status)
            d['express_name'] = item.express_name
            d['express_no'] = item.express_no
            
            address = (address_service.get(id=item.deliver_address_id, status=1) 
                       or address_service.get(id=item.deliver_address_id, status=0))
            d['name'] = address.name
            d['phone'] = address.phone
            d['address'] =  u'{0}{1}'.format(address.region_name, address.address)
            nl.append(Odict(d))

        tp = int(math.ceil(num*1.0/constants.NUM_PER_PAGE))
        return self.render_html('admin/delivered_list.html', li=nl, enddate=enddate, startdate=startdate,
                                goods_id=goods_id,cp=p, pages=range(1,tp+1) if tp>0 else [1]) 
