# -*- coding: utf-8 -*-

'''
Created on 2018年8月21日

@author: shuai.chen
'''

#云片短信服务
YUNPIAN_SHORTMSG = "https://sms.yunpian.com/v2/sms/single_send.json"
YUNPIAN_APIKEY = ""
VERIFY_CODE_TEXT = u"[塞上农场]您的验证码是 : {0}"


# 微信配置基础数据
WBC = {
    'APPID': 'wx0ab9673f89929f45',
    'APPSECRET': 'b65198d7845dcdf37a7a4ed2ed77ba2f',
    'MCHID': '14222000000',
    'KEY': 'd7810713e1exxxxxxxxxxadc9617d0a6',
    'GOODDESC': u'商户号中的公司简称或全称-无要求的商品名字',
    'NOTIFY_URL': 'https://www.xxxx.com/service/applesson/wechatordernotice', 
}

#微信支付
WECHAT_UNIFIED_ORDER = "https://api.mch.weixin.qq.com/pay/unifiedorder"
WECHAT_QUERY_ORDER = "https://api.mch.weixin.qq.com/pay/orderquery"

# 微信用户登录
REDIRECT_URL = "http://192.168.46.103:8012/user/login"

WECHAT_AUTH = """https://open.weixin.qq.com/connect/oauth2/authorize?appid={0}&redirect_uri={1}&response_type=code&scope=SCOPE&state=STATE"""
WECHAT_AUTH = WECHAT_AUTH.format(WBC['APPID'], REDIRECT_URL)

WECHAT_TOKEN = "https://api.weixin.qq.com/sns/oauth2/access_token?appid={0}&secret={1}&code={2}&grant_type=authorization_code"
WECHAT_USER_INFO = "https://api.weixin.qq.com/sns/userinfo?access_token={0}&openid={1}"
