# -*- coding: utf-8 -*-
# filename: basic.py
import urllib
import time
import json

class Basic:    
    def __init__(self):        
        self.__accessToken = ''        
        self.__leftTime = 0    

    def __real_get_access_token(self):        
        appId = "wx6aad3116fe8ab187"        
        appSecret = "b1cf48e18e8114e31707a5c09381abc3"        
        postUrl = ("https://api.weixin.qq.com/cgi-bin/token?grant_type="               
            "client_credential&appid=%s&secret=%s" % (appId, appSecret))        
        urlResp = urllib.urlopen(postUrl)        
        urlResp = json.loads(urlResp.read())                
        self.__accessToken = urlResp['access_token']        
        self.__leftTime = urlResp['expires_in']    

    def get_access_token(self):        
        if self.__leftTime < 10:            
            self.__real_get_access_token()    
        return self.__accessToken    

    def run(self):        
        while(True):            
            if self.__leftTime > 10:                
                time.sleep(2)                
                self.__leftTime -= 2            
                print 2
            else:                
                self.__real_get_access_token()
                print self.__accessToken

x = Basic()
x.run()
