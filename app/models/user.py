# -*- coding: utf-8 -*-

'''
Created on 2018年5月18日

@author: shuai.chen
'''

import datetime

from sqlalchemy import *
from base.sql import SqlModel


class UserInfo(SqlModel):
    """
    用户信息
    """
    __tablename__ = "user_info" 
    __connection_name__ = "default"
    
    id = Column('id',BigInteger,primary_key=True,autoincrement=True,nullable=False)
    account = Column('account',String(32),nullable=False,index=True,unique=True,)
    phone = Column('phone',String(16),nullable=False,default='',index=True)    
    nickname = Column('nickname',String(16),nullable=False,default='')    
    password = Column('password',String(32),nullable=False)
    avatar_id = Column('avatar_id',BigInteger,nullable=False,default=0)
    deliver_address_id = Column('deliver_address_id',BigInteger,nullable=False,default=0)    
    create_date = Column('create_date',DateTime,nullable=False,default=datetime.datetime.now,server_default=text('CURRENT_TIMESTAMP'))
    update_time = Column('update_time',DateTime,nullable=False,default=datetime.datetime.now,server_default=text('CURRENT_TIMESTAMP'))

class WechatUser(SqlModel):
    '''
    微信用户
    '''
    __tablename__ = "wechat_user" 
    __connection_name__ = "default"
    
    id = Column('id',BigInteger,primary_key=True,autoincrement=True,nullable=False)
    openid = Column('openid',String(32),nullable=False, index=True)
    nickname = Column('nickname',String(32),nullable=False,default='')
    sex = Column('sex',SmallInteger,nullable=False,default=0)
    province = Column('province',String(32),nullable=False,default='')
    city = Column('city',String(32),nullable=False,default='')
    country = Column('country',String(16),nullable=False,default='')
    headimgurl = Column('headimgurl',String(128),nullable=False,default='')
    deliver_address_id = Column('deliver_address_id',BigInteger,nullable=False,default=0)
    create_date = Column('create_date',DateTime,nullable=False,default=datetime.datetime.now,server_default=text('CURRENT_TIMESTAMP'))
    update_time = Column('update_time',DateTime,nullable=False,default=datetime.datetime.now,server_default=text('CURRENT_TIMESTAMP'))
            
class UserGoods(SqlModel):
    """
    用户商品(订单)
    """
    __tablename__ = "user_goods" 
    __connection_name__ = "default"  
        
    id = Column('id',BigInteger,primary_key=True,autoincrement=True,nullable=False)
    code = Column('code',String(18),nullable=False,unique=True,index=True) 
    transaction_id = Column('transaction_id',String(32),nullable=False,default='',index=True)
    user_id = Column('user_id',BigInteger,nullable=False,index=True)
    goods_id = Column('goods_id',Integer,nullable=False,index=True)
    goods_name = Column('goods_name',String(16),nullable=False)    
    goods_price = Column('goods_price',Float,nullable=False)
    number = Column('number',Integer,nullable=False,default=1)
    amount = Column('amount',Float,nullable=False)
    feed_day= Column('feed_day',Integer,nullable=False,default=0)
    deliver_date = Column('deliver_date',DateTime,nullable=False,index=True)
    status = Column('status',SmallInteger,nullable=False,default=0)   
    deliver_address_id = Column('deliver_address_id',BigInteger,nullable=False,default=0)
    create_date = Column('create_date',DateTime,nullable=False,default=datetime.datetime.now,server_default=text('CURRENT_TIMESTAMP'))
    update_time = Column('update_time',DateTime,nullable=False,default=datetime.datetime.now,server_default=text('CURRENT_TIMESTAMP'))

class UserDeliverAddress(SqlModel):
    """
    用户邮寄地址
    """
    __tablename__ = "user_deliver_address" 
    __connection_name__ = "default"

    id = Column('id',BigInteger,primary_key=True,autoincrement=True,nullable=False)
    user_id = Column('user_id',BigInteger,nullable=False,index=True)
    name = Column('name',String(16),nullable=False,default='')
    phone = Column('phone',String(16),nullable=False,default='')
    address = Column('address',String(256),nullable=False,default='')
    zip_code = Column('zip_code',Integer,nullable=False,default=0)
    region_id = Column('region_id',Integer,nullable=False,default=0)
    region_name = Column('region_name',String(128),nullable=False,default='')
    status = Column('status',SmallInteger,nullable=False,default=1,index=True)
    create_date = Column('create_date',DateTime,nullable=False,default=datetime.datetime.now,server_default=text('CURRENT_TIMESTAMP'))
    update_time = Column('update_time',DateTime,nullable=False,default=datetime.datetime.now,server_default=text('CURRENT_TIMESTAMP'))
    
class UserPay(SqlModel):
    """
    用户支付信息
    """
    __tablename__ = "user_pay" 
    __connection_name__ = "default"
    
    id = Column('id',Integer,primary_key=True,autoincrement=True,nullable=False)
    user_goods_id = Column('user_goods_id',BigInteger,unique=True,nullable=False,index=True)    
    transaction_id = Column('transaction_id',String(32),nullable=False,default='',index=True)
    user_id = Column('user_id',BigInteger,nullable=False,index=True)
    goods_id = Column('goods_id',Integer,nullable=False,index=True)
    pay_type = Column('pay_type',SmallInteger,nullable=False, default=1)
    amount = Column('amount',Float,nullable=False)
    status = Column('status',SmallInteger,nullable=False)
    create_date = Column('create_date',DateTime,nullable=False,default=datetime.datetime.now,server_default=text('CURRENT_TIMESTAMP'))
    update_time = Column('update_time',DateTime,nullable=False,default=datetime.datetime.now,server_default=text('CURRENT_TIMESTAMP'))

class DeliverInfo(SqlModel):
    """
    用户邮寄信息
    """
    __tablename__ = "deliver_info" 
    __connection_name__ = "default"

    id = Column('id',Integer,primary_key=True,autoincrement=True,nullable=False)
    user_goods_id = Column('user_goods_id',BigInteger,unique=True,nullable=False,index=True)
    user_id = Column('user_id',BigInteger,nullable=False)
    goods_id = Column('goods_id',Integer,nullable=False)
    goods_name = Column('goods_name',String(16),nullable=False)
    number = Column('number',Integer,nullable=False,default=1)    
    express_name = Column('express_name',String(16),nullable=False)
    express_no = Column('express_no',String(32),nullable=False)
    status = Column('status',SmallInteger,nullable=False)
    deliver_address_id = Column('deliver_address_id',BigInteger,nullable=False,default=0)
    create_date = Column('create_date',DateTime,nullable=False,default=datetime.datetime.now,server_default=text('CURRENT_TIMESTAMP'))
    update_time = Column('update_time',DateTime,nullable=False,default=datetime.datetime.now,server_default=text('CURRENT_TIMESTAMP'))

class UserNews(SqlModel):
    """
    用户消息
    """
    __tablename__ = "user_news" 
    __connection_name__ = "default"    

    id = Column('id',BigInteger,primary_key=True,autoincrement=True,nullable=False)
    user_id = Column('user_id',BigInteger,nullable=False,index=True)
    content = Column('content',String(128),nullable=False,default='')
    status = Column('status',SmallInteger,nullable=False,default=0)
    create_date = Column('create_date',DateTime,nullable=False,default=datetime.datetime.now,server_default=text('CURRENT_TIMESTAMP'))    
    update_time = Column('update_time',DateTime,nullable=False,default=datetime.datetime.now,server_default=text('CURRENT_TIMESTAMP'))

                                    