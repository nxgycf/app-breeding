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

XSRF_COOKIES = False
COOKIE_SECRET = "BREEDING"

#session configuration
SESSION = {
    "open":True, #是否开启session           
    "storage":"towgo.cache.local_cache.LocalCache",
    "secret":"BREEDING",
    "timeout": 7*24*3600
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
        "host":"192.168.1.165",
        "port":6381,
        "db":0,
        "password":"",
        "max_connections":100   
    }   
}

#mysql configuration
MYSQL = {
         "default":{
                 "host":"127.0.0.1",
                 "port":3306,
                 "username":"root",
                 "password":"root",
                 "database":"breeding",
                 "query":{'charset':'utf8'}
            }         
}

#icon picture save path
AVATAR_PATH = "/Users/shuai.chen/Pictures/avatar"
GOODS_PICTURE_PATH = "/Users/shuai.chen/Pictures/goods_picture"

#icon picture access path
AVATAR_URL = "http://192.168.46.103:8013/avatar/"
GOODS_PICTURE_URL  = "http://192.168.46.103:8013/goods_picture/"

#WeChat PAY
PAY_NOTICE_URL = "http://192.168.46.103:8012/pay/notice"
