#coding=utf8
from sqlalchemy import (Column, Integer, BigInteger, Text,
        Date, DateTime, SmallInteger, String, Numeric, orm, event)
from sqlalchemy.ext.declarative import declarative_base
from pyutil.data.easydict import EasyDict

import json
import hashlib
import base64
def make_password(raw):
    key = base64.b64encode(raw) + raw[0]
    return hashlib.sha1(key).hexdigest()

class JsonDataMixin(object):

    @property
    def data_dict(self):
        if not hasattr(self, '_data_dict'):
            self.init_on_load()
        return self._data_dict

    def init_on_load(self):
        if type(self.data) is dict:
            _data_dict = self.data
        else:
            _data_dict = json.loads(self.data) if self.data else {}
        self._data_dict = EasyDict(_data_dict)

    def save_data_dict(self):
        self.data = json.dumps(self.data_dict, sort_keys=True,
                indent=4, separators=(',', ':'))
        if hasattr(self, '_data_dict'):
            del self._data_dict

Base = declarative_base()
class User(Base, JsonDataMixin):
    PERM_ADMIN = 0xffffffffffff     # 所有权限
    PERM_CREATE_USER = 0x01         # 管理用户权限
    PERM_LICENSE = 0x02             # license平台权限
    PERM_DATA_ADMIN = 0x04          # 数据管理权限
    PERM_DATA_READ = 0x08           # 数据读权限
    PERM_DATA_WRITE = 0x10          # 数据写权限
    PERM_DATA_PLATFORM = 0x20       # 数据平台权限
    PERM_DATA_DELETE = 0x40         # 数据删除权限

    __tablename__ = 'user'
    id = Column(BigInteger, primary_key=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    permission = Column(BigInteger)    # mask of permission of sub system
    create_time = Column(DateTime)
    modify_time = Column(DateTime)
    status = Column(SmallInteger)
    data = Column(String)

    @property
    def depart(self):
        return self.data_dict.get('depart', '')

    @depart.setter
    def depart(self, _department):
        self._data_dict.depart = _depart

    @property
    def real_name(self):
        return self.data_dict.get('real_name', '')

    @real_name.setter
    def real_name(self, _real_name):
        self._data_dict.real_name = _real_name

    def set_password(self, raw):
        self.password = make_password(raw)

    def check_password(self, raw):
        return self.password == make_password(raw)

if __name__ == '__main__':
    import sys
    raw_pwd = sys.argv[1] if len(sys.argv) > 1 else '123456'
    print make_password(raw_pwd)
