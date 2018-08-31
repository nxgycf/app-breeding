#coding:utf-8

'''
Created on 2017年2月13日
@author: shuai.chen
'''

from datetime import datetime

from sqlalchemy import *
from base.sql import SqlModel

class Admin(SqlModel):
    """
    insert into admin (account,password,name,level) values ('nxgych@163.com','ff8af7df974ab9e239803015757303f7','陈帅',3);
    """
    __tablename__ = "admin" 
    __connection_name__ = "default"
    
    id = Column('id',BigInteger,primary_key=True,autoincrement=True,nullable=False)
    account = Column('account',String(32), unique=True, nullable=False)
    password = Column('password',String(32),nullable=False)
    name = Column('name',String(32),default="",nullable=False)
    level = Column('level',Integer,default=1,nullable=False)
    create_date = Column('create_date',TIMESTAMP,default=datetime.now,server_default=text('CURRENT_TIMESTAMP'),nullable=False)
    update_time = Column('update_time',TIMESTAMP,default=datetime.now,server_default=text('CURRENT_TIMESTAMP'),nullable=False)
        