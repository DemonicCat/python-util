#! /usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, BigInteger, SmallInteger, String,\
                        DateTime, Text, Date, DECIMAL, Float, Time, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()

# 定义User对象:
class User(Base):
    # 表的名字:
    __tablename__ = 'users'

    # 表的结构:
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=True)

# 初始化数据库连接:
engine = create_engine('mysql+mysqlconnector://root:root@192.168.1.13:3306/test')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

session = DBSession()
ed_user = User(name='ed')
session.add(ed_user)
session.commit()

#查询
for instance in session.query(User).order_by(User.id):
    print instance.name,instance.id
    
session.close()
