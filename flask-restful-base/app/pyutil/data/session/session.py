import uuid
from redis_cli import def_redis_cli

UID_SESSION_KEY = '_uid'
class TransportError(Exception):
    def __init__(self, *args):
        self.args = args

class SessionSecurityError(Exception):
    def __init__(self, *args):
        self.args = args

class Session(object):
    DEF_EXPIRE = 7 * 86400

    def _key(self, sid):
        return '%s|%s' % (self.ns, sid)

    @property
    def key(self):
        return self._key(self.sid)

    def __init__(self, sid=None, namespace=None, backend=None):
        self.ns = namespace or 'ws'
        self.sid = sid
        self.sdata = {}
        self.modified = False
        self.exists = False
        self.backend = backend or def_redis_cli
        if not self.sid:
            self.sid = self._gen_sid()
            return
        try:
            if not self.backend.exists(self.key):
                raise SessionSecurityError()
            self.sdata = self.backend.hgetall(self.key)
            self.exists = True
        except:
            return

    def __getitem__(self, key):
        return self.sdata.get(key)

    def __setitem__(self, key, item):
        self.modified = True
        self.sdata[key] = item

    def _gen_sid(self):
        sid = uuid.uuid1().hex
        if not self.backend.exists(self._key(sid)):
            return sid
        else:
            return _gen_sid(self)

    @property
    def token(self):
        return self.sid

    @property
    def session_key(self):
        return self.sid

    def save(self):
        if not self.modified:
            return
        self.backend.hmset(self.key, self.sdata)
        if 0 > self.backend.ttl(self.key):
            self.backend.expire(self.key, self.DEF_EXPIRE)
        self.exists = True

    def keys(self):
        return self.sdata.keys()

    def get_expiry_age(self):
        return self.backend.ttl(self.key)

    def set_expiry(self, age):
        return self.backend.expire(self.key, age)

    def remove(self):
        if not self.exists:
            return
        self.backend.delete(self.key)

if __name__ == '__main__':
    ss = Session('616c263c4f3c11e89661f8bc124d9ad8')
    print ss['_uid']
    print ss.key
    ss.save()
    ss.set_expiry(86400)
