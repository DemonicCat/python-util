#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

#数据保存到.json文件
#data = {}
def writeJson(data, json_file_path):
    with open(json_file_path,'wb') as f:
        json.dump(data,f,indent=4,ensure_ascii=False)
        
#读取.json文件
#data={} #存放读取的数据
def readJson(json_file_path):
    with open(json_file_path,'r') as f:
        data=json.load(f)
