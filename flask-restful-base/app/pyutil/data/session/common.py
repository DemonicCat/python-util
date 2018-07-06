from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import create_engine

UserWriteSession = scoped_session(sessionmaker())
UserReadSession = scoped_session(sessionmaker())
GidSession = scoped_session(sessionmaker())

def _create_engine(user, password, host, port, db, autocommit=False):
    engine = create_engine('mysql://%s:%s@%s:%s/%s?charset=utf8&&use_unicode=1' % (
            user, password,
            host, port,
            db),
            pool_size = 10,
            max_overflow = -1,
            pool_recycle = 7200,
            connect_args = {'connect_timeout': 1, 'autocommit': 1 if autocommit else 0}
        )
    return engine

def config_gid_session(conf):
    engine = _create_engine(conf.user, conf.password,
        conf.host, int(conf.port),
        conf.db_name)
    GidSession.configure(bind=engine, autocommit=False, autoflush=False, expire_on_commit=False)

def config_user_read_session(conf):
    engine = _create_engine(conf.user, conf.password,
        conf.host, int(conf.port),
        conf.db_name)
    UserReadSession.configure(bind=engine, autocommit=True, autoflush=False, expire_on_commit=False)

def config_user_write_session(conf):
    engine = _create_engine(conf.user, conf.password,
        conf.host, int(conf.port),
        conf.db_name)
    UserWriteSession.configure(bind=engine, autocommit=False, autoflush=False, expire_on_commit=False)

def create_session(conf, write=True):
    engine = _create_engine(conf.user, conf.password,
        conf.host, int(conf.port),
        conf.db_name)
    Session = scoped_session(sessionmaker())
    Session.configure(bind=engine, autocommit=(not write), autoflush=False, expire_on_commit=False)
    return Session

