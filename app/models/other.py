# -*- coding: utf-8 -*-

'''
Created on 2018年7月25日

@author: shuai.chen
'''


import datetime

from sqlalchemy import *
from base.sql import SqlModel

    
class AvatarInfo(SqlModel):
    """
    avatar信息
    """
    __tablename__ = "avatar_info" 
    __connection_name__ = "default"

    id = Column('id',BigInteger,primary_key=True,nullable=False)
    filename = Column('filename',String(32),nullable=False)
    type = Column('type',SmallInteger,nullable=False, default=0)
    path = Column('path',String(128),nullable=False, default='')
    create_date = Column('create_date',DateTime,nullable=False,default=datetime.datetime.now,server_default=text('CURRENT_TIMESTAMP'))
    update_time = Column('update_time',DateTime,nullable=False,default=datetime.datetime.now,server_default=text('CURRENT_TIMESTAMP'))

class Region(SqlModel):
    """
    region
    """
    __tablename__ = "region" 
    __connection_name__ = "default"

    id = Column('id',Integer,primary_key=True,nullable=False)
    region_code = Column('region_code',String(8),nullable=False)
    region_name = Column('region_name',String(32),nullable=False,default='')
    region_level = Column('region_level',SmallInteger,nullable=False,default=0)
    city_code = Column('city_code',String(6),nullable=False,default='')
    center = Column('center',String(32),nullable=False,default='')
    parent_id = Column('parent_id',Integer,nullable=False,default=1,index=True)
            