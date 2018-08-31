# -*- coding: utf-8 -*-

'''
Created on 2018年8月17日

@author: shuai.chen
'''
import json
from towgo.cache.db_cache import RedisCache

REDIS = {
    "default":{
        "host":"192.168.1.165",
        "port":6381,
        "db":0,
        "password":"",
        "max_connections":100   
    }   
}

for rcn,rconfigs in REDIS.iteritems():
    RedisCache.connect(rcn,**rconfigs)  
    
redis = RedisCache()
redis.hset('a','1',json.dumps({'x':1,'y':2}))
v = redis.hget('a','1')
print type(json.loads(v))

redis.delete('a')

print redis.keys()
# redis.delete(*['order_4', 'order_list_1', 'order_2'])

# print redis.hgetall('discount_2')
# print redis.hgetall('discount_1')

    