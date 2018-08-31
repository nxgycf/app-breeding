#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2016年4月22日

@author: shuai.chen

根据 MYSQL 表结构转换成 SQLALCHEMY model
'''

sql = \
"""id INTEGER NOT NULL PRIMARY KEY,
region_code VARCHAR(8) NOT NULL COMMENT '地区编码',
region_name VARCHAR(32) NOT NULL DEFAULT '' comment '地区名字',
region_level TINYINT NOT NULL DEFAULT 0 comment '级别',
city_code VARCHAR(6) NOT NULL DEFAULT '' comment '区号',
center VARCHAR(32) NOT NULL DEFAULT '' COMMENT '城市中心点（即：经纬度坐标）',
parent_id INTEGER NOT NULL DEFAULT -1 comment '父级ID',
"""
  

def gen():
    li = sql.split(',\n')
    for s in li:
        ft = ''
        ee = s.split(' ')
        if len(ee) < 3:
            continue
        
        ty = ee[1]
        if ty.upper() == "BIGINT":
            ft = "BigInteger"
        elif ty.upper() == "INTEGER":
            ft = 'Integer'
        elif ty.upper() in ['TINYINT', 'SMALLINT']:
            ft = 'SmallInteger'
        elif ty.upper().startswith('VARCHAR'):
            ft = 'String%s'%ty[7:]
        elif ty.upper().startswith("CHAR"):
            ft = 'String%s'%ty[4:]                       
        elif ty.upper() in ['TIMESTAMP' ,'DATETIME']:
            ft = 'DateTime'
        elif ty.upper() in ['DATE']:
            ft = 'Date'            
        elif ty.upper() in ['FLOAT','DECIMAL', 'DOUBLE']:
            ft = 'Float'         
        elif ty.upper() == "LONGTEXT":
            ft = 'String'   
        
        field = ee[0]
        code = "%s = Column('%s',%s"%(field,field,ft)
        
        add = ""
        if 'AUTO_INCREMENT' in s:
            add += ",primary_key=True,autoincrement=True"
        if 'NOT NULL' in s:
            add += ",nullable=False"
        if 'DEFAULT' in ee:
            index = ee.index("DEFAULT")
            
            v = ee[index+1]
            if v in ["NULL","null"]:
                defalut = None
            elif ft.find('Int') != -1 or ft in ['Float']:
                import re
                defalut = int(re.compile(r'\d+').search(v).group())     
            elif ft == "DateTime":
                defalut = "datetime.datetime.now,server_default=text('CURRENT_TIMESTAMP')"   
            else:
                defalut = v    
            
            add += ",default=%s"%defalut
            
        if add:
            code += add    
                           
        code += ')'
            
        if not code.startswith('0'):
            print '   ',code


if __name__ == "__main__":
    gen()