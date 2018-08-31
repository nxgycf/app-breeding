# -*- coding: utf-8 -*-

'''
Created on 2018年5月18日

@author: shuai.chen
'''

from __future__ import absolute_import

from base.service import Service, operate
from base.cache import do_cache, rm_cache
from common import keys


class UserInfoService(Service):
    pass

class WechatUserService(Service):
    pass

class UserDeliverAddressService(Service):

    @do_cache(keys.USER_ADDRESS_LIST)
    def gets(self, **condition):
        return super(UserDeliverAddressService, self).gets(**condition)

    @do_cache(keys.USER_ADDRESS)
    def get(self, **condition):
        return super(UserDeliverAddressService, self).get(**condition)
        
    def insert(self, obj):
        self.cache.delete(keys.USER_ADDRESS_LIST % {'user_id':obj.user_id, "status":1})
        
        return super(UserDeliverAddressService, self).insert(obj)    
    
    @rm_cache(keys.USER_ADDRESS, keys.USER_ADDRESS_LIST)
    def update(self, attrs, **condition):
        return super(UserDeliverAddressService, self).update(attrs, **condition)

class UserGoodsService(Service):

    @do_cache(keys.ORDER_LIST)
    def gets(self, **condition):
        return super(UserGoodsService, self).gets(**condition)

    @do_cache(keys.ORDER)
    def get(self, **condition):
        return super(UserGoodsService, self).get(**condition)

    def get_by_code(self, **condition):
        return super(UserGoodsService, self).get(**condition)
    
    @operate
    def pay(self, user_pay, attrs, **condition):
        '''
        pay order
        '''
        # delete cache
        kl = [keys.ORDER % condition, keys.ORDER_LIST % {'user_id':user_pay.user_id}]
        self.cache.delete(*kl)
        
        self.session.add(user_pay)
        self.session.query(self.model).filter_by(**condition).update(attrs)
        self.session.commit()
        
    @operate
    def deliver(self, deliver_info, attrs, **condition):
        '''
        发货
        '''
        # delete cache
        kl = [keys.ORDER % condition, keys.ORDER_LIST % {'user_id':deliver_info.user_id}]
        self.cache.delete(*kl)
        
        self.session.add(deliver_info)
        self.session.query(self.model).filter_by(**condition).update(attrs)
        self.session.commit()
            
    def get_by_date(self, goods_id, date_field, status, startdate, enddate, page, num):
        '''
        @param goods_id: 商品ID
        @param date_field: 查询字段
        @param status: 查询状态
        @param startdate: 起始日期
        @param enddate: 截止日期
        @param page: 第几页
        @param num: 每页显示条数
        '''
        sql = str.format("select * from {0} where date({1}) between '{2}' and '{3}'", 
                          self.model.__tablename__, date_field, startdate, enddate)
        csql = str.format("select count(*) as num from {0} where date({1}) between '{2}' and '{3}'", 
                  self.model.__tablename__, date_field, startdate, enddate)
        if status == 1:
            sql = "{0} and status=1".format(sql)
            csql = "{0} and status=1".format(csql)
        if goods_id:
            sql = str.format("{0} and goods_id={1}", sql, goods_id) 
            csql = str.format("{0} and goods_id={1}", csql, goods_id) 
        sql = str.format("{0} order by {1} limit {2},{3}", sql, date_field, (page-1)*num, page*num)  
        
        li, num = self.get_by_sql(sql), self.get_by_sql(csql, 'num')
        return li, num[0].num if num is not None else 0
    
    def get_count(self):
        sql1 = str.format("""select goods_id,goods_name,count(distinct user_id) as count,sum(number) as sum
                             from {0} where status=1 group by goods_id""", 
                          self.model.__tablename__)
        sql2 = str.format("""select goods_id,goods_name,count(distinct user_id) as count,sum(number) as sum
                             from {0} where status=2 group by goods_id""", 
                          self.model.__tablename__)
        
        fields = ['goods_id', 'goods_name', 'count', 'sum']
        q1, q2= self.get_by_sqls([(sql1,fields), (sql2,fields)])
        return q1, q2
    

class DeliverService(Service):
    
    @do_cache(keys.DELIVER)
    def get(self, **condition):
        return super(DeliverService, self).get(**condition)    

    def get_by_date(self, goods_id, startdate, enddate, page, num):
        '''
        @param goods_id: 商品ID
        @param startdate: 起始日期
        @param enddate: 截止日期
        @param page: 第几页
        @param num: 每页显示条数
        '''        
        sql = str.format("select * from {0} where date(create_date) between '{1}' and '{2}'", 
                          self.model.__tablename__, startdate, enddate)
        csql = str.format("select count(*) as num from {0} where date(create_date) between '{1}' and '{2}'", 
                          self.model.__tablename__, startdate, enddate)   
        if goods_id:
            sql = str.format("{0} and goods_id={1}", sql, goods_id)   
            csql = str.format("{0} and goods_id={1}", csql, goods_id)   
        sql = str.format("{0} limit {1},{2}", sql, (page-1)*num, page*num)    
          
        li, num = self.get_by_sql(sql), self.get_by_sql(csql, 'num')
        return li, num[0].num if num is not None else 0

class UserPayService(Service):

    @do_cache(keys.USER_PAY)
    def get(self, **condition):
        return super(UserPayService, self).get(**condition)    
    
