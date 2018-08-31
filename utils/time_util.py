#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2016年4月27日

@author: shuai.chen
'''

#时间格式相互转换


from datetime import datetime, timedelta, date
import time


def to_str(dt,ft="%Y-%m-%d %H:%M:%S"):
    """
    将时间对象或时间戳转换成时间字符串
    """
    if isinstance(dt, datetime):
        return dt.strftime(ft)
    if isinstance(dt, long) or isinstance(dt, int) or isinstance(dt, float):
        ldt = long(dt)
        if ldt > 10**12:
            return datetime.fromtimestamp(ldt/1000).strftime(ft)
        return datetime.fromtimestamp(ldt).strftime(ft)  
    return dt


def to_dt(sdt):
    """
    将时间字符串或时间戳转换成时间对象
    """
    if isinstance(sdt, str) or isinstance(sdt, unicode):
        sdt = str(sdt).strip()
        if ":" not in sdt:
            return datetime.strptime(sdt, "%Y-%m-%d")
        return datetime.strptime(sdt, "%Y-%m-%d %H:%M:%S")
    if isinstance(sdt, long) or isinstance(sdt, int) or isinstance(sdt, float):
        ldt = long(sdt)     
        if ldt > 10**12:
            return datetime.fromtimestamp(ldt/1000)
        return datetime.fromtimestamp(ldt)   
    return sdt    
    

def to_ts(dt):
    """
    将时间对象或时间字符串转换成时间戳
    """ 
    if isinstance(dt,datetime):
        return long(time.mktime(dt.timetuple()))
    if isinstance(dt, str) or isinstance(dt, unicode):
        dt = str(dt).strip()
        if ":" not in dt:
            dto = time.strptime(dt, "%Y-%m-%d")
            return long(time.mktime(dto))
        dto = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
        return long(time.mktime(dto))
    return dt


def to_date(sdt):
    """
    将时间字符串或时间戳转换成日期对象
    """
    if isinstance(sdt, str) or isinstance(sdt, unicode):
        sdt = str(sdt).strip()
        if ":" not in sdt:
            return datetime.strptime(sdt, "%Y-%m-%d").date()
        return datetime.strptime(sdt, "%Y-%m-%d %H:%M:%S").date()
    if isinstance(sdt, long) or isinstance(sdt, int) or isinstance(sdt, float):
        ldt = long(sdt)     
        if ldt > 10**12:
            return date.fromtimestamp(ldt/1000)
        return date.fromtimestamp(ldt)   
    return sdt 

def delta_str(dateStr=time.strftime("%Y-%m-%d"), delta=1, ft="%Y-%m-%d"):
    """
    接收一个日期字符串，时间格式，和偏移的天数，返回时间偏移后的日期字符串
    """
    baseDate =  datetime.strptime(dateStr, ft).date()
    deltaDate = baseDate + timedelta(days=delta)
    return deltaDate.strftime(ft) 

def delta_dt(dt=datetime.now(), delta=1):
    '''
    返回间隔天数后的对象
    '''
    return dt + timedelta(days=delta)

if __name__ == "__main__":
    print to_dt(1461721279458L) 
    print to_dt("2015-08-10 10:02:33") 

    print to_str(1461722832,'%Y-%m-%d %H:%M:%S')
    print to_str(datetime.now(),'%Y-%m-%d %H:%M:%S')
    
    print to_ts("2015-08-10 10:02:33")
    print to_ts(datetime.now())

    print to_date(1461721279458L) 
    print to_date("2015-08-10 10:02:33")      
    