#coding:utf-8

'''
Created on 2017年2月13日
@author: shuai.chen
'''

import json
from datetime import datetime,date
from sqlalchemy.orm import class_mapper

from towgo.dbs.alchemy import BaseModel

class SqlModel(BaseModel):
    
    __abstract__ = True
    
    def __getitem__(self, name):
        '''
        get ATTR value
        '''
        return self.__dict__[name]
    
    def __setitem__(self, name, value):
        '''
        set ATTR value
        '''
        self.__dict__[name] = value

    def as_json(self):
        '''
        to json
        '''
        data = {}
        for col in class_mapper(self.__class__).mapped_table.c:
            key = col.name
            value = getattr(self, col.name)
            if isinstance(value, datetime) or isinstance(value, date):
                value = value.strftime("%Y-%m-%d %H:%M:%S")
            data[key] =value    
        return json.dumps(data)
            