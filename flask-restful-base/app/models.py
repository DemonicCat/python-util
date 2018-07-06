#!/usr/bin/python
# encoding:utf8
import json
from pyutil.data.easydict import EasyDict
from pyutil.data.session.common import create_session
from config import conf
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Column, Integer, BigInteger, SmallInteger, String,
    DateTime, Text, Date, DECIMAL, Float, Time, desc)

Base = declarative_base()


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
         

class Model(Base):
    __tablename__ = "model"
    
    id              = Column(Integer, primary_key=True)
    hardware        = Column(Integer)
    alg_framework   =  Column(Integer)
    net_type        = Column(Integer)
    data_type       = Column(Integer)
    business        = Column(Integer)
    purpose         = Column(String)
    data_input      = Column(String)
    input_size      = Column(String)
    version         = Column(String, default = '')
    scale           = Column(String)    
    is_publish      = Column(SmallInteger, default=0)
    status          = Column(SmallInteger, default=0)
    user_id         = Column(Integer)
    uri             = Column(String, default='')
    convert_from    = Column(Integer)
    create_time     = Column(String)
    upload_time     = Column(DateTime, default='0000-00-00 00:00:00')
    modify_time     = Column(DateTime, default='0000-00-00 00:00:00')
    note            = Column(String)

    @property
    def output_uri(self):
        return self._output_uri

    @output_uri.setter
    def output_uri(self, value):
        self._output_uri = value

    def __repr__(self):
        return "<Model: %s>" % (self.id)
        
    def info(self):
        return dict(
            id              = self.id,
            hardware        = self.hardware,
            alg_framework   = self.alg_framework,
            net_type        = self.net_type,
            data_type       = self.data_type,
            business        = self.business,
            purpose         = self.purpose,
            data_input      = self.data_input,
            input_size      = self.input_size,
            version         = self.version,
            scale           = self.scale, 
            is_publish      = self.is_publish,
            status          = self.status,
            user_id         = self.user_id,
            uri             = self.uri,
            convert_from    = self.convert_from,
            create_time     = str(self.create_time),
            upload_time     = str(self.upload_time),
            modify_time     = str(self.modify_time),
            note            = self.note
            )

