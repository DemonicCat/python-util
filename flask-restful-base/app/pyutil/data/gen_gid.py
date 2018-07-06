import logging
from sqlalchemy import func
from model.gid import SeqTable
from session.common import GidSession

def _insert_seq(name, init_val=1):
    seq_model = SeqTable()
    seq_model.name = name
    seq_model.gid = init_val
    ws = GidSession()
    try:
        ws.add(seq_model)
        ws.commit()
        return 0
    except Exception as err:
        logging.exception(err)        
        return -1;
    finally:
        ws.close()

def gen_id(name):
    ws = GidSession()
    # get cur max id
    seq_model = ws.query(SeqTable).filter(SeqTable.name == name).all()
    if not seq_model:
        # insert it
        if 0 != _insert_seq(name):
            return None
        return gen_id(name)

    seq_model = seq_model[0]
    gid = seq_model.gid + 1;
    seq_model.gid = gid
    sql = "update seq_table set gid=%s where name='%s' and gid<%s" % (gid, name, gid)
    try:
        res = ws.execute(sql)
        ws.commit()
        if res.rowcount > 0:
            return gid
        return gen_id(name)
    except Exception as err:
        return gen_id(name)
    finally:
        ws.close()

def config_def_gid_session():
    from easydict import EasyDict
    from session.common import config_gid_session
    def_conf = EasyDict(dict(
        host='192.168.1.222',
        port=3306,
        user='ssro',
        password='nrm2015',
        db_name='gid_db',
    ))
    config_gid_session(def_conf)

if __name__ == '__main__':
    config_def_gid_session()
    print gen_id('__test')
