from sqlalchemy import desc
from sqlalchemy import asc


record = session.query(Model).get(id)

records = session.query(Model.id, Model.uri)\
                   .filter(Model.status == 0)\
                   .all()
                   
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
