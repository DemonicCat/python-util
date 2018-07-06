#!/usr/bin/python
# encoding:utf8

import json
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Column, Integer, BigInteger, SmallInteger, String,
    DateTime, Text)

from pyutil.data.easydict import EasyDict

Base = declarative_base()
GidBase = declarative_base()

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

class Label(Base, JsonDataMixin):
    
    __tablename__ = 'label'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    createtime = Column(DateTime)

    def __repr__(self):
        return '<Label: %s>' % self.name

class Image(Base):

    __tablename__ = 'image'

    id = Column(BigInteger, primary_key=True)
    name = Column(String)
    uri = Column(String)
    status = Column(SmallInteger, default=1)
    weather = Column(SmallInteger, default=0)
    time = Column(SmallInteger, default=0)
    position = Column(SmallInteger)
    project_id = Column(Integer)
    image_tag_id = Column(SmallInteger)
    create_time = Column(DateTime)
    modify_time = Column(DateTime)

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

    _position_map = {0: u"卡口", 1: u"电警"}
    @property
    def position_name(self):
        return self._position_map.get(self.position, u"未知code(%s)" % (self.position))

    def __repr__(self):
        return '<Image: %s>' % self.uri


class ImageTag(Base, JsonDataMixin):

    __tablename__ = 'image_tag'

    id = Column(SmallInteger, primary_key=True)
    name = Column(String)
    classifyid = Column(SmallInteger)
    classifyname = Column(String)
    data = Column(Text)
    create_time = Column(DateTime)

    def __repr__(self):
        return '<ImageTag: %s>' % self.name


class Project(Base):

    __tablename__ = 'project'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    time = Column(String)
    place = Column(String)
    tag = Column(String)
    create_time = Column('createtime', DateTime)
    modify_time = Column('modifytime', DateTime)

    def __repr__(self):
        return '<Project: %s>' % self.name


car_color_map = {
    1: u"黑色", 2: u"蓝色", 3: u"棕色", 4: u"绿色", 5: u"灰色", 6: u"白色",
    7: u"红色", 8: u"黄色", 9: u"粉色", 10: u"紫色", 0: u"其他"}

car_type_map = {
    1: u"靠边不完整", 2: u"有遮挡", 3: u"方向相反", 4: u"倾斜角度（较大）",
    0: u"正常"}

car_kind_map = {
    0: u"其他", 1: u"轿车", 2: u"越野车", 3: u"商务车", 4: u"小型货车",
    5: u"大型货车", 6: u"轻客",7: u"小型客车", 8: u"大型客车", 9: u"三轮车",
    10: u"微面", 11: u"皮卡车", 12: u"挂车", 13: u"混凝土搅拌车",14: u"罐车",
    15: u"随车吊", 16: u"消防车", 17: u"渣土车", 18: u"押运车", 19: u"工程抢修车",
    20: u"救援车", 21: u"栏板卡车"}

belt_map = {0: u"模糊，未确定", 1: u"系安全带", 2: u"未系安全带"}

phone_map = {0: u"模糊，未确定", 1: u"打电话", 2: u"未打电话"}

class SampCar(Base, JsonDataMixin):

    __tablename__ = 'samp_car'

    id = Column(BigInteger, primary_key=True)
    ref_id = Column(BigInteger)
    samp_id = Column(BigInteger)
    image_id = Column(BigInteger)
    position = Column(SmallInteger, default=0)
    carstyle_guid = Column(String, default='')
    kind_id = Column(SmallInteger, default=0)
    color = Column(SmallInteger)
    type = Column(SmallInteger)
    bbox = Column(String)
    face_bbox = Column(String, default='')
    wind_bbox = Column(String, default='')
    plate = Column(String)
    marker = Column(Text)
    data = Column(Text)
    modify_time = Column(DateTime)
    is_del = Column(SmallInteger)
    is_done = Column(SmallInteger)
    is_check = Column(SmallInteger)
    done_flag = Column(BigInteger)
    check_flag = Column(BigInteger)
    plate_id = Column(BigInteger)
    tollstation_id = Column(SmallInteger)

    _color_map = car_color_map
    @property
    def color_name(self):
        return self._color_map.get(self.color, u"未知code(%s)" % (self.color))

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
        return self.data_dict.beltflag

    _belt_map = belt_map
    @property
    def belt_name(self):
        return self._belt_map.get(self.belt_flag, u"未知code(%s)" % (self.belt_flag))

    @property
    def phone_flag(self):
        return self.data_dict.phoneflag

    _phone_map = phone_map
    @property
    def phone_name(self):
        return self._phone_map.get(self.phone_flag, u"未知code(%s)" % (self.phone_flag))

    @property
    def crash_flag(self):
        return self.data_dict.crashflag

    def __repr__(self):
        return '<SampCar: %s>' % self.id


plate_color_map = {
    0: u"其他", 1: u"黄色", 2: u"蓝色", 3: u"黑色", 4: u"白色", 5: u"绿色"}

plate_mode_map = {
    0: u"未知", 1: u"单层", 2: u"双层"}

plate_type_map = {
    1: u"大型汽车号牌", 2: u"小型汽车号牌", 3: u"使馆汽车号牌", 4: u"领馆汽车号牌",
    5: u"境外汽车号牌", 6: u"外籍汽车号牌", 7: u"两、三轮摩托车号牌",
    8: u"轻便摩托车号牌", 9: u"使馆摩托车号牌", 10: u"领馆摩托车号牌",
    11: u"境外摩托车号牌", 12: u"外籍摩托车号牌", 13: u"农用运输车号牌",
    14: u"拖拉机号牌", 15: u"挂车号牌", 16: u"教练汽车号牌", 17: u"教练摩托车号牌",
    18: u"试验汽车号牌", 19: u"试验摩托车号牌", 20: u"临时人境汽车号牌",
    21: u"临时人境摩托车号牌", 22: u"临时行驶车号牌", 23: u"警用汽车号牌",
    24: u"警用摩托号牌", 26: u"香港入出境车", 27: u"澳门入出境车", 31: u"武警号牌",
    32: u"军队号牌", 99: u"其他号牌"}

class SampPlate(Base, JsonDataMixin):

    __tablename__ = 'samp_plate'

    id = Column(BigInteger, primary_key=True)
    ref_id = Column(BigInteger)
    samp_id = Column(BigInteger)
    image_id = Column(BigInteger)
    word = Column(String)
    color = Column(String)
    mode = Column(SmallInteger)
    type = Column(SmallInteger)
    box = Column(String)
    create_time = Column(DateTime)
    modify_time = Column(DateTime)
    data = Column(Text)
    is_del = Column(SmallInteger)
    done_flag = Column(BigInteger)
    check_flag = Column(BigInteger)

    _color_map = plate_color_map
    @property
    def color_name(self):
        return self._color_map.get(self.color, u'未知code(%s)' % (self.color))

    _mode_map = plate_mode_map
    @property
    def mode_name(self):
        return self._mode_map.get(self.mode, u"未知code(%s)" % (self.mode))

    _type_map = plate_type_map
    @property
    def type_name(self):
        return self._type_map.get(self.type, u"未知code(%s)" % (self.type))

    def __repr__(self):
        return '<SampPlate: %s>' % self.id

class SampPerson(Base, JsonDataMixin):
    
    __tablename__ = 'samp_person'

    id = Column(BigInteger, primary_key=True)
    ref_id = Column(BigInteger)
    samp_id = Column(BigInteger)
    image_id = Column(BigInteger)
    bbox = Column(String)
    mistake = Column(SmallInteger)
    gender = Column(SmallInteger)
    age = Column(SmallInteger)
    orientation = Column(SmallInteger)
    hat = Column(SmallInteger)
    bag = Column(SmallInteger)
    knapsack = Column(SmallInteger)
    upper = Column(SmallInteger)
    bottom = Column(SmallInteger)
    create_time = Column(DateTime)
    modify_time = Column(DateTime)
    is_del = Column(SmallInteger)
    done_flag = Column(BigInteger)
    check_flag = Column(BigInteger)
    data = Column(Text)

    def __repr__(self):
        return '<SampPerson: %s>' % self.id

class SampImageRef(Base):

    __tablename__ = 'samp_image_ref'

    id = Column(BigInteger, primary_key=True)
    samp_id = Column(BigInteger)
    image_id = Column(BigInteger)
    modify_time = Column(DateTime)
    is_del = Column(SmallInteger, default=0)
    is_done = Column(SmallInteger, default=0)
    is_check = Column(SmallInteger, default=0)

    def __repr__(self):
        return '<TaskImageRef: %s>' % self.id


class SampInfo(Base, JsonDataMixin):

    __tablename__ = 'samp_info'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    usage = Column(SmallInteger)
    function = Column(SmallInteger)
    phase = Column(BigInteger)
    create_time = Column(DateTime)
    data = Column(Text)

    _function_map = {0: u'其他', 1: u'测试集', 2: u'训练集'}

    @property
    def function_name(self):
        return self._function_map.get(self.function, u'未知code(%s)' % (self.function))

    _phase_map = {
        0x0000001: u'车头/车尾',    0x0000002: u'品牌型号',
        0x0000004: u'车辆类型',     0x0000008: u'车辆颜色',
        0x0000010: u'号牌号码',     0x0000020: u'号牌类型',
        0x0000040: u'号牌颜色',     0x0000080: u'号牌单双层',
        0x0000100: u'安全带',       0x0000200: u'打电话',
        0x0000400: u'车辆状态',     0x0000800: u'车身位置',
        0x0001000: u'车脸位置',     0x0002000: u'车窗位置',
        0x0004000: u'车牌位置',     0x0008000: u'标识物',
        0x0010000: u'危化品',       0x0020000: u'自行车',
        0x0040000: u'二轮车',       0x0080000: u'行人',
        0x0100000: u'收费站类型',   0x0200000: u'人车分离'}

    @property
    def phase_list(self):
        li = filter(lambda x:x[0] & self.phase == x[0], self._phase_map.items())
        return [ l[1] for l in li ]

    def __repr__(self):
        return '<SampTask: %s>' % self.name


class Samp(Base, JsonDataMixin):

    __tablename__ = 'samp'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    usage = Column(SmallInteger)
    function = Column(SmallInteger)
    phase = Column(BigInteger)
    data = Column(Text)
    create_time = Column(DateTime)
    modify_time = Column(DateTime)

    @property
    def ref_ids(self):
        return self.data_dict.ref_ids

    @property
    def car_ids(self):
        return self.data_dict.car_ids

    @property
    def samp_ids(self):
        return self.data_dict.samp_ids

    def __repr__(self):
        return '<Samp: %s>' % self.name


class SampLog(Base):

    __tablename__ = 'samp_log'

    id = Column(BigInteger, primary_key=True)
    create_time = Column(DateTime)
    add_ids = Column(Text)
    del_ids = Column(Text)

    def __repr__(self):
        return '<SampLog: %s>' % self.create_time


class TestInfo(Base, JsonDataMixin):

    __tablename__ = 'test_info'

    id = Column(BigInteger, primary_key=True)
    name = Column(String)
    create_time = Column(DateTime)
    data = Column(Text)
    function = Column(SmallInteger)
    status = Column(SmallInteger)
    schedule = Column(Text)
    statistics = Column(Text)
    describe = Column(String)

    @property
    def alg_api(self):
        return self.data_dict.get('alg_api', None)

    @property
    def calc_param(self):
        return self.data_dict.calc_param

    @property
    def threshold(self):
        return self.data_dict.threshold

    @property
    def test_samp_ids(self):
        return self.data_dict.test_samp_ids

    @property
    def test_type(self):
        return self.data_dict.get('test_type', 'common')

    @property
    def process(self):
        schedule = json.loads(self.schedule)
        return round(float(schedule['completed'])/schedule['total'], 2)

    @property
    def time_len(self):
        schedule = json.loads(self.schedule)
        return schedule['time_len']

    _status_map = {
        -1: u'等待', 1: u'正在执行', 2: u'暂停', 3: u'已取消', 4: u'已完成'}

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
        return '<TestInfo: %s>' % self.name


class TestResult(Base, JsonDataMixin):

    __tablename__ = 'test_result'

    id = Column(BigInteger, primary_key=True)
    test_id = Column(BigInteger)
    test_samp_id = Column(BigInteger)
    ref_id = Column(BigInteger)
    data = Column(Text)
    create_time = Column(DateTime)

    @property
    def result(self):
        return self.data_dict.result

    def __repr__(self):
        return '<TestResult: %s>' % self.id


class TestCar(Base, JsonDataMixin):

    __tablename__ = 'test_car'

    id = Column(BigInteger, primary_key=True)
    test_id = Column(BigInteger)
    ref_id = Column(BigInteger)
    test_samp_id = Column(BigInteger)
    position = Column(SmallInteger, default=0)
    carstyle_guid = Column(String, default='')
    kind_id = Column(SmallInteger, default=0)
    color = Column(String)
    type = Column(SmallInteger)
    bbox = Column(String)
    face_bbox = Column(String, default='')
    wind_bbox = Column(String, default='')
    plate_id = Column(BigInteger)
    marker = Column(Text)
    data = Column(Text)
    create_time = Column(DateTime)

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
        return self.data_dict.get('beltflag', None)

    _belt_map = belt_map
    @property
    def belt_name(self):
        return self._belt_map.get(self.belt_flag, u"未知code(%s)" % (self.belt_flag))

    @property
    def phone_flag(self):
        return self.data_dict.get('phoneflag', None)

    _phone_map = phone_map
    @property
    def phone_name(self):
        return self._phone_map.get(self.phone_flag, u"未知code(%s)" % (self.phone_flag))

    @property
    def crash_flag(self):
        return self.data_dict.get('crashflag', None)

    def __repr__(self):
        return '<TestCar: %s>' % self.id


class TestPlate(Base, JsonDataMixin):

    __tablename__ = 'test_plate'

    id = Column(BigInteger, primary_key=True)
    test_id = Column(BigInteger)
    ref_id = Column(BigInteger)
    test_samp_id = Column(BigInteger)
    image_id = Column(BigInteger)
    word = Column(String)
    color = Column(SmallInteger)
    mode = Column(SmallInteger)
    type = Column(SmallInteger)
    box = Column(String)
    create_time = Column(DateTime)
    data = Column(Text)

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

    id = Column(BigInteger, primary_key=True)
    url = Column(String)
    status = Column(SmallInteger)
    data = Column(Text)
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

