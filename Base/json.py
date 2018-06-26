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

data = [ { 'a' : 1, 'b' : 2, 'c' : 3, 'd' : 4, 'e' : 5 } ]
#将python对象转化为json字符串
#语法
#json.dumps(obj, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, cls=None, indent=None, separators=None, encoding="utf-8", default=None, sort_keys=False, **kw)
json = json.dumps(data)
print json

jsonData = '{"a":1,"b":2,"c":3,"d":4,"e":5}';
#将已编码的 JSON 字符串解码为 Python 对象
#语法
#json.loads(s[, encoding[, cls[, object_hook[, parse_float[, parse_int[, parse_constant[, object_pairs_hook[, **kw]]]]]]]])
text = json.loads(jsonData)
print text
