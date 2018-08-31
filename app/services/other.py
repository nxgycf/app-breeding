# -*- coding: utf-8 -*-

'''
Created on 2018年7月31日

@author: shuai.chen
'''

from __future__ import absolute_import

from base.service import Service
from base.cache import do_cache
from common import keys

class AvatarService(Service):

    @do_cache(keys.AVATAR, timeout=0)
    def get(self, **condition):
        return super(AvatarService, self).get(**condition)
    
    def delete(self, obj):
        self.cache.delete(keys.AVATAR % {'id':obj.id})
        return super(AvatarService, self).delete(obj)    
    