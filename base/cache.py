# -*- coding: utf-8 -*-

'''
Created on 2018年8月22日

@author: shuai.chen
'''

import functools
import cPickle as pickle

from towgo.cache.db_cache import RedisCache

from common import keys

def do_cache(prefix, timeout=keys.NORMAL_EXPIRE): 
    """
    缓存处理
    """
    def _deco(func):  
        @functools.wraps(func) 
        def __deco(self, *args, **kwargs):
            key = prefix % kwargs
                        
            obj = self.cache.get_obj(key)
            if obj:
                return obj
            
            obj = func(self, *args, **kwargs)
            if obj:
                self.cache.set_obj(key, obj, timeout)    
                        
            return obj
        return __deco   
    return _deco  

def up_cache(prefix, timeout=keys.NORMAL_EXPIRE): 
    """
    缓存更新
    """
    def _deco(func):  
        @functools.wraps(func) 
        def __deco(self, *args, **kwargs):
            key = prefix % kwargs
                        
            obj = self.cache.get_obj(key)
            if obj:
                for arg in args:
                    if isinstance(arg, dict):
                        for k,v in arg.iteritems():
                            obj[k] = v
                self.cache.set_obj(key, obj, timeout)  
            
            return func(self, *args, **kwargs)
        return __deco   
    return _deco 

def rm_cache(*prefixs):
    """
    缓存移除装饰器
    @param prefixs: 多个cache key
    """  
    def _deco(func):
        @functools.wraps(func) 
        def __deco(self, *args, **kwargs):    
            self.cache.delete(*[p % kwargs for p in prefixs])
            
            return func(self, *args, **kwargs)  
        return __deco
    return _deco


class Cache(RedisCache):   
    
    def set_list(self,key, data, expire=0):  
        '''
        存储 PYTHON list
        '''
        obj = {}
        for item in data:
            val = pickle.dumps(item, pickle.HIGHEST_PROTOCOL)
            obj[item.id] = val
        self.conn.hmset(key, obj)  
        if expire > 0: 
            self.conn.expire(key, expire) 

    def get_list(self, key):   
        '''
        获取 PYTHON list
        '''
        data = []
        val = self.conn.hgetall(key)
        for _, v in val.iteritems():
            data.append(pickle.loads(v))
        return data    
    
    def get_list_item(self, key, field):
        '''
        get list item
        '''
        val = self.conn.hget(key, field)
        if val:
            return pickle.loads(val)
        return None
    
    def set_list_item(self, key, item, expire=0):
        '''
        set list item
        '''
        val = pickle.dumps(item, pickle.HIGHEST_PROTOCOL)
        self.conn.hset(key, item.id, val)  
        if expire > 0: 
            self.conn.expire(key, expire) 
     
    def del_list_item(self, key, *field):  
        '''
        delete list item
        ''' 
        self.conn.hdel(key, *field) 
