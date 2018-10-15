#coding:utf-8

'''
Created on 2017年2月13日
@author: shuai.chen
'''

import re
import hashlib
import datetime
import random
import uuid

def get_password(password):
    '''
    获取原始密码md5值
    '''
    return hashlib.md5(password.encode('UTF8')).hexdigest()

def get_order_code():
    '''
    生成订单号
    '''
    now = datetime.datetime.now()
    series = []
    
    f = lambda x:"0{0}".format(x) if x<10 else str(x)
    series.append(str(now.year)[2:])
    series.append(f(now.month))
    series.append(f(now.day))
    series.append(f(now.hour))
    series.append(f(now.minute))
    series.append(f(now.second))
    series.append(str(now.microsecond))
    
    return ''.join(series)

def check_account(account):
    '''
    验证账号
    '''
    pat = r'^\d{11}$'
    return re.match(pat, account)

def check_password(password):
    '''
    ceck password
    '''
    pat = r"^[a-zA-Z0-9]{6,16}$"
    return re.match(pat, password)

def gen_verify_code():
    '''
    生成验证码
    '''
    return random.randint(100000,999999)

def MD5(string):
    '''
    generate md5 string
    '''
    md5 = hashlib.md5()
    md5.update(string.encode('utf-8'))
    return md5.hexdigest()

def get_nonce_str():
    '''
    随机字符串
    '''
    return ''.join(str(uuid.uuid4()).split('-'))    

def check_number_str(string):
    '''
    check number string seperate with comma
    '''
    pat = r'^\d+(,{1}\d+)*$'   
    return re.match(pat,string)


if __name__ == "__main__":
    print(check_account(''))
    print(check_password('123456'))
    print(get_order_code())
    print(gen_verify_code())

