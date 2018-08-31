#-*- coding:utf-8 -*-

'''
Created on 2017年1月3日
@author: shuai.chen
@towgo: https://github.com/nxgych/towgo/releases/download/1.0.0/towgo-1.0.0.tar.gz
'''

from __future__ import absolute_import

import tornado
from tornado.options import define

define("port", default=8012, help="running on the port : 8012", type=int)
define("settings", default='settings.development', help="running on the environment : development", type=str)


if __name__ == "__main__":
    '''
    run server command:
    python main.py --settings=settings.development --port=7777
    '''    
    tornado.options.parse_command_line()

    from towgo.server import TornadoHttpServer
    from common import initialize
    
    server = TornadoHttpServer()
    server.setInitMethod(initialize)
    server.start()    
