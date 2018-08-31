# -*- coding: utf-8 -*-

'''
Created on 2018年5月18日

@author: shuai.chen
'''

import json
import os
import time

import requests
from towgo.handler import TornadoHttpHandler
from towgo.msetting import settings
from towgo.utils import http_util
import xmltodict

from app.common import alert, constant
from app.common.result import returns, Result    
from app.models.goods import GoodsInfo, GoodsPicture
from app.models.other import AvatarInfo
from app.models.user import UserGoods, UserDeliverAddress, UserPay
from app.services.goods import GoodsService, GoodsPictureService
from app.services.other import AvatarService
from app.services.user import UserDeliverAddressService, UserGoodsService
from base.cache import Cache    
from common import keys
from utils import check, time_util


class Test(TornadoHttpHandler):
    @returns()
    def _get(self):
        return self.render_html('app/slide.html')
    
class Index(TornadoHttpHandler):
    
    @returns()
    def _get(self):
        index = int(self.get_argument('index', 0))
        index = index if index in [0,1,2] else 0
        
        auth = ''
        user = getattr(self, 'user', None)
        if user is None and index != 0:
            auth = constant.WECHAT_AUTH
            
        return self.render_html('app/index.html', index=index, auth='')
    
class Protocol(TornadoHttpHandler):
    
    @returns()
    def _get(self):
        return self.render_html('app/protocol.html')
    
class About(TornadoHttpHandler):
    
    @returns()
    def _get(self):
        return self.render_html('app/about.html')      

class SendCode(TornadoHttpHandler):   
           
    def __init__(self, *args, **kwargs):
        super(SendCode, self).__init__(*args, **kwargs)  
        self.cache = Cache()    
              
    @returns(rjson=True)
    def _post(self):
        phone = self.get_argument('account')
        if not check.check_account(phone):
            return Result(alert.INVALID_PHONE)()
        
        tkey = keys.VERIFY_CODE_TIME.format(phone)
        op = self.cache.get(tkey)
        if op:
            return Result(alert.VERIFY_CODE_OP)()
        
        code = check.gen_verify_code()
        params = {
            'apikey':constant.YUNPIAN_APIKEY, 
             'mobile':phone, 
             'text':constant.VERIFY_CODE_TEXT.format(code)
        }
        headers = {
            "Accept":"application/json;charset=utf-8;",
            "Content-Type":"application/x-www-form-urlencoded;charset=utf-8;"
        }
        rt = http_util.urllib_request(constant.YUNPIAN_SHORTMSG, "POST", params, headers)
        result = json.loads(rt)
        if result['code'] != 0:
            return Result(alert.VERIFY_CODE_FAIL)()
        
        # save code
        key = keys.VERIFY_CODE.format(phone)
        self.cache.set(key, code, keys.VERIFY_CODE_EXPIRE)
        self.cache.set(tkey, int(time.time()), keys.VERIFY_CODE_TIME_EXPIRE)

        return Result(alert.SUCCESS)()
        
class GoodsList(TornadoHttpHandler):     
    """
    GOODS LIST
    """
    
    def __init__(self, *args, **kwargs):
        super(GoodsList, self).__init__(*args, **kwargs)  
        self.cache = Cache()      

        self.d1 = self.cache.hgetall(keys.DISCOUNT.format(1))
        self.d2 = self.cache.hgetall(keys.DISCOUNT.format(2))   

    @returns()
    def _get(self):
        ''' 
            % for ele in goods_list:
                <div class="goods-list">
                    <a href="/goods/detail?goods_id=${ele['id']}">
                        <div class="goods-item">                
                            <li>
                                <img class="tp" src="${ele['avatar']}" alt="商品图片" >
                                <div class="ti">
                                    <p class="name">${ele['name']}</p><br/>
                                    <p class="brief">${ele['brief']}</p><br/>
                                    
                                    <!--
                                    % if ele['type'] == 1:
                                       <p class="brief">喂养周期 : ${ele['feed_day']} 天</p><br/>
                                    % else:
                                       % if ele['feed_day'] == 0:
                                           <p class="brief">现货</p><br/>
                                       % else:
                                           <p class="brief">种植周期 : ${ele['feed_day']} 天</p><br/>
                                       % endif 
                                    %endif
                                    -->

                                    <p class="discount">${ele['dis_desc']}</p><br/>
                                    % if ele['last_price'] < ele['price']:
                                        <p class="price">￥${ele['last_price']}  <span class="nprice">￥${ele['price']}</span></p>
                                    % else:
                                        <p class="price">￥${ele['price']} </p>
                                    % endif
                                </div>
                            </li>
                        </div>    
                    </a>    
                </div>                
            % endfor
        '''
        ad_pics = self.get_ad_pics() 
        return self.render_html('app/goods_list.html', pics=ad_pics)
#         return self.render_html('app/goods_list.html',goods_list=goods_list, pics=ad_pics)  
                
    @returns(rjson=True)
    def _post(self):
        gtype = int(self.get_argument('gtype', 0))
        gtype_list = [gtype] if gtype != 0 else [1, 2, 3]        
        
        service = GoodsService(GoodsInfo)
        all_goods = service.cgets(status=0) 
        
        goods_list = []
        for goods in all_goods:
            if goods.number <= 0:
                continue
            if goods.type not in gtype_list:
                continue
            
            d = {}
            d['id'] = goods.id
            d['name'] = goods.name
            d['price'] = goods.price
            d['feed_day'] = goods.feed_day
            d['number'] = goods.number
            d['status'] = goods.status
            d['brief'] = goods.brief
            d['detail'] = goods.detail  
            d['type'] = goods.type 
            
            if goods.avatar_id:
                avatar_service = AvatarService(AvatarInfo)
                avatar = avatar_service.get(id=goods.avatar_id)   
                d['avatar'] = os.path.join(settings.AVATAR_URL, avatar.filename) if avatar else ''
            
            dis = self.get_discount(goods.id)
            d['last_price'] = goods.price * dis['discount'] if 'discount' in dis else goods.price
            d['dis_desc'] = dis['desc'] if 'desc' in dis else ''
            
            d['price_string'] = str(d['price'])
            d['last_price_string'] = str(d['last_price'])
                
            goods_list.append(d)  
        
        return Result(alert.SUCCESS, data=goods_list)()        

    def get_ad_pics(self):
        '''
        获取广告图片
        '''
        ad_dir = os.path.join(settings.STATIC_PATH, 'image/ads/')
        pics = []
        for f in os.listdir(ad_dir):
            fp = f.split('.')
            if fp[-1] in ['png', 'jpg', 'jpeg']:
                path = '../../static/image/ads/{0}'.format(f)
                goods_id = fp[0].split("_")[1]
                pics.append((path, int(goods_id)))
        return pics   
    
    def get_discount(self, goods_id, with_desc=True):
        '''
        获取活动信息
        '''
        gid = str(goods_id)
        now = int(time.time())
        
        info = {}
        if gid in self.d1:
            d = json.loads(self.d1[gid])
            start = time_util.to_ts("{0} 00:00:00".format(d['start']))
            end = time_util.to_ts("{0} 23:59:59".format(d['end']))
            if now>= start and now <= end:
                info['discount'] = float(d['discount'])
                if with_desc:
                    info['desc'] = u"{0}至{1}期间{2}优惠 ".format(d['start'], d['end'], d['desc'])
                
        if gid in self.d2:        
            d = json.loads(self.d2[gid])
            start = time_util.to_ts("{0} 00:00:00".format(d['start']))
            end = time_util.to_ts("{0} 23:59:59".format(d['end']))
            if now>= start and now <= end:
                info['num'] = int(d['num'])
                info['amount'] = float(d['amount'])
                if with_desc:
                    desc = info.get('desc', u'{0}至{1}期间'.format(d['start'], d['end']))
                    info['desc'] = u"{0}每满{1}件立减{2}元".format(desc, info['num'],info['amount'])
            
        return info       
    
class GoodsDetail(GoodsList):     
    """
    GOODS detail
    """  
            
    @returns()
    def _get(self):        
        goods_id = int(self.get_argument('goods_id', 0))
        if not goods_id:
            return self.render_html('app/alert.html', msg=u"请选择商品!") 
        
        service = GoodsService(GoodsInfo)
        goods = service.get(id=goods_id)
        if not goods:
            return self.render_html('app/alert.html', msg=u"该商品不存在!") 
        
        d = {}
        d['id'] = goods.id
        d['name'] = goods.name
        d['price'] = goods.price
        d['feed_day'] = goods.feed_day
        d['number'] = goods.number
        d['status'] = goods.status
        d['brief'] = goods.brief
        d['detail'] = goods.detail   
        d['type'] = goods.type
        
        d['deliver_date'] = time_util.delta_str(delta=goods.feed_day + 1)
        
        d['avatar'] = ''
        if goods.avatar_id:
            avatar_service = AvatarService(AvatarInfo)
            avatar = avatar_service.get(id=goods.avatar_id)   
            d['avatar'] = os.path.join(settings.AVATAR_URL, avatar.filename) if avatar else ''

        detail_pic = ''
        pics = []
        pictures = GoodsPictureService(GoodsPicture).gets(goods_id=goods.id)
        for pic in pictures:
            url = os.path.join(settings.GOODS_PICTURE_URL, pic.filename)
            if pic.type == 1:
                detail_pic = url
            else:    
                pics.append( url)        
        
        d['detail_pic'] = detail_pic   
        d['pics'] = pics   
        
        dis = self.get_discount(goods.id)
        d['last_price'] = goods.price * dis['discount'] if 'discount' in dis else goods.price
        d['dis_desc'] = dis['desc'] if 'desc' in dis else ''
            
        return self.render_html('app/goods_detail.html',**d)  
    
class BuyGoods(GoodsList):
    """
    BUY
    """
    @returns(need_login=True)
    def _get(self):
        goods_id = int(self.get_argument('goods_id', 0))
        if not goods_id:
            return self.render_html('app/alert.html', msg=u"请选择商品!")     
        
        service = GoodsService(GoodsInfo)
        goods = service.get(id=goods_id)
        if not goods:
            return self.render_html('app/alert.html', msg=u"该商品不存在!") 

        alert = None  
        num = int(self.get_argument('num', 1))
        if goods.number < num:
            alert = u"!库存不足!"
        
        address_id = int(self.get_argument('address_id', self.user.deliver_address_id))
        if not address_id:
            alert = u"!请先添加您的收货地址!"
        
        address = None
        address_service = UserDeliverAddressService(UserDeliverAddress)  
        ua = address_service.get(id = address_id, status=1)
        if ua:
            address = {'name':ua.name,'phone':ua.phone,'address':u'{0}{1}'.format(ua.region_name, ua.address)}
            if not self.check_region(goods_id, ua.region_id):
                alert = u"!该地区暂不支持购买!"
        else:
            alert = u"!请先添加您的收货地址!"       
                                  
        d = {}
        d['id'] = goods.id
        d['name'] = goods.name
        d['price'] = goods.price
        d['feed_day'] = goods.feed_day
        d['number'] = goods.number
        d['status'] = goods.status
        d['brief'] = goods.brief
        d['detail'] = goods.detail   
        d['type'] = goods.type
        
        d['avatar'] = ''
        if goods.avatar_id:
            avatar_service = AvatarService(AvatarInfo)
            avatar = avatar_service.get(id=goods.avatar_id)   
            d['avatar'] = os.path.join(settings.AVATAR_URL, avatar.filename) if avatar else ''
   
        d['address'] = address   
        d['alert'] = alert 
        d['attach'] = {'num':num, 'address_id':address_id}
        
        dis = self.get_discount(goods.id)
        d['last_price'] = goods.price * dis['discount'] if 'discount' in dis else goods.price
        d['dis_num'] = dis['num'] if 'num' in dis else 1
        d['dis_amount'] = dis['amount'] if 'amount' in dis else 0
        d['dis_desc'] = dis['desc'] if 'desc' in dis else ''
        
        d['amount'] = d['last_price'] * num - int(num/d['dis_num'])*d['dis_amount']
        d['discount'] = goods.price * num  - d['amount']
                    
        return self.render_html('app/buy_goods.html',**d)  
                        
    @returns(need_login=True, rjson=True)
    def _post(self):
        goods_id = int(self.get_argument('goods_id', 0))
        num = int(self.get_argument('num', 1))
        if not goods_id or num == 0:
            return self.render_html('app/alert.html', msg=u"请选择商品!") 
        
        goods_service = GoodsService(GoodsInfo)
        goods = goods_service.get(id=goods_id)
        if not goods:
            return self.render_html('app/alert.html', msg=u"该商品不存在!") 

        if goods.number < num:
            return self.render_html('app/alert.html', msg=u"该商品库存不足!") 
        
        feed_day = int(self.get_argument('feed_day', goods.feed_day))
        address_id = int(self.get_argument('address_id', self.user.deliver_address_id))
        
        ua = UserDeliverAddressService(UserDeliverAddress) .get(id=address_id, status=1)
        if not ua:
            return self.render_html('app/alert.html', msg=u"该地址不存在!") 

        #判断开通地区
        if not self.check_region(goods_id, ua.region_id):
            return self.render_html('app/alert.html', msg=u"该地区暂不支持购买!") 
        
        dis = self.get_discount(goods.id, False)
        last_price = goods.price * dis['discount'] if 'discount' in dis else goods.price
        dis_num, dis_amount = dis['num'] if 'num' in dis else 1, dis['amount'] if 'amount' in dis else 0 
        amount = last_price * num - int(num/dis_num)*dis_amount
        
        # 创建订单   
        order_code = check.get_order_code() 
        data = self.request_unifiedorder(order_code, amount)

        if data.code == alert.SUCCESS:
            user_goods = UserGoods()
            user_goods.user_id = self.user.id
            user_goods.code = order_code
            user_goods.goods_id = goods.id
            user_goods.goods_name = goods.name
            user_goods.goods_price = goods.price
            user_goods.number = num
            user_goods.amount = amount
            user_goods.feed_day = feed_day
            user_goods.deliver_date = time_util.delta_dt(delta=feed_day + 1)
            user_goods.deliver_address_id = address_id 
            user_goods.status = 0
            
            goods_service.buy(user_goods, {'number':goods.number-num}, id=goods_id)
            
        return data()   
          
        '''    
        user_goods = UserGoods()
        user_goods.user_id = self.user.id
        user_goods.code = order_code
        user_goods.goods_id = goods.id
        user_goods.goods_name = goods.name
        user_goods.goods_price = goods.price
        user_goods.number = num
        user_goods.feed_day = feed_day
        user_goods.deliver_date = time_util.delta_dt(delta=feed_day + 1)
        user_goods.deliver_address_id = address_id 
         
        # 创建支付信息
        user_pay = UserPay()
        user_pay.user_id = self.user.id
        user_pay.goods_id = goods.id
        user_pay.amount = amount
        user_pay.status = 1
         
        #更新物品数量
        goods_service.buy(user_goods, user_pay, {'number':goods.number-num}, id=goods_id)

        self.redirect('/app?index=1')   
        '''
        
    def check_region(self, goods_id, region_id):
        '''
        check open region
        '''
        open_regions = self.cache.hget(keys.OPEN_REGION, str(goods_id))
        
        if open_regions:
            if str(region_id) not in open_regions:  
                return False
        return True


    def get_sign(self, kwargs):
        # 计算签名
        keys = sorted(kwargs)
        string = '&'.join([u'{0}={1}'.format(k, kwargs[k]) for k in keys if k != 'appkey'])    
        string = u"{0}&key={1}".format(string, constant.WBC['KEY'])
        return check.MD5(string).upper()
    
    def get_xml(self, kwargs):
        # 创建XML
        kwargs['sign'] = self.get_sign(kwargs)
        xmls = [u'<{0}>{1}</{0}>'.format(k, v) for k, v in kwargs.iteritems()]
        return u'<xml>{0}</xml>'.format(''.join(xmls))
    
    def request_unifiedorder(self, order_code, amount):
        '''
        微信统一订单请求
        '''
        unifiedorder_request = {
            'appid': constant.WBC['APPID'], # 公众账号ID
            'body': u'公司名称-商品',  # 商品描述
            'mch_id': '1397xxxxxx8',  # 商户号:深圳市泽慧文化传播有限公司
            'nonce_str': '',  # 随机字符串
            'notify_url': settings.PAY_NOTICE_URL,  # 微信支付结果异步通知地址
            'openid': self.user.id,  # openid
            'out_trade_no': '',  # 商户订单号
            'spbill_create_ip': self.request.remote_ip ,  # 终端IP
            'total_fee': '',  # 标价金额
            'trade_type': 'JSAPI',  # 交易类型
        }
        unifiedorder_request['nonce_str'] = check.get_nonce_str()
        unifiedorder_request['out_trade_no'] = order_code  # 内部订单号码
        unifiedorder_request['total_fee'] = int(amount * 100)  #单位 分
        
        # 签名并生成xml
        xml = self.get_xml(unifiedorder_request)
        resp = requests.post(constant.WECHAT_UNIFIED_ORDER, data=xml, 
                             headers={'Content-Type': 'text/xml'})
        msg = resp.text.encode('ISO-8859-1').decode('utf-8')
        xml_resp = xmltodict.parse(msg)
        xml_resp = xml_resp['xml']
        
        if xml_resp['return_code'] == 'SUCCESS':
            if xml_resp['result_code'] == 'SUCCESS':
                prepay_id = xml_resp['prepay_id']
                timestamp = str(int(time.time()))
                data = {
                    "app_id": xml_resp['appid'],
                    "nonce_str": check.get_nonce_str(),
                    "package": "prepay_id={0}".format(prepay_id),
                    "sign_type": "MD5",
                    "timestamp": timestamp
                }
                data['pay_sign'] = self.get_sign(data)
                data['order_code'] = order_code  # 付款后操作的订单
                # 签名后返回给前端做支付参数
                return Result(alert.SUCCESS, data=data)
            else:
                msg = xml_resp['err_code_des']
                return Result(alert.FAIL, message=msg)
        else:
            msg = xml_resp['return_msg']
            return Result(alert.FAIL, message=msg)

class PayResult(TornadoHttpHandler):
    '''
    支付结果处理
    '''    
    
    def __init__(self, *args, **kwargs):
        super(GoodsList, self).__init__(*args, **kwargs)  
        self.order_service = UserGoodsService(UserGoods)
    
    @returns(need_login=True, rjson=True)
    def _get(self):
        order_code = self.get_argument("order_code", '')
        if order_code:
            order = self.order_service.get_by_code(code=order_code)
            if order:
                return self.look_unifiedorder(order)()
        return Result(alert.FAIL, message=u"订单不存在!")()
         
    def look_unifiedorder(self, order):
        '''
        微信统一订单查询
        '''
        orderquery = {
            'appid': constant.WBC['APPID'],
            'mch_id': constant.WBC['MCHID'],
            'nonce_str': check.get_nonce_str(),
            'out_trade_no': order.code
        }
        xml = self.get_xml(orderquery)

        resp = requests.post(constant.WECHAT_QUERY_ORDER, data=xml.encode('utf-8'), 
                             headers={'Content-Type': 'text/xml'})
        msg = resp.text.encode('ISO-8859-1').decode('utf-8')
        xmlresp = xmltodict.parse(msg)
        xmlresp = xmlresp['xml']

        if xmlresp['return_code'] == 'SUCCESS':
            if xmlresp['result_code'] == 'SUCCESS':
                if xmlresp['trade_state'] == 'SUCCESS':
                    transaction_id = xmlresp['transaction_id']
                    cash_fee = xmlresp['cash_fee']

                    user_pay = UserPay()
                    user_pay.user_goods_id = order.id
                    user_pay.transaction_id = transaction_id
                    user_pay.user_id = self.user.id
                    user_pay.goods_id = order.goods_id
                    user_pay.amount = cash_fee
                    user_pay.status = 1
                    
                    self.order_service.pay(user_pay, {'status':1, 'transaction_id':transaction_id}, id=order.id)
                    return Result(alert.SUCCESS)
                else:
                    msg = xmlresp['trade_state_desc']
                    return Result(alert.FAIL, message=msg)
            else:
                msg = xmlresp['err_code_des']
                return Result(alert.FAIL, message=msg)
        else:
            msg = xmlresp['return_msg']
            return Result(alert.FAIL, message=msg)
               
class PayNotice(TornadoHttpHandler):
    '''
    支付通知
    '''
    
    def _get(self):
        self.finish(
            """
                <xml>
                  <return_code><![CDATA[SUCCESS]]></return_code>
                  <return_msg><![CDATA[OK]]></return_msg>
                </xml>
            """
        )
    
            
class SelectAddress(TornadoHttpHandler):    
    
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
        
        goods_id = self.get_argument('goods_id')
        num = int(self.get_argument('num', 1))
                
        return self.render_html('app/address_select.html',li=alist, default=default, goods_id=goods_id, num=num)     
