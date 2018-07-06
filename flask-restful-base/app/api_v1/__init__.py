#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import  Blueprint
from flask_restful import Api

api_v1_blueprint = Blueprint(
    'api/1.0',
    __name__,
    url_prefix='/api/1.0')
    
    
restful_api = Api(api_v1_blueprint)

from . import drawimgs 
