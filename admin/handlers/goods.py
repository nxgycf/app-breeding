# -*- coding: utf-8 -*-

'''
Created on 2018年7月26日

@author: shuai.chen
'''

from __future__ import absolute_import

import os
import time
import json

from towgo.handler import TornadoHttpHandler
from towgo.msetting import settings
from towgo.cache.db_cache import RedisCache

from admin.common.result import returns
from app.services.goods import GoodsService
from app.models.goods import GoodsInfo, GoodsPicture
from app.models.other import AvatarInfo
from app.services.other import AvatarService
from app.services.goods import GoodsPictureService

from admin.common import constants
from common import keys


class GoodsListHandler(TornadoHttpHandler):

    @returns(need_login=True)  
    def _post(self):
        return self._get()
            
    @returns(need_login=True)  
    def _get(self):
        service = GoodsService(GoodsInfo)
        li = service.gets()

        return self.render_html('admin/goods_list.html', li=li, tp=constants.GOODS_TYPE) 
        
class GoodsDetailHandler(TornadoHttpHandler):   
    
    def __init__(self, *args, **kwargs):
        super(GoodsDetailHandler, self).__init__(*args, **kwargs)  
        
        self.goods_service = GoodsPictureService(GoodsPicture)
        self.avatar_service = AvatarService(AvatarInfo)

    @returns(need_login=True)  
    def _get(self):   
        goods_id = self.get_argument("goods_id")  
#         code = self.get_argument("code")  
        goods = GoodsService(GoodsInfo).get(id=int(goods_id)) 

        _, icon, big, pics = self.get_goods_pics(goods.avatar_id, goods.id)        
        gtype = constants.GOODS_TYPE[goods.type]
        return self.render_html('admin/goods_detail.html', 
                    **{'code':goods.code,'name':goods.name,'price':goods.price,'feed_day':goods.feed_day,
                       'number':goods.number,'brief':goods.brief,'detail':goods.detail,'id':goods.id,
                       'status':[u'正常',u'下架'][goods.status],'icon':icon, 'pics':pics, 'type':gtype, 'big':big})                

    def get_goods_pics(self, avatar_id, goods_id):
        avatar = self.avatar_service.get(id=avatar_id)
        icon = os.path.join(settings.AVATAR_URL, avatar.filename) if avatar else ''        
        
        big = None
        pics = []
        pictures = self.goods_service.gets(goods_id=goods_id)
        for pic in pictures:
            url = os.path.join(settings.GOODS_PICTURE_URL, pic.filename)
            if pic.type == 1:
                big = (pic.id, url)
            else:    
                pics.append((pic.id, url))  
        return avatar, icon, big, pics                

        
class AddGoodsHandler(TornadoHttpHandler):

    @returns(need_login=True)  
    def _get(self):
        if self.admin.level < 2:
            return self.render_html('admin/error.html',msg="no permission!") 
        sign = self.get_argument("sign","0")
        if sign == "1":
            goods_id = self.get_argument("goods_id") 
#             code = self.get_argument("code")
            service = GoodsService(GoodsInfo)
            goods = service.get(id=int(goods_id))
            return self.render_html('admin/add_goods.html',msg=None, sign=sign,
                        **{'code':goods.code,'name':goods.name,'price':goods.price,'feed_day':goods.feed_day,
                           'number':goods.number,'brief':goods.brief,'detail':goods.detail,'status':goods.status,
                           'type':goods.type, 'types':constants.GOODS_TYPE.items(), 'id':goods.id})                 
        else:
            return self.render_html('admin/add_goods.html',msg=None, sign=sign,
                        **{'code':'','name':'','price':'','feed_day':'','number':'','brief':'','id':0,
                           'detail':'','status':0,'type':1, 'types':constants.GOODS_TYPE.items()}) 
            
    @returns(need_login=True)  
    def _post(self):
        if self.admin.level < 2:
            return self.render_html('admin/error.html',msg="no permission!") 
        
        sign = self.get_argument("sign",0)
        goods_id = self.get_argument("goods_id", 0) or 0
        code = self.get_argument("code",0) or 0
        name = self.get_argument("name","")  
        price = self.get_argument("price",0) or 0
        feed_day = self.get_argument("feed_day",1) or 1  
        number = self.get_argument("number",0) or 0
        brief = self.get_argument("brief","")  
        detail = self.get_argument("detail","")  
        status = self.get_argument("status",0)  or 0
        goods_type = self.get_argument("type",1)  or 1

        info = {'code':int(code),'name':name,'price':float(price),'feed_day':int(feed_day),'id':int(goods_id),
               'number':int(number),'brief':brief,'detail':detail, 'status':int(status),'type':goods_type,
               'types':constants.GOODS_TYPE.items()}
                
        if not all([code, name, price, feed_day, number]):
            return self.render_html('admin/add_goods.html',sign=sign, msg=u"字段不能为空！",**info) 

        service = GoodsService(GoodsInfo)
        if sign == "1":
            goods = service.get(id=int(goods_id)) 
            if not goods:
                return self.render_html('admin/add_goods.html', sign=sign, msg=u"该商品不存在!", **info)   
            else:
                info.pop('code')
                info.pop('id')
                info.pop('types')
                service.update(info,**{'id':goods.id})            
        else:  
            info.pop('id')
            info.pop('types')
            service.insert(info)
                    
        self.redirect('/admin/goods_list')  

class AddGoodsIconHandler(GoodsDetailHandler):     

    @returns(need_login=True)  
    def _get(self):  
        if self.admin.level < 2:
            return self.render_html('admin/error.html',msg="no permission!")     
        
        goods_id = self.get_argument("goods_id", 0) 
#         code = int(self.get_argument("code"))  
        goods = GoodsService(GoodsInfo).get(id=int(goods_id)) 
        
        _, icon, big, pics = self.get_goods_pics(goods.avatar_id, goods.id) 
        return self.render_html('admin/goods_icon.html', 
                    **{'code':goods.code, 'id':goods.id, 'name':goods.name, 'icon':icon, 'pics':pics, 'big':big})   
        
    @returns(need_login=True)  
    def _post(self):
        if self.admin.level < 2:
            return self.render_html('admin/error.html',msg="no permission!")   

#         code = int(self.get_argument("code")) 
        goods_id = int(self.get_argument("goods_id", 0))
        goods_service = GoodsService(GoodsInfo)
        goods = goods_service.get(id=goods_id) 
        
        avatar, icon, big, pics = self.get_goods_pics(goods.avatar_id, goods.id) 
        info = {'code':goods.code, 'id':goods.id, 'name':goods.name, 'icon':icon, 'pics':pics, 'big':big}
        
        sign = int(self.get_argument("sign", 0))
        if sign in [1, 2, 3]:
            upload_file = self.request.files.get('file',None)
            if upload_file is None:
                return self.render_string('admin/goods_icon.html',msg=u"请选择要上传的文件!", **info)   
    
            file_name = upload_file[0].get('filename')
            suffix = file_name.split('.')[-1]
            if suffix not in ['jpg', 'png', 'jpeg']:
                return self.render_string('admin/goods_icon.html',msg=u"需要上传 jpg/png/jpeg 文件!", **info)   
    
            body =  upload_file[0].get('body')
            if sign == 1:
                aid = self.upload_icon(body, goods_id, suffix)
                goods_service.update({'avatar_id':aid}, **{'id':goods_id})
                
                if avatar:
                    self.avatar_service.delete(avatar)
                    os.remove(os.path.join(settings.AVATAR_PATH, avatar.filename))
            elif sign == 2:
                self.upload_picture(body, goods_id, suffix, 1)   
                if big:
                    self.delete_pic(big[0])   
            elif sign == 3:
                if len(pics) >= constants.GOODS_PIC_LIMIT:
                    return self.render_string('admin/goods_icon.html',
                                              msg=u"每个商品不能超过%d张图片!" % constants.GOODS_PIC_LIMIT, **info) 
                else:
                    self.upload_picture(body, goods_id, suffix, 0)
        else:
            #delete picture
            pid = int(self.get_argument("pid", 0))  
            self.delete_pic(pid)
                         
        self.redirect('/admin/add_goods_icon?goods_id='+str(goods.id))
        
    def delete_pic(self, pid): 
        pic = self.goods_service.get(id=pid)
        self.goods_service.delete(pic)
        os.remove(os.path.join(settings.GOODS_PICTURE_PATH, pic.filename)) 
        
    def upload_icon(self, body, goods_id, suffix):
        icon_id = int(time.time()*1000)
        file_name = str.format('{0}_{1}.{2}', str(goods_id), str(icon_id), suffix)
        fname = os.path.join(settings.AVATAR_PATH, file_name)
        with open(fname,'w+') as _f:
            _f.write(body)
            _f.close()
         
        avatar = AvatarInfo()
        avatar.id = icon_id
        avatar.filename = file_name
        avatar.type = suffix
        avatar.path = ""  
        
        aservice = AvatarService(AvatarInfo)
        aservice.insert(avatar)
        return icon_id 

    def upload_picture(self, body, goods_id, suffix, tp):  
        '''
        @param tp: 1:详图 2：header图
        '''
        pic_id = int(time.time()*1000)
        file_name = str.format('{0}_{1}.{2}', str(goods_id), str(pic_id), suffix) 
        fname = os.path.join(settings.GOODS_PICTURE_PATH, file_name)
        with open(fname,'w+') as _f:
            _f.write(body)
            _f.close() 
            
        goods_picture = GoodsPicture()
        goods_picture.id = pic_id
        goods_picture.goods_id = goods_id
        goods_picture.filename = file_name
        goods_picture.type = tp
        goods_picture.path = ""  
        
        gservice = GoodsPictureService(GoodsPicture)
        gservice.insert(goods_picture)        
               

class GoodsRemoveHandler(TornadoHttpHandler):     

    @returns(need_login=True)  
    def _get(self):  
        if self.admin.level < 2:
            return self.render_html('admin/error.html',msg="no permission!") 
                  
#         code = self.get_argument("code")  
        goods_id = self.get_argument("goods_id")
        
        service = GoodsService(GoodsInfo)
        goods = service.get(code=id(goods_id)) 
        if goods:
            service.delete(goods)

        self.redirect('/admin/goods_list')   


class DiscountHnadler(TornadoHttpHandler): 
    
    def __init__(self, *args, **kwargs):
        super(DiscountHnadler, self).__init__(*args, **kwargs)  
        self.cache = RedisCache()
     
    @returns(need_login=True)  
    def _get(self):
        if self.admin.level < 2:
            return self.render_html('admin/error.html',msg="no permission!") 
        
        sign = self.get_argument("sign", "0")
        if sign == "1":
            dtype = self.get_argument("type")
            goods_id =  self.get_argument("goods_id")
            self.cache.hdel(keys.DISCOUNT.format(dtype), goods_id)
                    
        info_1 = self.cache.hgetall(keys.DISCOUNT.format(1))
        info_2 = self.cache.hgetall(keys.DISCOUNT.format(2))
        info = {}
        for k,v in info_1.iteritems():
            value = json.loads(v)
            value['type'] = 1
            info[k] = [value]
        for k,v in info_2.iteritems():   
            value = json.loads(v)
            value['type'] = 2
            if k in info:
                info[k].append(value)
            else:
                info[k] = [value]        
        return self.render_html('admin/discount.html',infos=info.items(),msg="") 
    
    @returns(need_login=True)  
    def _post(self):
        if self.admin.level < 2:
            return self.render_html('admin/error.html',msg="no permission!") 
        
        dtype = self.get_argument("type")
        goods_id =  self.get_argument("goods_id")
        start = self.get_argument("start")
        end = self.get_argument("end")
        if not all([goods_id, start, end]):
            return self.render_html('admin/error.html',msg="fields is required!")  

        goods = GoodsService(GoodsInfo).get(id=int(goods_id)) 
        if not goods:
            return self.render_html('admin/error.html', msg=u"商品ID:%s, 该商品不存在!" % goods_id)     
            
        if dtype == "1":
            discount = self.get_argument("discount")
            desc = self.get_argument("desc")
            info = {'start':start, 'end':end, 'discount':discount,'desc':desc}
            self.cache.hset(keys.DISCOUNT.format(1), goods_id, json.dumps(info))
        elif dtype == "2":
            num = self.get_argument("num")
            amount = self.get_argument("amount")
            info = {'start':start, 'end':end, 'num':num,'amount':amount}
            self.cache.hset(keys.DISCOUNT.format(2), goods_id, json.dumps(info))
            
        self.redirect('/admin/discount')
        
class OpenRegionHandler(TornadoHttpHandler):
 
    def __init__(self, *args, **kwargs):
        super(OpenRegionHandler, self).__init__(*args, **kwargs)  
        self.cache = RedisCache()
           
    @returns(need_login=True)  
    def _get(self):  
        if self.admin.level < 2:
            return self.render_html('admin/error.html',msg="no permission!") 
        
        sign = self.get_argument("sign", "0")
        if sign == "1":
            goods_id = self.get_argument("goods_id") 
            self.cache.hdel(keys.OPEN_REGION, goods_id)
        
        info = self.cache.hgetall(keys.OPEN_REGION)
        return self.render_html('admin/open_region.html', info=info.items())
        
    @returns(need_login=True)  
    def _post(self):  
        if self.admin.level < 2:
            return self.render_html('admin/error.html',msg="no permission!") 
        
        goods_id = self.get_argument("goods_id")    
        region_ids = self.get_argument("region_ids", '')   
        
        key = keys.OPEN_REGION
        if goods_id and region_ids:
            goods = GoodsService(GoodsInfo).get(id=int(goods_id)) 
            if not goods:
                return self.render_html('admin/error.html', msg=u"商品ID:%s, 该商品不存在!" % goods_id)   
            
            ids = []
            region_ids = region_ids.replace(' ', '')
            for rid in region_ids.split(','):
                if '-' in rid:
                    s, e = rid.split('-')
                    ids.extend(map(str, range(int(s), int(e) + 1)))
                else:
                    ids.append(rid)     
                
            self.cache.hset(key, goods_id, ','.join(ids))
            
        self.redirect('/admin/open_region')  
        
            