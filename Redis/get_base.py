#!/usr/bin/env python
# -*- coding: utf-8 -*-
from redis_cli import def_redis_cli
import random
import string

class GetRedisInfo(object):
    DEF_EXPIRE = 3600
    
    @property
    def key(self):
        return self.sid
        
    @property
    def value(self):
        return self.sdata
        
    def __init__(self, sid=None, **kw):
        self.sid = sid
        self.sdata  = kw
        self.backend = def_redis_cli
        if not self.sid:
            self.sid = self._gen_sid()    
        try:
            if self.backend.exists(self.key):
                self.sdata = self.backend.hgetall(self.key)
        except:
            return   
            
    def __getitem__(self, key):
        return self.sdata.get(key)

    def __setitem__(self, key, item):
        self.sdata[key] = item
            
    def _gen_sid(self):
        ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 10))
        if not self.backend.exists(self.key):
            return ran_str
        else:
            return _gen_sid(self)   
            
    def save(self):
        self.backend.hmset(self.key, self.sdata)
        if 0 > self.backend.ttl(self.key):
            self.backend.expire(self.key, self.DEF_EXPIRE)

if __name__ == '__main__':
    v = {'model_ids':[333]}
    t = GetRedisInfo(**v)
    print t.key
    print t.value
    t.save()
