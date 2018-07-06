#!/usr/bin/python
# encoding:utf8

import json
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Column, Integer, BigInteger, SmallInteger, String, DateTime, Text, Date)
from pyutil.data.easydict import EasyDict

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
                separators=(',', ':'))
        if hasattr(self, '_data_dict'):
            del self._data_dict

class CarStyle(Base, JsonDataMixin):

    __tablename__ = 'carstyle_alg'

    gid = Column(String, primary_key=True)
    position = Column(SmallInteger)
    brand_id = Column(SmallInteger)
    brand_name = Column(String)
    series_id = Column(SmallInteger)
    series_name = Column(String)
    spec_id = Column(SmallInteger)
    spec_name = Column(String)
    kind_id = Column(SmallInteger)
    extra_name = Column(String)
    ref_name = Column(String)
    create_time = Column(DateTime)
    modify_time = Column(DateTime)
    status = Column(SmallInteger)
    modify_gid = Column(String)
    tollstation_id = Column(SmallInteger)
    country = Column(String)
    manufacturer = Column(Text)
    data = Column(Text)

    @property
    def name(self):
        _name = '-'.join([self.brand_name, self.series_name,
                self.spec_name, self.extra_name])
        return _name.strip('-')

    @property
    def pic_path(self):
        return self.data_dict.get('PicPath', [])

    @property
    def tollstation_basic(self):
        return self.data_dict.get('Tollstationbasic', {})

class CarKind(Base):

    __tablename__ = 'carkind'

    SF_CarKindCode = Column(SmallInteger, primary_key=True)
    SF_CarKindName = Column(String)
    GB_CarKindCode = Column(SmallInteger)
    GB_CarKindName = Column(String)
    DisplayKindName = Column(String)
    ClassifyCode = Column(SmallInteger)
    ClassifyName = Column(String)
    TollgateKindName = Column(String)


class CarColor(Base):
    
    __tablename__ = 'carcolor'

    SF_CarColorCode = Column(SmallInteger, primary_key=True)
    SF_CarColorName = Column(String)
    GB_CarColorCode = Column(SmallInteger)
    GB_CarColorName = Column(String)
    DisplayColorName = Column(String)


class CarBrand(Base, JsonDataMixin):

    __tablename__ = 'carbrand'

    Id = Column(Integer, primary_key=True)
    Name = Column(String)
    CreateTime = Column(DateTime)
    ModifyTime = Column(DateTime)
    data = Column('Data', Text)


class CarPlate(Base):
    
    __tablename__ = 'carplate'

    PlateType = Column(SmallInteger, primary_key=True)
    TypeName = Column(String)
    BackgroundColor = Column(String)
    TextColor = Column(String)
