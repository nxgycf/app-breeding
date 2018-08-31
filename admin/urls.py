#coding:utf-8

'''
Created on 2017年2月13日
@author: shuai.chen
'''

from admin.handlers import admin as ad
from admin.handlers import manage as mg
from admin.handlers import goods, deliver, user

urls = [  
      (r'/admin', ad.IndexHandler),
      (r'/admin/login', ad.LoginHandler),
      (r'/admin/main', ad.MainHandler),
      (r'/admin/left', ad.LeftHandler),
      (r'/admin/logout', ad.LogoutHandler),
      
      (r'/admin/mod_pass', mg.ModifyPasswordHandler),
      (r'/admin/add_admin', mg.AddAdminHandler),
      (r'/admin/look_admins', mg.LookAdminHandler),
      (r'/admin/del_admin', mg.DelAdminHandler),
      
      (r'/admin/look_user', user.LookUsertHandler),
      (r'/admin/ad_pics', user.AdPicUploadHandler),
      
      (r'/admin/goods_list', goods.GoodsListHandler),
      (r'/admin/add_goods', goods.AddGoodsHandler),   
      (r'/admin/goods_detail', goods.GoodsDetailHandler),
      (r'/admin/add_goods_icon', goods.AddGoodsIconHandler),
      (r'/admin/remove_goods', goods.GoodsRemoveHandler), 
      (r'/admin/open_region', goods.OpenRegionHandler),   
      (r'/admin/discount', goods.DiscountHnadler), 
      
      (r'/admin/delivered_list', deliver.DeliveredListHandler),  
      (r'/admin/deliver_list', deliver.DeliverListHandler),  
      (r'/admin/deliver', deliver.DeliverHandler), 
]