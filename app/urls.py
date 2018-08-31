# -*- coding: utf-8 -*-

'''
Created on 2018年5月18日

@author: shuai.chen
'''

from app.handlers import goods, user

urls = [
    (r'/test', goods.Test),
    
    (r'/app', goods.Index),
    (r'/protocol', goods.Protocol),
    (r'/about', goods.About),
    (r'/send_code', goods.SendCode),
    
    (r'/goods/list', goods.GoodsList),
    (r'/goods/detail', goods.GoodsDetail),
    (r'/goods/buy', goods.BuyGoods),
    (r'/pay/result', goods.PayResult),
    (r'/pay/notice', goods.PayNotice),

    (r'/user/login', user.UserLogin), #WechatUserLogin  UserLogin
    (r'/user/info', user.PersonalInfo), #WechatUserInfo  PersonalInfo
        
    (r'/user/register', user.UserRegister), 
    (r'/user/reset_password', user.ResetPassword), 
    (r'/user/forget_password', user.ForgetPassword), 
    (r'/user/logout', user.UserLogout), 
    
    (r'/user/address_list', user.UserAddressList), 
    (r'/user/add_address', user.UserAddAddress), 
    (r'/user/edit_address', user.UserEditAddress), 
    (r'/user/remove_address', user.UserRemoveAddress),

    (r'/user/order_list', user.OrderList),
    (r'/user/order_detail', user.OrderDetail),
    (r'/user/select_address', goods.SelectAddress),
]