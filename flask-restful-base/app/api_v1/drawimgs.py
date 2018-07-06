#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import abort, request, jsonify, session, send_from_directory
from flask_restful import Resource, reqparse
from datetime import datetime
from collections import OrderedDict

import logging
import json
import os

from . import restful_api
from common import imgs_path, SUCC, NOTFOUND
from auth.auth_server import check_login

def imgs_name():
    names = os.listdir(imgs_path)
    names = filter(lambda l: not l.endswith('json'), names)
    names.sort()
    #return list(enumerate(names))
    return names

class ShowImgs(Resource):
    @check_login()
    def get(self):
        filter_params = dict(request.args.items())
        page_index = 1
        page_size = 10
        names = imgs_name()
        total = len(names)
        for k, v in filter_params.items():
            if k == 'current':
                page_index = int(filter_params['current']) 
            elif k == 'pageSize':
                page_size =  int(filter_params['pageSize'])
        
        pagination = dict(
            total   = total,
            current = page_index,
            pageSize = page_size
        )
        if page_index * page_size <= total:
            names = names[(page_index - 1) * page_size : page_index * page_size]
        else:
            names = names[(page_index - 1) * page_size :]
        r_dic = dict(
            info    = names,
            pagination = pagination
        )
        return jsonify(r_dic)

class ShowImg(Resource):
    def get(self, name):
        return send_from_directory(imgs_path, name, as_attachment=True)

class ImgInfo(Resource):
    def get(self):
        pass

class SavePoints(Resource):
    def post(self):
        datas = request.get_json(force=True)
        img_name = datas['imgname']
        json_path = os.path.join(imgs_path, img_name.split('.')[0] + '.json')
        with open(json_path, 'wb') as f:
            json.dump(datas, f, indent=4, ensure_ascii=False)
        return jsonify(SUCC)    

class GetPoints(Resource):
    def get(self, name):
        json_path = os.path.join(imgs_path, name.split('.')[0] + '.json')
        data = {}
        if not os.path.exists(json_path):
            r_dict = dict(
                imgname = name,
                shapes = []
            )
            return jsonify(r_dict)
        with open(json_path, 'r') as f:
            data = json.load(f)
            return jsonify(data)




restful_api.add_resource(ShowImg, '/showimgs/<string:name>')
restful_api.add_resource(ShowImgs, '/showimgs')
restful_api.add_resource(SavePoints, '/savepoints')
restful_api.add_resource(GetPoints, '/getpoints/<string:name>')

