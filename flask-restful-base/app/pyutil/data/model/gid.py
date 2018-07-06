from sqlalchemy import (Column, Integer, BigInteger, Text,
        Date, DateTime, SmallInteger, String, Numeric, orm, event)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
GidBase = declarative_base()

class SeqTable(GidBase):
    __tablename__ = 'seq_table'
    name = Column(String, primary_key=True)
    gid = Column(BigInteger)
