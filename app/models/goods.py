# -*- coding: utf-8 -*-

'''
Created on 2018年5月18日

@author: shuai.chen
'''

import datetime

from sqlalchemy import *
from base.sql import SqlModel

class GoodsInfo(SqlModel):
    """
    商品信息
    """
    __tablename__ = "goods_info" 
    __connection_name__ = "default"
    
    id = Column('id',Integer,primary_key=True,autoincrement=True,nullable=False)
    code = Column('code',Integer,nullable=False,unique=True,index=True)
    avatar_id = Column('avatar_id',BigInteger,nullable=False,default=0)
    name = Column('name',String(16),nullable=False)
    price = Column('price',Float,nullable=False)
    type = Column('type',Integer,nullable=False,default=1,index=True)
    feed_day = Column('feed_day',Integer,nullable=False,default=0)
    brief = Column('brief',String(128),nullable=False,default='')
    detail = Column('detail',String(512),nullable=False,default='')
    number = Column('number',Integer,nullable=False,default=1)
    status = Column('status',SmallInteger,nullable=False,default=0)
    create_date = Column('create_date',DateTime,nullable=False,default=datetime.datetime.now,server_default=text('CURRENT_TIMESTAMP'))
    update_time = Column('update_time',DateTime,nullable=False,default=datetime.datetime.now,server_default=text('CURRENT_TIMESTAMP'))

class GoodsPicture(SqlModel):
    """
    picture信息
    """
    __tablename__ = "goods_picture" 
    __connection_name__ = "default"

    id = Column('id',BigInteger,primary_key=True,nullable=False)
    goods_id = Column('goods_id',Integer,nullable=False,index=True)    
    filename = Column('filename',String(32),nullable=False)
    type = Column('type',SmallInteger,nullable=False, default=0)
    path = Column('path',String(128),nullable=False, default='')
    create_date = Column('create_date',DateTime,nullable=False,default=datetime.datetime.now,server_default=text('CURRENT_TIMESTAMP'))
    update_time = Column('update_time',DateTime,nullable=False,default=datetime.datetime.now,server_default=text('CURRENT_TIMESTAMP'))
