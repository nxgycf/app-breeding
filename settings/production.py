#coding:utf-8

'''
Created on 2017年1月3日
@author: shuai.chen
'''

import os

PROJECT_PATH = os.path.dirname(os.path.dirname(__file__))

MULTI_PROCESS = False
THREAD_POOL_SIZE = 50

#static path
STATIC_PATH = os.path.join(PROJECT_PATH,'static')

#templates path
TEMPLATE_PATH = os.path.join(PROJECT_PATH,'templates')

#resource path
RESOURCE_PATH = os.path.join(PROJECT_PATH,'resources')

XSRF_COOKIES = True
COOKIE_SECRET = "BREEDING"

#session configuration
SESSION = {
    "open":True, #是否开启session           
    "storage":"towgo.cache.db_cache.RedisCache",
    "secret":"BREEDING",
    "timeout": 30*24*3600
}

TORNADO_USE_MAKO =True
#mako templates
MAKO = {
    "directories": [TEMPLATE_PATH], 
    "filesystem_checks": False,
    "collection_size": 500        
}

#log configuration
LOG = {        
    "path":os.path.join(PROJECT_PATH,'logs'), #日志文件路径
    "files":{'info':"INFO",'error':"ERROR",'debug':"DEBUG"}, #{filename:level}
}

#app register
APPS = ('app','admin')

#redis configuration
REDIS = {
    "default":{
        "host":"172.16.19.1",  #"192.168.1.32",
        "port":19000,
        "db":0,
        "password":"",
        "max_connections":100   
    }   
}

#mysql configuration
MYSQL = {   
         "default":{
                 "host":"172.16.19.12",
                 "port":3316,
                 "username":"feedu1",
                 "password":"x57s3P2p",
                 "database":"feed",
                 "query":{'charset':'utf8'}
        }               
}