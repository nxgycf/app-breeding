#coding:utf-8


import traceback

def initialize():
    '''
    initialize method
    '''
    from towgo.log.log_util import CommonLog
    try:
        #init result code
        from app.common import result
        result.get_msg(0)
            
        from towgo.msetting import settings
        #init redis
        from towgo.cache.db_cache import RedisCache
        for rcn,rconfigs in settings.REDIS.iteritems():
            RedisCache.connect(rcn,**rconfigs)     
               
        #init mysql
        from towgo.dbs.alchemy import Connection
        for mcn,mconfigs in settings.MYSQL.iteritems():
            Connection.connect(mcn,**mconfigs)  
        
    except:
        CommonLog.error("initialize: %s" % traceback.format_exc())
            