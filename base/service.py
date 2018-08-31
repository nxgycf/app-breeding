#coding:utf-8

'''
Created on 2017年2月14日
@author: shuai.chen
'''

from __future__ import absolute_import

import functools
from sqlalchemy import text

from .cache import Cache

def operate(func):
    '''
    数据库操作
    '''
    @functools.wraps(func)
    def _deco(self, *args, **kwargs):
        self.session = self.model.session()
        try:
            return func(self, *args, **kwargs)  
        except:
            if self.session:
                self.session.rollback()
            raise
        finally:
            if self.session:
                self.session.close()             
    return _deco

class Service(object):

    def __init__(self,model=None, cache=True):
        self.model = model
        if cache:
            self.cache = Cache()
    
    @operate        
    def get(self, **condition):
        """
        根据 条件 获取对象
        @param param:
            condition:dict 
        """
        return self.session.query(self.model).filter_by(**condition).first()
    
    @operate                    
    def insert(self, obj):
        """
        insert 
        @param param:
            attrs:dict         
        """
        obj = self.model(**obj) if isinstance(obj, dict) else obj
        self.session.add(obj)
        self.session.commit()
        return obj.id
    
    @operate          
    def update(self, attrs, **condition):
        """
        update 
        @param param:
            condition:dict   
            attrs:dict      
        """        
        self.session.query(self.model).filter_by(**condition).update(attrs)
        self.session.commit() 
    
    @operate
    def delete(self, obj):
        """
        delete object
        @param param:
            obj:object         
        """
        self.session.delete(obj)
        self.session.commit()    
    
    @operate                    
    def gets(self,**condition):
        """
        get list
        根据 条件 获取对象 list
        @param param:
            condition:dict          
        """
        if condition:
            return self.session.query(self.model).filter_by(**condition).all()
        else:
            return self.session.query(self.model).all()

    @operate
    def get_by_sql(self, sql, *fields):
        '''
        根据字段和SQL语句查询
        @param param: 
            SQL：查询语句
        @return: 
            result:返回查询列表    
        '''
        sql = text(sql)
        if fields:
            result = self.session.query(*fields).from_statement(sql).params().all() 
        else:
            result = self.session.query(self.model).from_statement(sql).params().all()     
        return result        

    @operate
    def get_by_sqls(self, sqls):
        '''
        根据字段和SQL语句查询
        @param param: 
            SQLs：多个查询语句 [(sql,[fields]),]
        @return: 
            result:返回查询列表    
        '''
        results = []
        for item in sqls:
            sql, fields = text(item[0]), item[1]
            if fields:
                result = self.session.query(*fields).from_statement(sql).params().all() 
            else:
                result = self.session.query(self.model).from_statement(sql).params().all()     
            results.append(result)    
        return results       
                            