#! /usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, BigInteger, SmallInteger, String,\
                        DateTime, Text, Date, DECIMAL, Float, Time, create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
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
Session = sessionmaker(bind=engine)

'''
用scoped_session的目的主要是为了线程安全。
scoped_session类似单例模式，当我们调用使用的时候，会先在Registry里找找之前是否已经创建session了。
要是有，就把这个session返回。
要是没有，就创建新的session，注册到Registry中以便下次返回给调用者。
这样就实现了这样一个目的：在同一个线程中，call scoped_session 的时候，返回的是同一个对象
'''
#session_factory = sessionmaker(bind=some_engine)
#Session = scoped_session(session_factory)

session = Session()
ed_user = User(name='ed')
session.add(ed_user)
session.commit()

#查询
for instance in session.query(User).order_by(User.id):
    print instance.name,instance.id
    
session.close()
