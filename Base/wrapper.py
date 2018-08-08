#!/usr/bin/python
# encoding:utf8
import functools
from flask import  session, jsonify, request
from session import WebSessionInterface
from extensions import UserReadSession
from pyutil.data.model.user import User
from pyutil.data.session.common import create_session
from pyutil.data.session.session import UID_SESSION_KEY


USER_NOT_LOGGED_IN  = dict(code=403, message='请登陆')
USER_UNAUTHORIZED   = dict(code=401, message='无操作权限')

PERM_MODEL_UPLOAD       = 0x0080    #上传权限
PERM_MODEL_DOWNLOAD     = 0x0100    #下载权限
PERM_MODEL_PUBLISH      = 0x0200    #发布权限
PERM_MODEL_QUERY        = 0x0400    #遍历权限
PERM_MODEL_MANAGE_BASE  = 0x0800    #基础管理
PERM_MODEL_MANAGE_DEV   = 0x1000    #模型管理平台开发权限
PERM_MODEL_MANAGE_CONVERT = 0x2000  #模型转换

def check_login():    
    def wrapper(func):
        @functools.wraps(func)
        def decorator(*args, **kwargs):
            urs = UserReadSession()
            if not session[UID_SESSION_KEY]:
                return jsonify(USER_NOT_LOGGED_IN)
            user = urs.query(User).get(session[UID_SESSION_KEY])
            urs.close()
            request.user = user
            return func(*args, **kwargs)
        return decorator
    return wrapper
 
#带参数的装饰器
 def check_permission(perm):    
    def wrapper(func):
        @functools.wraps(func)
        def decorator(*args, **kwargs):
            urs = UserReadSession()
            if not session[UID_SESSION_KEY]:
                return jsonify(USER_NOT_LOGGED_IN)

            user = urs.query(User).get(session[UID_SESSION_KEY])
            urs.close()
            if not user or not (user.permission & perm) or user.status != 0:
                return jsonify(USER_UNAUTHORIZED)

            request.user = user
            return func(*args, **kwargs)
        return decorator
    return wrapper

#装饰器内部传参
import datetime
 
class ca:
    def __init__(self):
        self.value='initial'
        self.stat='ok'
        
    def domethod(self):
        self.value='changed'
        self.stat='dump'
        print 'The value is %s'%self.value
        print 'The stat is %s'%self.stat
        return self
 
    def backhome(self):
        self.value='initial'
        print 'The value is back to %s'%self.value
 
    def setok(self):
        self.stat='ok'
        print 'The stat is %s'%self.stat
 
def dec(func):
    def _dec(*a,**ka):
        InOfa=ca()
        targetargs=InOfa.domethod()
        res=func(targetargs,*a,**ka)
        res[0].setok()
        return res[1]
    return _dec
 
@dec
def thecorefunc(targetargs,date=datetime.date.today()):
    print date
    targetargs.backhome()
    return (targetargs,date)
 
if __name__=='__main__':
    thecorefunc()
