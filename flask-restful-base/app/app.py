#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask_cors import *
from config import conf
from auth.session import WebSessionInterface

def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    app.session_interface = WebSessionInterface()
    app.config['SESSION_COOKIE_NAME'] = 'sessionid'
    
    # Import the views module
    
    from api_v1 import  api_v1_blueprint
    app.register_blueprint(api_v1_blueprint)
    
    return app


if __name__ == '__main__':
    app = create_app()
    # Entry the application 
    app.run(host='0.0.0.0', port=16083, debug=True, threaded=True)
