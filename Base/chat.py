#!/usr/bin/env python
# -*- coding: utf-8 -*-  
import urllib  
import json  
      
def getHtml(url):  
    page = urllib.urlopen(url)  
    html = page.read()  
    return html  
      
if __name__ == '__main__':  
    key = '7c8512ee6038496080717e75cbb2ff09'  
    api = 'http://www.tuling123.com/openapi/api?key=' + key + '&info='  
    while True:  
        info = raw_input('我: ')  
        request = api + info  
        response = getHtml(request)  
        dic_json = json.loads(response)  
        print '机器人: '.decode('utf-8') + dic_json['text']  