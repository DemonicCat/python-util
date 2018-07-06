#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyutil.data.session.common import create_session
from config import conf

db_conf = conf.db
ReadSession     = create_session(db_conf, write=False)
WriteSession    = create_session(db_conf, write=True)

paths = conf.path
imgs_path = paths['imgs_path']

from pyutil.log.log import init as init_log
init_log(conf.log)


SUCC = {'code': 201, 'message': 'succ'}
DELSUCC = {'code': 204, 'message': 'del succ'}
ERROR = {'code': 400, 'message': 'inner error'}
NOAUTH = {'code': 401, 'message': '无操作权限'}
NOTFOUND = {'code': 404, 'message': '不存在'}


