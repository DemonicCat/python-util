from sqlalchemy import desc
from sqlalchemy import asc


record = session.query(Model).get(id)

records = session.query(Model.id, Model.uri)\
                   .filter(Model.status == 0)\
                   .all()

query.filter(User.name == 'ed') #equals
query.filter(User.name != 'ed') #not equals
query.filter(User.name.like('%ed%')) #LIKE
uery.filter(User.name.in_(['ed','wendy', 'jack'])) #IN
query.filter(User.name.in_(session.query(User.name).filter(User.name.like('%ed%'))#IN
query.filter(~User.name.in_(['ed','wendy', 'jack']))#not IN
query.filter(User.name == None)#is None
query.filter(User.name != None)#not None
from sqlalchemy import and_
query.filter(and_(User.name =='ed',User.fullname =='Ed Jones')) # and
query.filter(User.name == 'ed',User.fullname =='Ed Jones') # and
query.filter(User.name == 'ed').filter(User.fullname == 'Ed Jones')# and
from sqlalchemy import or_
query.filter(or_(User.name =='ed', User.name =='wendy')) #or
query.filter(User.name.match('wendy')) #match  

#只查询第二条和第三条数据                          
for u in session.query(User).order_by(User.id)[1:3]:

bus_class_id = rs.query(Business)\
                    .filter(Business.id == bus_id)\
                    .first()\
                    .class_id
                           
def get(self):
    rs = ReadSession()
    filter_params = dict(request.args.items())
    page_index = 1
    page_size = 10
    records = rs.query(Model).filter(Model.status == 0)

    for k, v in filter_params.items():
        if k == 'current':
            page_index = int(filter_params['current']) 
        elif k == 'pageSize':
            page_size =  int(filter_params['pageSize']) 
        elif k in ['purpose', 'data_input', 'version', 'scale', 'input_size']:
            #模糊搜索
            records = records.filter(getattr(Model, k).like("%{x}%".format(x=v.encode('utf8'))))
            #sqlite 不用format
            #records = records.filter(getattr(Model, k).like("%"+v+"%"))
        elif k == 'model_output':           
            output_list = rs.query(ModelOutput.model_id)\
                        .filter(ModelOutput.status == 0)\
                        .filter(ModelOutput.uri.like("%{x}%".format(x=v.encode('utf8'))))\
                        .all()
            model_ids = [l[0] for l in output_list]
            #范围搜索
            records = records.filter(Model.id.in_(set(model_ids)))
        else:
            records = records.filter(getattr(Model, k)==v)
            
    records_num = records.count() #计数
    records = records.order_by(desc(Model.create_time)) #排序
    records = records.slice((page_index - 1) * page_size, page_index * page_size) #偏移分页
    
    
def sql_query():
    session = Session()
    #查询
    q_ids = session.execute('select id from users \
                        where  age = 30 \
                        and sex = 1 \
                        and phone > 18502541423')
    #import pdb;pdb.set_trace()
    ids = [str(q[0]) for q in q_ids.fetchall()]
    print tuple(ids)
    q_cs = session.execute('select country from users \
                    where  id in (' + ','.join(tuple(ids)) + ')')
    print q_cs.fetchone() #获取单条数据
    print q_cs.fetchall() #接收全部的返回结果行
    print q_cs.rowcount #这是一个只读属性，并返回执行execute()方法后影响的行数
   

