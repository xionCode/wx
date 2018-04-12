# -*- coding: utf-8 -*-
import hashlib
import web
import lxml
import time
import os
import urllib2,json
import urllib
import re
import random
import hashlib
import cookielib
import requests
import math
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from bs4 import BeautifulSoup
from urllib import urlencode
from lxml import etree
from smtplib import SMTP_SSL
from email.header import Header
from email.mime.text import MIMEText

#session = requests.Session()
#s.config['keep_alivesession = requests.Session()
class WeixinInterface:

    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)

    def GET(self):
        #获取输入参数
        data = web.input()
        signature=data.signature
        timestamp=data.timestamp
        nonce=data.nonce
        echostr = data.echostr
        #自己的token
        token="hello" #这里改写你在微信公众平台里输入的token
        #字典序排序
        list=[token,timestamp,nonce]
        list.sort()
        sha1=hashlib.sha1()
        map(sha1.update,list)
        hashcode=sha1.hexdigest()
        #sha1加密算法

        #如果是来自微信的请求，则回复echostr
        if hashcode == signature:
            return echostr

    def POST(self): 
        str_xml = web.data() #获得post来的数据 
        xml = etree.fromstring(str_xml)#进行XML解析 
        msgType=xml.find("MsgType").text
        fromUser=xml.find("FromUserName").text 
        toUser=xml.find("ToUserName").text 
        if msgType == 'location':
            wdu = xml.find("Location_X").text
            wdu = float(wdu)
            
            jdu = xml.find("Location_Y").text
            jdu = float(jdu)
            #转换为百度标准
            x_pi = 3.14159265358979324 * 3000.0 / 180.0
            x = jdu
            y = wdu
            z = math.sqrt(x * x + y * y) + 0.00002 * math.sin(y * x_pi)
            theta = math.atan2(y, x) + 0.000003 * math.cos(x * x_pi)
            jdu = z * math.cos(theta) + 0.0065
            wdu = z * math.sin(theta) + 0.006
            wdu = str(wdu)
            jdu = str(jdu)
            Lmesag = u"您的位置："
            Lmesag += xml.find("Label").text
            myres = requests.get('http://d3.weather.com.cn/webgis_rain_new/webgis/ele?lat='+ wdu + '&lon='+ jdu + '&callback=fc5m&_=1470809429568')
            if myres.status_code != 200:
                if myres.status_code == 500:
                    status_error = u"服务器未响应，请稍后再试~"
                    return self.render.reply_text(fromUser,toUser,int(time.time()), status_error)
            myres.encoding = 'utf-8'
            text = myres.text
            text = text[9:-2]
            data = json.loads(text)
            pretime = data['time']
            msg = data['msg']
            pretime1 = u"查询时间："
            pretime1 += pretime
            msg1 = "天气预报：\n中国天气网雷达数据(雷达外推数据，仅供参考)："
            msg1 += msg
            Lmesag += '\n'
            Lmesag += pretime1
            Lmesag += '\n'
            Lmesag += msg1
            cyres = requests.get('http://www.caiyunapp.com/fcgi-bin/v1/api.py?lonlat=' + jdu + ',' + wdu + '&format=json&product=minutes_prec&token=96Ly7wgKGq6FhllM&random=0.8600497214532319')
            cyres.encoding = "utf-8"
            cyData = json.loads(cyres.text)
            cymsg = u"\n\n彩云天气数据(准确率较高):"
            #cymsg += cyData['summary']
            cytemp = u"\n温度："
            cytemp += str(cyData['temp'])
            cymsg += cytemp
            cymsg +=u"\n未来1小时天气预报："
            cymsg += cyData['summary']
            Lmesag += cymsg
            return self.render.reply_text(fromUser,toUser,int(time.time()), Lmesag)
        else:
            pass
