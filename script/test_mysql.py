# -*- coding: utf-8 -*-

'''
Created on 2018年8月3日

@author: shuai.chen
'''

import json
import datetime
from towgo.dbs.sqldb import Model, Column, SqlConn

MYSQL = {
         "default":{
                 "host":"127.0.0.1",
                 "port":3306,
                 "username":"root",
                 "password":"root",
                 "database":"breeding",
                 "query":{'charset':'utf8'},
                 
                 "mincached": 1,
                 "maxcached": 5,
                 "maxconnections": 100,
                 "blocking": True
            }         
}

for mcn,mconfigs in MYSQL.iteritems():
    SqlConn.connect(mcn,**mconfigs)  
    

class GoodsPicture(Model):  
    __connection_name__ = "default"
    __table_name__ = "goods_picture"    
    
    id = Column('id',primary_key=True,nullable=False)
    goods_id = Column('goods_id',nullable=False)    
    filename = Column('filename',nullable=False)
    type = Column('type',nullable=False)
    path = Column('path',nullable=False)
    create_date = Column('create_date',nullable=False,default=datetime.datetime.now)
    update_time = Column('update_time',nullable=False,default=datetime.datetime.now)

class Region(Model):
    """
    region
    """
    __table_name__ = "region" 
    __connection_name__ = "default"

    id = Column('id',primary_key=True,nullable=False)
    region_code = Column('region_code',nullable=False)
    region_name = Column('region_name',nullable=False,default='')
    region_level = Column('region_level',nullable=False,default=0)
    city_code = Column('city_code',nullable=False,default='')
    center = Column('center',nullable=False,default='')
    parent_id = Column('parent_id',nullable=False,default=1)


#{ id:'2',value:'北京',childs:[{id:'2',value:'北京',childs:[]}]}
m = {}

mt = {}
for region in Region.getmany(region_level=3):
    v = {'id':str(region.id),'value':region.region_name.decode('utf-8')}
    prid = str(region.parent_id)
    if prid in mt:
        mt[prid].append(v)
    else:
        mt[prid] = [v]    

st = {}
for region in Region.getmany(region_level=2):  
    v = {'id':str(region.id),'value':region.region_name.decode('utf-8')}
    if str(region.id)in mt:
        v['childs'] = mt[str(region.id)]
       
    prid = str(region.parent_id)
    if prid in st:
        st[prid].append(v)
    else:
        st[prid] = [v]    
     
ft = []
for region in Region.getmany(region_level=1):
    v = {'id':str(region.id),'value':region.region_name.decode('utf-8')}    
    if str(region.id) in st:
        v['childs'] = st[str(region.id)]
         
    ft.append(v) 
print json.dumps(ft)        

         
        