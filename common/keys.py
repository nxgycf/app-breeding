# -*- coding: utf-8 -*-

'''
Created on 2018年8月17日

@author: shuai.chen
'''

# REDIS KEY
NORMAL_EXPIRE = 24*3600

GOODS_LIST = "goods_list_%(status)s"
GOODS = "goods_%(id)s"

GOODS_PICTURES = "goods_pictures_%(goods_id)s"
AVATAR = "avatar_%(id)s"

USER_ADDRESS_LIST = "user_address_list_%(user_id)s_%(status)s"
USER_ADDRESS = "user_address_%(id)s_%(status)s"

ORDER_LIST = "order_list_%(user_id)s"
ORDER = "order_%(id)s"
ORDER_CODE = "order_code_%(code)s"

DELIVER = "deliver_%(user_goods_id)s"
USER_PAY = "user_pay_%(user_goods_id)s"

# 验证码
VERIFY_CODE = "verify_code_{0}" #verify_code_{phone}
VERIFY_CODE_TIME = "verify_code_time_{0}"  #verify_code_time_{phone}
VERIFY_CODE_EXPIRE = 5*60
VERIFY_CODE_TIME_EXPIRE = 60

# 后台
DISCOUNT = "discount_{0}" #discount_{type}  type 1:折扣 2:满减
OPEN_REGION = "open_region" #open_region
