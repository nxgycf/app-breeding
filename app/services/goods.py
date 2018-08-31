# -*- coding: utf-8 -*-

'''
Created on 2018年5月18日

@author: shuai.chen
'''

from __future__ import absolute_import

from base.service import Service, operate

from base.cache import do_cache, rm_cache, up_cache
from common import keys


class GoodsService(Service):
    
    @do_cache(keys.GOODS_LIST, timeout=0)
    def cgets(self, **condition):
        return self.gets(**condition)

    @do_cache(keys.GOODS, timeout=0)
    def get(self, **condition):
        return super(GoodsService, self).get(**condition)

    def insert(self, obj):
        self.cache.delete(keys.GOODS_LIST % {'status':0})
        
        return super(GoodsService, self).insert(obj)
        
    @rm_cache(keys.GOODS, keys.GOODS_LIST % {'status':0})
    def update(self, attrs, **condition):
        return super(GoodsService, self).update(attrs, **condition)
    
    def delete(self, obj):
        kl = [keys.GOODS % {'id':obj.id}, keys.GOODS_LIST % {'status':0}]
        self.cache.delete(*kl)
        
        return super(GoodsService, self).delete(obj)
    
    @up_cache(keys.GOODS, timeout=0)
    @operate
    def buy(self, user_goods, attrs, **condition):
        '''
        buy goods
        '''
        self.session.add(user_goods)
        self.session.query(self.model).filter_by(**condition).update(attrs)
        self.session.commit()

class GoodsPictureService(Service):

    @do_cache(keys.GOODS_PICTURES, timeout=0)
    def gets(self, **condition):
        return super(GoodsPictureService, self).gets(**condition)
    
    def insert(self, obj):
        self.cache.delete(keys.GOODS_PICTURES % {'goods_id':obj.goods_id})
        
        return super(GoodsPictureService, self).insert(obj)    

    def delete(self, obj):
        self.cache.delete(keys.GOODS_PICTURES % {'goods_id':obj.goods_id})
        
        return super(GoodsPictureService, self).delete(obj)
    