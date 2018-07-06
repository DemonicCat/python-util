#!/usr/bin/python
# encoding:utf8

import os
import zlib
import json
import base64
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Column, Integer, BigInteger, SmallInteger, String,
    DateTime, Text, Date, DECIMAL, Float)
from pyutil.data.model.const import *
from pyutil.data.easydict import EasyDict
from pyutil.data.model.const import *

Base = declarative_base()
GidBase = declarative_base()

brand_map = {}

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


class SeqTable(GidBase):
    __tablename__ = 'seq_table'

    name = Column(String, primary_key=True)
    gid = Column(BigInteger)

    def __repr__(self):
        return '<SeqTable: %s>' % self.name

function_map = {
    1 << 0: u'车头/车尾',    1 << 1: u'品牌型号',
    1 << 2: u'车辆类型',     1 << 3: u'车辆颜色',
    1 << 4: u'号牌号码',     1 << 5: u'号牌类型',
    1 << 6: u'号牌颜色',     1 << 7: u'号牌单双层',
    1 << 8: u'安全带',       1 << 9: u'打电话',
    1 << 10: u'车辆状态',    1 << 11: u'车身位置',
    1 << 12: u'车脸位置',    1 << 13: u'车窗位置',
    1 << 14: u'车牌位置',    1 << 15: u'标识物',
    1 << 16: u'危化品',      1 << 17: u'自行车',
    1 << 18: u'二轮车',      1 << 19: u'行人',
    1 << 20: u'收费站类型',  1 << 21: u'人车分离',
    1 << 22: u'误检',        1 << 23: u'性别',
    1 << 24: u'年龄',        1 << 25: u'帽子',
    1 << 26: u'手提包',      1 << 27: u'背包',
    1 << 28: u'上衣颜色',    1 << 29: u'下衣颜色',
    1 << 30: u'朝向',        1 << 31: u'撞损',
    1 << 32: u'口罩',        1 << 33: u'眼镜',
    1 << 34: u'胡子',        1 << 35: u'围巾',
    1 << 36: u'打伞',        1 << 37: u'乘客身体未知',
    1 << 38: u'乘客面部未知',1 << 39: u'发型',
    1 << 40: u'上衣类型',    1 << 41: u'下衣类型',
    1 << 42: u'耳机',        1 << 43: u'鞋子颜色',
    1 << 44: u'帽子颜色',    1 << 45: u'手套',
    1 << 46: u'手机',        1 << 47: u'抱小孩'
}



class Project(Base):

    __tablename__ = 'project'

    id          = Column(Integer, primary_key=True)
    name        = Column(String)
    time        = Column(String)
    place       = Column(String)
    is_del      = Column(SmallInteger)
    create_time = Column(DateTime)
    modify_time = Column(DateTime)

    def __repr__(self):
        return '<Project: %s>' % self.name

    def add_model(self, data):
        self.name = data['name']
        self.time = data.get('time', '')
        self.place = data.get('place', '')
        self.is_del = data.get('is_del', 0)

    def get_info(self):
        return dict(
                id=self.id, 
                name=self.name, 
                time=self.time,
                place=self.place, 
                is_del=self.is_del,
                create_time=unicode(self.create_time),
                modify_time=unicode(self.modify_time))


class Image(Base):

    __tablename__ = 'image'

    id          = Column(BigInteger, primary_key=True)
    name        = Column(String)
    uri         = Column(String)
    status      = Column(SmallInteger, default=1)
    weather     = Column(SmallInteger, default=0)
    time        = Column(SmallInteger, default=0)
    md5         = Column(String)
    position    = Column(SmallInteger)
    project_id  = Column(Integer)
    create_time = Column(DateTime)
    modify_time = Column(DateTime)

    _path_prefix = '/mnt/mfs/image_store/basicimage'
    @property
    def path(self):
        return os.path.join(self._path_prefix, self.uri)

    _status_map = {1: u"在用", 0: u"弃用"}
    @property
    def status_name(self):
        return self._status_map.get(self.status, u"未知code(%s)" % (self.status))

    _weather_map = {0: u"未知",1: u"晴天",2: u"阴天",3: u"雾天",4: u"雨天",5: u"雪天"}
    @property
    def weather_name(self):
        return self._weather_map.get(self.weather, u"未知code(%s)" % (self.weather))

    _time_map = {0: u"未知",1: u"白天",2: u"黑夜"}
    @property
    def time_name(self):
        return self._time_map.get(self.time, u"未知code(%s)" % (self.time))

    @property
    def position_name(self):
        return position_map.get(self.position, u"未知code(%s)" % (self.position))

    def __repr__(self):
        return '<Image: %s>' % self.uri

    def add_model(self, data):
        self.name = data['name']
        self.uri = data['uri']
        self.status = data.get('status', 1)
        self.weather = data.get('weather', 0)
        self.md5 = data.get('md5', '')
        self.time = data.get('time', 0)
        self.position = data['position']
        self.project_id = data.get('project_id', 0)

    def get_info(self):
        return dict(
                id=self.id, 
                name=self.name, 
                path=self.path,
                status=self.status, 
                status_name=self.status_name,
                weather=self.weather, 
                weather_name=self.weather_name, 
                position=self.position, 
                position_name=self.position_name, 
                project_id=self.project_id, 
                uri=self.uri, 
                time=self.time, 
                time_name=self.time_name)


class SampTask(Base, JsonDataMixin):
    __tablename__ = 'samp_task'

    id          = Column(Integer, primary_key=True)
    name        = Column(String)
    usage       = Column(SmallInteger)
    function    = Column(BigInteger)
    label_function = Column(BigInteger)
    phase       = Column(SmallInteger)
    is_del      = Column(SmallInteger)
    create_time = Column(DateTime)
    modify_time = Column(DateTime)
    data        = Column(Text)

    _phase_map = {0: u'其他', 1: u'测试集', 2: u'训练集'}

    @property
    def phase_name(self):
        return self._phase_map.get(self.phase, u'未知code(%s)' % (self.function))

    _function_map = function_map

    @property
    def function_list(self):
        li = filter(lambda x:x[0] & self.function == x[0], self._function_map.items())
        return [ l[1] for l in li ]

    @property
    def desc(self):
        return self.data_dict.get('desc', '')

    @desc.setter
    def desc(self, _desc):
        self.data_dict.desc = _desc

    def __repr__(self):
        return '<SampTask: %s>' % self.id

    def add_model(self, data):
        self.name = data['name']
        self.usage = data.get('usage', 0)
        self.function = data.get('function', 0)
        self.phase = data.get('phase', 0)
        self.is_del = data.get('is_del', 0)
        self.label_function = data.get('label_function', 0)
        self.data_dict.desc = data.get('desc', '')
        self.save_data_dict()

    def get_info(self):
        return dict(
                id=self.id, 
                name=self.name,
                phase=self.phase, 
                phase_name=self.phase_name,
                function=self.function, 
                function_list=self.function_list,
                label_function=self.label_function,
                create_time=unicode(self.create_time), 
                desc=self.desc,
                modify_time=unicode(self.modify_time))

class TaskImageRef(Base):

    __tablename__ = 'task_image_ref'

    id          = Column(BigInteger, primary_key=True)
    task_id     = Column(BigInteger)
    image_id    = Column(BigInteger)
    create_time = Column(DateTime)
    modify_time = Column(DateTime)
    is_del      = Column(SmallInteger, default=0)
    done_flag   = Column(BigInteger)
    check_flag  = Column(BigInteger)

    def __repr__(self):
        return '<TaskImageRef: %s>' % self.id

    def add_model(self, data):
        self.task_id = data['task_id']
        self.image_id = data['image_id']
        self.is_del = data.get('is_del', 0)
        self.done_flag = data.get('done_flag', 0)
        self.check_flag = data.get('check_flag', 0)

    def get_info(self):
        return dict(
                id=self.id,
                task_id=self.task_id,
                image_id=self.image_id,
                create_time=unicode(self.create_time),
                modify_time=unicode(self.modify_time),
                is_del=self.is_del, 
                done_flag=self.done_flag, 
                check_flag=self.check_flag)

    def save_data_dict(self):
        pass

class SampCar(Base, JsonDataMixin):

    __tablename__ = 'samp_car'

    id              = Column(BigInteger, primary_key=True)
    ref_id          = Column(BigInteger)
    task_id         = Column(BigInteger)
    image_id        = Column(BigInteger)
    position        = Column(SmallInteger, default=0)
    kind_id         = Column(SmallInteger, default=0)
    carstyle_guid   = Column(String, default='')
    separation_type = Column(SmallInteger, default=0)
    color           = Column(SmallInteger)
    type            = Column(SmallInteger)
    bbox            = Column(String)
    face_bbox       = Column(String, default='')
    wind_bbox       = Column(String, default='')
    marker          = Column(Text)
    data            = Column(Text)
    plate_id        = Column(BigInteger)
    create_time     = Column(DateTime)
    modify_time     = Column(DateTime)
    is_del          = Column(SmallInteger)
    done_flag       = Column(BigInteger)
    check_flag      = Column(BigInteger)
    tollstation_id  = Column(SmallInteger)

    _ext_box = []

    @property
    def type_name(self):
        return car_type_map.get(self.type, u"未知code(%s)" % (self.type))

    @property
    def position_name(self):
        return position_map.get(self.position, u"未知code(%s)" % (self.position))

    @property
    def color_name(self):
        return car_color_map.get(self.color, u"未知code(%s)" % (self.color))

    @property
    def kind_name(self):
        return car_kind_map.get(self.kind_id, u"未知code(%s)" % (self.kind_id))
    
    @property
    def guid(self):
        return self.data_dict.get('guid', 0)

    @guid.setter
    def guid(self, _guid):
        self.data_dict.guid = _guid

    @property
    def clarity_flag(self):
        return self.data_dict.get('clarity_flag', 0)

    @clarity_flag.setter
    def clarity_flag(self, _clarity_flag):
        self.data_dict.clarity_flag = _clarity_flag

    @property
    def passenger_ids(self):
        return self.data_dict.get('passenger_ids', [])

    @property
    def crash_flag(self):
        return self.data_dict.get('crash_flag', 0)

    @crash_flag.setter
    def crash_flag(self, _crash_flag):
        self.data_dict.crash_flag = _crash_flag

    @property
    def crash_name(self):
        return crash_map.get(self.crash_flag, u"未知code(%s)" % (self.crash_flag))

    @property
    def tollstation_name(self):
        return tollstation_map.get(self.crash_flag, u"未知code(%s)" % (self.crash_flag))

    @property
    def separation_name(self):
        return separation_map.get(self.separation_type, \
            u"未知code(%s)" % (self.separation_type))

    def __repr__(self):
        return '<SampCar: %s>' % self.id

    def add_model(self, data):
        self.ref_id = data['ref_id']
        self.task_id = data['task_id']
        self.image_id = data['image_id']
        self.position = data['position']
        self.bbox = data['bbox']
        self.carstyle_guid = data.get('carstyle_guid', '')
        self.face_bbox = data.get('face_bbox', '')
        self.wind_bbox = data.get('wind_bbox', '')
        self.marker = json.dumps(data.get('marker', '{}'))
        self.kind_id = data.get('kind_id', 0)
        self.plate_id = data.get('plate_id', 0)
        self.type = data.get('type', 0)
        self.tollstation_id = data.get('tollstation_id', 0)
        self.separation_type = data.get('separation_type', 0)
        self.data_dict.crash_flag = data.get('crash_flag', 0)
        self.data_dict.guid = data.get('guid', 0)
        self.data_dict.clarity_flag = data.get('clarity_flag', 0)
        self.color = data.get('color', 0)
        self.done_flag = data.get('done_flag', 0)
        self.check_flag = data.get('check_flag', 0)
        self.is_del = data.get('is_del', 0)
        self.data_dict.passenger_ids = data.get("passenger_ids", [])
        self.save_data_dict()

    def get_info(self):
        return dict(
                id=self.id, 
                ref_id=self.ref_id, 
                task_id=self.task_id,
                image_id=self.image_id, 
                carstyle_guid=self.carstyle_guid,
                bbox=self.bbox, 
                face_bbox=self.face_bbox,
                marker=json.loads(self.marker), 
                wind_bbox=self.wind_bbox,
                create_time=unicode(self.create_time),
                modify_time=unicode(self.modify_time), 
                done_flag=self.done_flag,
                check_flag=self.check_flag, 
                plate_id=self.plate_id,
                separation_type=self.separation_type, 
                is_del=self.is_del,
                position=self.position,
                kind_id=self.kind_id, 
                type=self.type, 
                type_name=self.type_name,
                tollstation_id=self.tollstation_id, 
                crash_flag=self.crash_flag,
                color=self.color, 
                guid=self.guid, 
                clarity_flag=self.clarity_flag, 
                position_name = self.position_name,
                kind_name = self.kind_name,
                separation_name = self.separation_name,
                tollstation_name = self.tollstation_name,
                brand_name = brand_map.get(self.carstyle_guid, u'未知(%s)' % self.carstyle_guid),
                color_name = self.color_name
        ) 


class SampPlate(Base, JsonDataMixin):

    __tablename__ = 'samp_plate'

    id          = Column(BigInteger, primary_key=True)
    ref_id      = Column(BigInteger)
    task_id     = Column(BigInteger)
    image_id    = Column(BigInteger)
    car_id      = Column(BigInteger)
    word        = Column(String)
    color       = Column(String)
    mode        = Column(SmallInteger)
    type        = Column(SmallInteger)
    box         = Column(String)
    create_time = Column(DateTime)
    modify_time = Column(DateTime)
    data        = Column(Text)
    is_del      = Column(SmallInteger)
    done_flag   = Column(BigInteger)
    check_flag  = Column(BigInteger)

    @property
    def color_name(self):
        return plate_color_map.get(self.color, u'未知code(%s)' % (self.color))

    @property
    def mode_name(self):
        return plate_mode_map.get(self.mode, u"未知code(%s)" % (self.mode))

    @property
    def type_name(self):
        return plate_type_map.get(self.type, u"未知code(%s)" % (self.type))

    def __repr__(self):
        return '<SampPlate: %s>' % self.id

    def add_model(self, data):
        self.ref_id = data['ref_id']
        self.task_id = data['task_id']
        self.image_id = data['image_id']
        self.car_id = data.get('car_id', 0)
        self.box = data['box']
        self.word = data.get('word', '')
        self.color = data.get('color', 0)
        self.mode = data.get('mode', 0)
        self.type = data.get('type', 0)
        self.data = data.get('data', '')
        self.done_flag = data.get('done_flag', 0)
        self.check_flag = data.get('check_flag', 0)
        self.is_del = data.get('is_del', 0)
        self.save_data_dict()

    def get_info(self):
        return dict(
                id=self.id, 
                ref_id=self.ref_id, 
                task_id=self.task_id,
                image_id=self.image_id, 
                word=self.word, 
                box=self.box,
                color=self.color, 
                mode=self.mode, 
                type=self.type,
                car_id=self.car_id,
                data=json.loads(self.data),
                done_flag=self.done_flag, 
                check_flag=self.check_flag,
                create_time=unicode(self.create_time),
                modify_time=unicode(self.modify_time),
                color_name=self.color_name,
                mode_name=self.mode_name,
                type_name=self.type_name)


class SampPassenger(Base, JsonDataMixin):

    __tablename__ = 'samp_passenger'

    id              = Column(BigInteger, primary_key=True)
    ref_id          = Column(BigInteger)
    task_id         = Column(Integer)
    image_id        = Column(BigInteger)
    car_id          = Column(BigInteger)
    belt_flag       = Column(SmallInteger)
    phone_flag      = Column(SmallInteger)
    body_box        = Column(String)
    upper_body_box  = Column(String)
    lower_body_box  = Column(String)
    face_box        = Column(String)
    phone_box       = Column(String)
    belt_box        = Column(String)
    is_driver       = Column(SmallInteger)
    is_del          = Column(SmallInteger)
    done_flag       = Column(BigInteger)
    check_flag      = Column(BigInteger)
    data            = Column(Text)
    create_time     = Column(DateTime)
    modify_time     = Column(DateTime)

    def __repr__(self):
        return '<SampPassenger: %s>' % self.id

    def add_model(self, data):
        self.ref_id = data['ref_id']
        self.task_id = data['task_id']
        self.image_id = data['image_id']
        self.car_id = data.get('car_id', 0)
        self.belt_flag = data.get('belt_flag', 0)
        self.phone_flag = data.get('phone_flag', 0)
        self.body_box = data.get('body_box', '0,0,0,0')
        self.upper_body_box = data.get('upper_body_box', '0,0,0,0')
        self.lower_body_box = data.get('lower_body_box', '0,0,0,0')
        self.face_box = data.get('face_box', '0,0,0,0')
        self.belt_box = data.get('belt_box', '0,0,0,0')
        self.phone_box = data.get('phone_box', '0,0,0,0')
        self.is_driver = data.get('is_driver', 0)
        self.is_del = data.get('is_del', 0)
        self.done_flag = data.get('done_flag', 0)
        self.check_flag = data.get('check_flag', 0)
        self.save_data_dict()

    def get_info(self):
        return dict(
                id = self.id,
                task_id=self.task_id,
                ref_id=self.ref_id,
                image_id=self.image_id,
                car_id=self.car_id,
                belt_flag = self.belt_flag,
                phone_flag = self.phone_flag,
                body_box = self.body_box,
                upper_body_box = self.upper_body_box, 
                lower_body_box = self.lower_body_box,
                face_box = self.face_box,
                belt_box = self.belt_box,
                phone_box = self.phone_box,
                done_flag = self.done_flag,
                check_flag = self.check_flag,
                is_driver = self.is_driver)


class SampPerson(Base, JsonDataMixin):
    
    __tablename__ = 'samp_person'

    id              = Column(BigInteger, primary_key=True)
    ref_id          = Column(BigInteger)
    task_id         = Column(BigInteger)
    image_id        = Column(BigInteger)
    bbox            = Column(String)
    mistake         = Column(SmallInteger)
    gender          = Column(SmallInteger)
    age             = Column(SmallInteger)
    orientation     = Column(SmallInteger)
    hat             = Column(SmallInteger)
    bag             = Column(SmallInteger)
    knapsack        = Column(SmallInteger)
    upper_color     = Column(SmallInteger)
    bottom_color    = Column(SmallInteger)
    mask            = Column(SmallInteger)
    glasses         = Column(SmallInteger)
    beard           = Column(SmallInteger)
    scarf           = Column(SmallInteger)
    umbrella        = Column(SmallInteger)
    hair            = Column(SmallInteger)
    upper_type      = Column(SmallInteger)
    bottom_type     = Column(SmallInteger)
    headset         = Column(SmallInteger)
    shoes_color     = Column(SmallInteger)
    hat_color       = Column(SmallInteger)
    gloves          = Column(SmallInteger)
    mobile_phone    = Column(SmallInteger)
    baby            = Column(SmallInteger)
    create_time     = Column(DateTime)
    modify_time     = Column(DateTime)
    is_del          = Column(SmallInteger)
    done_flag       = Column(BigInteger)
    check_flag      = Column(BigInteger)
    data            = Column(Text)

    _ext_box = ['trunk_box', 'bag_box']

    @property
    def mistake_name(self):
        return mistake_map.get(self.mistake, u"未知code(%s)" % self.mistake)

    @property
    def gender_name(self):
        return gender_map.get(self.gender, u"未知code(%s)" % self.gender)

    @property
    def age_name(self):
        return age_map.get(self.age, u"未知code(%s)" % self.age)

    @property
    def orientation_name(self):
        return orientation_map.get(self.orientation, u"未知code(%s)" % self.orientation)

    @property
    def hat_name(self):
        return hat_map.get(self.hat, u"未知code(%s)" % self.hat)

    @property
    def bag_name(self):
        return bag_map.get(self.bag, u"未知code(%s)" % self.bag)

    @property
    def knapsack_name(self):
        return knapsack_map.get(self.knapsack, u"未知code(%s)" % self.knapsack)

    @property
    def guid(self):
        return self.data_dict.get('guid', 0)

    @guid.setter
    def guid(self, _guid):
        self.data_dict.guid = _guid

    @property
    def clarity_flag(self):
        return self.data_dict.get('clarity_flag', 0)

    @clarity_flag.setter
    def clarity_flag(self, _clarity_flag):
        self.data_dict.clarity_flag = _clarity_flag

    @property
    def face_box(self):
        return self.data_dict.get('face_box', '0,0,0,0')

    @face_box.setter
    def face_box(self, _face_box):
        self.data_dict.face_box = _face_box

    @property
    def head_box(self):
        return self.data_dict.get('head_box', '0,0,0,0')

    @head_box.setter
    def head_box(self, _head_box):
        self.data_dict.head_box = _head_box

    def __repr__(self):
        return '<SampPerson: %s>' % self.id

    def add_model(self, data):
        self.ref_id = data['ref_id']
        self.task_id = data['task_id']
        self.image_id = data['image_id']
        self.bbox = data['bbox']
        self.mistake = data.get('mistake', 1)
        self.gender = data.get('gender', 0)
        self.age = data.get('age', 0)
        self.orientation = data.get('orientation', 0)
        self.hat = data.get('hat', 0)
        self.bag = data.get('bag', 0)
        self.knapsack = data.get('knapsack', 0)
        self.upper_color = data.get('upper', 0)
        self.bottom_color = data.get('bottom', 0)
        self.mask = data.get('mask', 0)
        self.glasses = data.get('glasses', 0)
        self.beard = data.get('beard', 0)
        self.scarf = data.get('scarf', 0)
        self.umbrella = data.get('umbrella', 0)
        self.hair = data.get('hair', 0)
        self.upper_type = data.get('upper_type', 0)
        self.bottom_type = data.get('bottom_type', 0)
        self.headset = data.get('headset', 0)
        self.shoes_color = data.get('shoes_color', 0)
        self.hat_color = data.get('hat_color', 0)
        self.gloves = data.get('gloves', 0)
        self.mobile_phone = data.get('mobile_phone', 0)
        self.baby = data.get('baby', 0)
        self.is_del = data.get('is_del', 0)
        self.done_flag = data.get('done_flag', 0)
        self.check_flag = data.get('check_flag', 0)
        self.data_dict.guid = data.get('guid', 0)
        self.data_dict.clarity_flag = data.get('clarity_flag', 0)
        self.data_dict.face_box = data.get('face_box', '0,0,0,0')
        self.data_dict.head_box = data.get('head_box', '0,0,0,0')
        self.save_data_dict()

    def get_info(self):
        return dict(
                id=self.id,
                ref_id=self.ref_id,
                task_id=self.task_id,
                image_id=self.image_id,
                mistake=self.mistake,
                mistake_name=self.mistake_name,
                gender=self.gender, 
                gender_name=self.gender_name,
                age=self.age, 
                age_name=self.age_name,
                orientation=self.orientation,
                orientation_name=self.orientation_name,
                hat=self.hat, 
                hat_name=self.hat_name,
                bag=self.bag, 
                bag_name=self.bag_name,
                knapsack=self.knapsack, 
                knapsack_name=self.knapsack_name,
                upper_color=self.upper_color, 
                bottom_color=self.bottom_color,
                mask=self.mask, 
                glasses=self.glasses, 
                beard=self.beard,
                scarf=self.scarf,
                umbrella=self.umbrella,
                bbox=self.bbox,
                hair=self.hair,
                upper_type=self.upper_type,
                bottom_type=self.bottom_type,
                headset=self.headset,
                shoes_color=self.shoes_color, 
                hat_color=self.hat_color,
                gloves=self.gloves, 
                mobile_phone=self.mobile_phone,
                baby=self.baby, 
                done_flag=self.done_flag,
                check_flag=self.check_flag,
                guid=self.guid,
                face_box=self.face_box,
                head_box=self.head_box,
                clarity_flag=self.clarity_flag)


class Label(Base, JsonDataMixin):
    
    __tablename__ = 'label'

    id          = Column(Integer, primary_key=True)
    name        = Column(String)
    target      = Column(String)
    create_time = Column(DateTime)
    data        = Column(Text)
    function    = Column(String)
    function_id = Column(Integer)

    def __repr__(self):
        return '<Label: %s>' % self.name

    def get_info(self):
        return dict(
                id=self.id,
                name=self.name, 
                target=self.target, 
                create_time=unicode(self.create_time),
                function=self.function,
                function_id=self.function_id)


class LabelRef(Base, JsonDataMixin):
    
    __tablename__ = 'label_ref'

    id          = Column(BigInteger, primary_key=True)
    label_id    = Column(Integer)
    ele_id      = Column(BigInteger)
    element     = Column(SmallInteger)
    create_time = Column(DateTime)
    modify_time = Column(DateTime)
    data        = Column(Text)
    is_del      = Column(SmallInteger)

    def __repr__(self):
        return '<LabelRef: %s>' % self.id

    def get_info(self):
        return dict(
                id=self.id, 
                label_id=self.label_id,
                ele_id=self.ele_id,
                element=self.element)

class MarkerLabelRef(Base, JsonDataMixin):
    
    __tablename__ = 'marker_label_ref'

    id = Column(BigInteger, primary_key=True)
    label_id = Column(Integer)
    task_id = Column(Integer)
    function_id = Column(Integer)
    ele_id = Column(BigInteger)
    element = Column(SmallInteger)
    create_time = Column(DateTime)
    modify_time = Column(DateTime)
    data = Column(Text)
    is_del = Column(SmallInteger)
    is_done = Column(SmallInteger)
    is_check = Column(SmallInteger)

    def __repr__(self):
        return '<LabelRef: %s>' % self.id

    def get_info(self):
        return dict(
                id=self.id,
                label_id=self.label_id,
                function_id=self.function_id,
                ele_id=self.ele_id, 
                element=self.element,
                task_id=self.task_id,
                is_done=self.is_done, 
                is_check=self.is_check)


class Samp(Base, JsonDataMixin):

    __tablename__ = 'samp'

    id          = Column(Integer, primary_key=True)
    name        = Column(String)
    function    = Column(BigInteger)
    label_function = Column(BigInteger)
    phase       = Column(BigInteger)
    target      = Column(String)
    data        = Column(Text)
    create_time = Column(DateTime)
    modify_time = Column(DateTime)

    @property
    def desc(self):
        return self.data_dict.get('desc', '')

    @desc.setter
    def desc(self, _desc):
        self.data_dict.desc = _desc

    def __repr__(self):
        return '<Samp: %s>' % self.name

    def get_info(self):
        return dict(
                id=self.id, 
                name=self.name, 
                function=self.function,
                label_function=self.label_function, 
                target=self.target,
                phase=self.phase, 
                create_time=unicode(self.create_time),
                modify_time=unicode(self.modify_time), 
                desc=self.desc)


class SampSlice(Base, JsonDataMixin):
    
    __tablename__ = 'samp_slice'

    id          = Column(BigInteger, primary_key=True)
    samp_id     = Column(Integer)
    samp_name   = Column(String)
    slice_date  = Column(Date)
    function    = Column(SmallInteger)
    phase       = Column(BigInteger)
    create_time = Column(DateTime)
    data        = Column(Text)

    @property
    def samp_data(self):
        return zlib.decompress(base64.b64decode(self.data_dict.samp_data))

    @samp_data.setter
    def samp_data(self, _samp):
        self.data_dict.samp_data = base64.b64encode(zlib.compress(_samp))

    def __repr__(self):
        return '<SampSlice: %s>' % self.id


class SampRef(Base, JsonDataMixin):

    __tablename__ = 'samp_ref'

    id          = Column(BigInteger, primary_key=True)
    samp_id     = Column(Integer)
    ele_id      = Column(BigInteger)
    element     = Column(String)
    create_time = Column(DateTime)
    modify_time = Column(DateTime)
    is_del      = Column(SmallInteger)
    data        = Column(Text)

    def __repr__(self):
        return '<SampRef: %s>' % self.id

    def get_info(self):
        return dict(
                id=self.id, 
                samp_id=self.samp_id,
                ele_id=self.ele_id, 
                element=self.element)

class SampLog(Base, JsonDataMixin):

    __tablename__ = 'samp_log'

    id          = Column(BigInteger, primary_key=True)
    samp_id     = Column(BigInteger)
    operation   = Column(String)
    element     = Column(String)
    ele_ids     = Column(Text)
    create_time = Column(DateTime)
    data        = Column(Text)

    def __repr__(self):
        return '<SampLog: %s>' % self.create_time


class TestInfo(Base, JsonDataMixin):

    __tablename__ = 'test_info'

    id          = Column(BigInteger, primary_key=True)
    name        = Column(String)
    user_id     = Column(BigInteger)
    group_id    = Column(BigInteger)
    create_time = Column(DateTime)
    function    = Column(SmallInteger)
    alg_api     = Column(String)
    type        = Column(String)
    status      = Column(SmallInteger)
    schedule    = Column(Text)
    describe    = Column(String)
    data        = Column(Text)

    @property
    def calc_param(self):
        return self.data_dict.calc_param

    @property
    def test_samp_ids(self):
        return self.data_dict.test_samp_ids

    @property
    def thresholds(self):
        return self.data_dict.thresholds if 'thresholds' in self.data_dict.keys()\
                else [self.data_dict.threshold]

    @property
    def processor(self):
        return self.data_dict.processor

    @property
    def process(self):
        schedule = json.loads(self.schedule)
        return round(float(schedule.get('completed', 0))/schedule['total'], 2)

    @property
    def time_len(self):
        schedule = json.loads(self.schedule)
        return schedule.get('time_len', 0)

    _status_map = {
        -1: u'等待', 1: u'正在执行', 2: u'暂停', 3: u'已取消', 4: u'已完成', 9: u'异常退出'}

    @property
    def status_name(self):
        return self._status_map.get(self.status, u"未知code(%s)" % (self.status))

    _func_map = {
        'Detect': 1, 'BrandRec': 2, 'ColorRec': 4, 'MarkerRec': 8, 'PlateRec': 16,
        'TypeRec': 32}

    @property
    def targets(self):
        calc_param = json.loads(self.calc_param)
        result = ['Detect']
        for k, v in calc_param['Recognize'].items():
            if v['IsRec']:
                result.append(k)
        return result

    def __repr__(self):
        return '<TestInfo: %s>' % self.id


class TestGroup(Base, JsonDataMixin):

    __tablename__ = 'test_group'

    id              = Column(Integer, primary_key=True)
    name            = Column(String)
    describe        = Column(String)
    is_pf_test      = Column(SmallInteger)
    function        = Column(BigInteger)
    create_user_id  = Column(Integer)
    create_time     = Column(DateTime)
    data            = Column(Text)

    def __repr__(self):
        return '<TestGroup: %s>' % name


class TestImageResult(Base, JsonDataMixin):

    __tablename__ = 'test_image_result'

    id              = Column(BigInteger, primary_key=True)
    test_id         = Column(BigInteger)
    test_samp_id    = Column(BigInteger)
    ref_id          = Column(BigInteger)
    threshold       = Column(DECIMAL)
    data            = Column(Text)
    create_time     = Column(DateTime)
    is_del          = Column(SmallInteger)

    @property
    def result(self):
        return self.data_dict.result

    @property
    def counts(self):
        return self.data_dict.counts

    def __repr__(self):
        return '<TestImageResult: %s>' % self.id

class TestResult(Base, JsonDataMixin):

    __tablename__ = 'test_result'

    id          = Column(BigInteger, primary_key=True)
    test_id     = Column(BigInteger)
    test_samp_id    = Column(BigInteger)
    threshold       = Column(DECIMAL)
    data            = Column(Text)
    create_time     = Column(DateTime)
    is_del          = Column(SmallInteger)

    @property
    def result(self):
        return self.data_dict.result

    def __repr__(self):
        return '<TestResult: %s>' % (self.id)


class TestCar(Base, JsonDataMixin):

    __tablename__ = 'test_car'

    id              = Column(BigInteger, primary_key=True)
    test_id         = Column(BigInteger)
    ref_id          = Column(BigInteger)
    test_samp_id    = Column(BigInteger)
    position        = Column(SmallInteger, default=0)
    kind_id         = Column(SmallInteger, default=0)
    carstyle_guid   = Column(String, default='')
    separation_type = Column(SmallInteger)
    color           = Column(String)
    type            = Column(SmallInteger)
    bbox            = Column(String)
    face_bbox       = Column(String, default='')
    wind_bbox       = Column(String, default='')
    marker          = Column(Text)
    data            = Column(Text)
    plate_id        = Column(BigInteger)
    create_time     = Column(DateTime)
    tollstation_id  = Column(SmallInteger)
    is_del          = Column(SmallInteger)

    _color_map = car_color_map
    @property
    def color_name(self):
        return self._color_map.get(int(self.color), u"未知code(%s)" % (self.color))

    _type_map = car_type_map
    @property
    def type_name(self):
        return self._type_map.get(self.type, u"未知code(%s)" % (self.type))

    _kind_map = car_kind_map
    @property
    def kind_name(self):
        return self._kind_map.get(self.kind_id, u"未知code(%s)" % (self.kind_id))

    @property
    def belt_flag(self):
        return self.data_dict.get('belt_flag', 0)

    _belt_map = belt_map
    @property
    def belt_name(self):
        return self._belt_map.get(self.belt_flag, u"未知code(%s)" % (self.belt_flag))

    @property
    def phone_flag(self):
        return self.data_dict.get('phone_flag', 0)

    _phone_map = phone_map
    @property
    def phone_name(self):
        return self._phone_map.get(self.phone_flag, u"未知code(%s)" % (self.phone_flag))

    @property
    def crash_flag(self):
        return self.data_dict.get('crash_flag', 0)

    @property
    def danger_flag(self):
        return self.data_dict.get('danger_flag', 0)

    def __repr__(self):
        return '<TestCar: %s>' % self.id


class TestPlate(Base, JsonDataMixin):

    __tablename__ = 'test_plate'

    id              = Column(BigInteger, primary_key=True)
    test_id         = Column(BigInteger)
    ref_id          = Column(BigInteger)
    test_samp_id    = Column(BigInteger)
    word            = Column(String)
    color           = Column(SmallInteger)
    mode            = Column(SmallInteger)
    type            = Column(SmallInteger)
    box             = Column(String)
    create_time     = Column(DateTime)
    data            = Column(Text)
    is_del          = Column(SmallInteger)

    _color_map = plate_color_map
    @property
    def color_name(self):
        return self._color_map.get(self.color, u'未知code(%s)' % (self.color))

    _mode_map = plate_mode_map
    @property
    def mode_name(self):
        return self._mode_map.get(self.mode, u'未知code(%s)' % (self.mode)) 

    _type_map = plate_type_map
    @property
    def type_name(self):
        return self._type_map.get(self.type, u'未知code(%s)' % (self.type))

    @property
    def det_score(self):
        return self.data_dict.get('det_score', None)

    def __repr__(self):
        return '<TestPlate: %s>' % self.id


class AlgApi(Base, JsonDataMixin):

    __tablename__ = 'alg_api'

    id          = Column(BigInteger, primary_key=True)
    url         = Column(String)
    describe    = Column(String)
    status      = Column(SmallInteger)
    data        = Column(Text)
    create_time = Column(DateTime)

    @property
    def sdk_version(self):
        return self.data_dict.get('sdk_version', None)

    _status_map = {0: u'弃用', 1: u'在用', 10: u'默认使用'}
    @property
    def status_name(self):
        return self._status_map.get(self.status, u'未知code(%s)' % (self.status))

    def __repr__(self):
        return '<AlgAPI: %s>' % self.id


class TaskPlan(Base, JsonDataMixin):
    
    __tablename__ = 'task_plan'

    id              = Column(Integer, primary_key=True)
    task_id         = Column(BigInteger)
    plan_flag       = Column(BigInteger)
    label_plan_flag = Column(BigInteger)
    status          = Column(SmallInteger)
    weight          = Column(SmallInteger)
    batch           = Column(SmallInteger)
    leader          = Column(SmallInteger)
    mark_users      = Column(Text)
    mark_deadline   = Column(Date)
    check_users     = Column(Text)
    check_deadline  = Column(Date)
    data            = Column(Text)
    create_time     = Column(DateTime)
    modify_time     = Column(DateTime)

    @property
    def users(self):
        return {
            1: json.loads(self.mark_users),
            2: json.loads(self.check_users)
        }

    status_map = {
        0: u'已关闭',
        1: u'正在标注',
        2: u'正在复查',
        3: u'任务暂停'
    }

    @property
    def status_name(self):
        return self.status_map.get(self.status,
                u'未知code(%s)' % self.status)

    plan_map = function_map

    @property
    def plan_list(self):
        li = filter(lambda x:x[0] & self.plan_flag == x[0],
                self.plan_map.items())
        return [ l[1] for l in li ]
    
    @property
    def day_work(self):
        return self.data_dict.get('day_work', 0)

    @day_work.setter
    def day_work(self, _day_work):
        self.data_dict.day_work = _day_work

    @property
    def check_day_work(self):
        return self.data_dict.get('check_day_work', 0)

    @check_day_work.setter
    def check_day_work(self, _check_day_work):
        self.data_dict.check_day_work = _check_day_work

    def __repr__(self):
        return '<TaskPlan: %s>' % self.id

class TrackTestInfo(Base, JsonDataMixin):

    __tablename__ = 'track_test_info'

    id          = Column(BigInteger, primary_key=True)
    name        = Column(String)
    describe    = Column(String)
    status      = Column(SmallInteger)
    user_id     = Column(Integer)
    group_id    = Column(Integer)
    schedule    = Column(Text)
    create_time = Column(DateTime)
    data        = Column(Text)

    _status_map = {
        -1: u'结果未上传', 1: u'正在测试', 2: u'正在测试', 3: u'已取消', 4: u'已完成', 9: u'异常'}

    @property
    def status_name(self):
        return self._status_map.get(self.status, u"未知code(%s)" % (self.status))

    @property
    def test_samp_ids(self):
        return self.data_dict.test_samp_ids

    @property
    def attachment(self):
        return self.data_dict.get('attachment', '')

class TrackTestResult(Base, JsonDataMixin):
    
    __tablename__ = 'track_test_result'

    id          = Column(BigInteger, primary_key=True)
    test_id     = Column(BigInteger)
    test_samp_id= Column(BigInteger)
    create_time = Column(DateTime)
    data        = Column(Text)
    is_del      = Column(SmallInteger)

    @property
    def result(self):
        return self.data_dict.result

    def __repr__(self):
        return '<TrackTestResult: %s>' % (self.id)


class TrackTestObject(Base):
    
    __tablename__ = 'track_test_object'

    id          = Column(BigInteger, primary_key=True)
    test_id     = Column(BigInteger)
    test_samp_id= Column(BigInteger)
    ref_id      = Column(BigInteger)
    image_id    = Column(BigInteger)
    alg_guid    = Column(Integer)
    box         = Column(String)
    type        = Column(SmallInteger)
    score       = Column(SmallInteger)
    is_pcb      = Column(SmallInteger)
    is_del      = Column(SmallInteger, default=0)
    create_time = Column(DateTime)

    _type_map = separation_map
    @property
    def type_name(self):
        return self._type_map.get(self.type, u'未知code(%s)' % self.type)


class TrackTestObjectResult(Base):

    __tablename__ = 'track_test_object_result'

    id          = Column(BigInteger, primary_key=True)
    test_id     = Column(BigInteger)
    test_samp_id= Column(BigInteger)
    alg_guid    = Column(Integer, default=-1)
    label_guid  = Column(String, default='')
    is_lost     = Column(String, default=0)
    is_mistake  = Column(String, default=0)
    is_filter   = Column(SmallInteger, default=0)
    is_match_pcb= Column(SmallInteger, default=0)
    is_match_seq= Column(SmallInteger, default=0)
    avg_iou     = Column(Float, default=0)
    succ_rate   = Column(Float, default=0)
    is_del      = Column(SmallInteger, default=0)
    create_time = Column(DateTime)

class Log(Base):
    __tablename__ = 'log'

    id          = Column(BigInteger, primary_key=True)
    user_id     = Column(Integer)
    plan_id     = Column(Integer)
    ref_id      = Column(BigInteger)
    data_type   = Column(String)
    data_id     = Column(BigInteger)
    change_log  = Column(Text)
    operation   = Column(String)
    log_time    = Column(DateTime)
    
class LogArchive(Base):
    __tablename__ = 'log_archive'

    id = Column(BigInteger, primary_key=True)
    date = Column(Date)
    type = Column(String)
    data = Column(Text)
    modify_time = Column(DateTime)


class SampBox(Base, JsonDataMixin):

    __tablename__ = 'samp_box'

    id              = Column(BigInteger, primary_key=True)
    ref_id          = Column(BigInteger)
    image_id        = Column(BigInteger)
    task_id         = Column(BigInteger)
    box             = Column(String)
    type            = Column(SmallInteger)
    object_id       = Column(BigInteger)
    object_type     = Column(String)
    guid            = Column(String)
    data            = Column(String)
    create_time     = Column(DateTime)
    modify_time     = Column(DateTime)
    is_del          = Column(SmallInteger)
    is_done         = Column(SmallInteger)
    is_check        = Column(SmallInteger)

    def __repr__(self):
        return '<SampBox: %s>' % self.id

    @classmethod
    def rect2array(self, rect_str):
        x, y, w, h = map(int, rect_str.split(','))
        return json.dumps([(x, y), (x+w, y), (x+w, y+h), (x, y+h)])

    @classmethod
    def array2rect(self, array_str):
        array = json.loads(array_str)
        x, y = array[0]; w = array[2][0] - x; h = array[2][1] - y
        return ','.join(map(str, [x, y , w, h]))

    def add_model(self, data):
        self.ref_id     = data['ref_id']
        self.task_id    = data['task_id']
        self.image_id   = data['image_id']
        self.box        = data['box']
        self.type       = data['type']
        self.object_id  = data.get('object_id', 0)
        self.object_type= data.get('object_type', 0)
        self.guid       = data.get('guid', '')
        self.is_del     = data.get('is_del', 0)
        self.is_done    = data.get('is_done', 0)
        self.is_check   = data.get('is_check', 0)

        self.save_data_dict()

    def get_info(self):
        return dict(
            id          = self.id,
            ref_id      = self.ref_id,
            task_id     = self.task_id,
            image_id    = self.image_id,
            box         = self.array2rect(self.box),
            type        = self.type,
            object_id   = self.object_id,
            object_type = self.object_type,
            guid        = self.guid
        )


class VersionUpdateLog(Base, JsonDataMixin):
    __tablename__ = "version_update_log"

    id = Column(Integer, primary_key = True)
    program = Column(String)
    version = Column(String)
    update_time = Column(DateTime)
    log = Column(Text)
    data = Column(Text)

    def add_model(self, data):
        self.program = data["program"]
        self.version = data["version"]
        self.log = data.get("log", "")
        self.data = json.dumps(data.get("data", []))

    def get_info(self):
        return dict(
                id = self.id,
                program = self.program,
                version = self.version,
                update_time=unicode(self.update_time),
                log = self.log,
                data = json.loads(self.data))

class Function(Base, JsonDataMixin):
    __tablename__ = 'function'

    id      = Column(Integer, primary_key=True)
    name    = Column(String)
    is_exclusion = Column(Integer)
    is_old  = Column(Integer)
    target  = Column(String)
    num_bit = Column(Integer)
    num_bit_group = Column(Integer)
    field   = Column(String)
    data    = Column(Text)
    
    table_map = dict(samp_car=SampCar, samp_plate=SampPlate,\
            samp_passenger=SampPassenger, samp_person=SampPerson,
            samp_box=SampBox)

    _ext_box = []
    
    @property
    def table(self):
        return self.table_map.get(self.target, SampCar)

    @property
    def field_name(self):
        return getattr(self.table, self.field)

    @property
    def func_num(self):
        return 1 << self.num_bit

    @property
    def exception(self):
        return self.data_dict.get('exception', {})

    @property
    def contain(self):
        return self.data_dict.get('contain', {})

    def get_info(self):
        return dict(
                id=self.id,
                name= self.name,
                is_exclusion=self.is_exclusion,
                is_old=self.is_old,
                target=self.target,
                num_bit=self.num_bit,
                field=self.field,
                func_num=self.func_num,
                contain=self.contain,
                exception=self.exception,
               num_bit_group=self.num_bit_group)

