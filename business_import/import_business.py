import sys
import os
import json
import pyhdb
import pyhdb.exceptions
from pyhdb.protocol.lobs import NClob

if len(sys.argv) != 2:
    print 'Usage: python import_business.py <path>'
    print '\t path: path to texts file'
    exit()

filepath = sys.argv[1]


with open("../secrets.json") as f:
    secrets = json.load(f)

connection = pyhdb.connect(
    host=secrets['host'],
    port=secrets['port'],
    user=secrets['username'],
    password=secrets['password']
)

cursor = connection.cursor()




with open(filepath) as f:
    for i, line in enumerate(f):
        print i
        try:
            sql_to_prepare = 'CALL LTN_DEVELOP.add_document (?, ?, ?)'
            params = {
                'DOCUMENT_ID': 'MAZ_{n:06d}'.format(n=i),
                'DOCUMENT_TEXT': NClob(line.replace("'", "''")),
                'TASK': 2
            }
            psid = cursor.prepare(sql_to_prepare)
            ps = cursor.get_prepared_statement(psid)
            cursor.execute_prepared(ps, [params])
        except Exception, e:
            print 'Error: ', e
        connection.commit()






