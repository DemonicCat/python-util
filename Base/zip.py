
import zipfile
from io import BytesIO

file_list = ['E:\\code\\test.py', 'E:\\code\\2\\2.jpg']

memory_file = BytesIO()
with zipfile.ZipFile(memory_file, "w", zipfile.ZIP_DEFLATED) as zf:
    for _file in file_list:
        with open( _file, 'rb') as fp:
            file_name = _file.split('/')[-1]
            zf.writestr(file_name, fp.read())
memory_file.seek(0)

with open('E:\\code\\12.zip', 'wb') as f:
    f.write(memory_file.getvalue())
