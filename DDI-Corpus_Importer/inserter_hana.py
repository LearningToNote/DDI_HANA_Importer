# this assumes a schema db called LEARNING_TO_NOTE is created
# use db_setup/hana.sql

import json
import math

import pyhdb
import pyhdb.exceptions
from pyhdb.protocol.lobs import NClob

CHUNK_SIZE = 1000

with open("../secrets.json") as f:
    secrets = json.load(f)

connection = pyhdb.connect(
    host=secrets['host'],
    port=secrets['port'],
    user=secrets['username'],
    password=secrets['password']
)

cursor = connection.cursor()


def insert_many(statement, values):
    if len(values) > 0:
        number_of_chunks = int(math.ceil(len(values)/float(CHUNK_SIZE)))

        try:
            for i in range(number_of_chunks):
                cursor.executemany(
                    statement,
                    values[i*CHUNK_SIZE:i*CHUNK_SIZE+CHUNK_SIZE])

        except pyhdb.exceptions.DatabaseError as e:
            print e


def store_user(id, name, token, description, image):
    cursor.execute("INSERT INTO LEARNING_TO_NOTE.USERS VALUES(?,?,?,?,?)", (id, name, token, description, image))
    connection.commit()


def insert_types(types):
    insert_many("INSERT INTO LEARNING_TO_NOTE.TYPES VALUES (?,?,?,?,?)", types)
    connection.commit()


def create_task(username):
    task = 1
    try:
        sql_to_prepare = 'CALL LEARNING_TO_NOTE.add_task (?, ?, ?, ?, ?)'
        params = {
            'TASK_NAME': 'Biomedical Domain (Drug-Drug-Interactions)',
            'TABLE_NAME': 'BIO_TEXTS',
            'ER_ANALYSIS_CONFIG': 'LTN::ltn_analysis',
            'AUTHOR': username,
            'TASK_ID': None
        }
        psid = cursor.prepare(sql_to_prepare)
        ps = cursor.get_prepared_statement(psid)
        cursor.execute_prepared(ps, [params])
        task = cursor.fetchone()[0][0]
    except Exception, e:
        print 'Warning: ', e
    return task


def store(documents, user_documents, entities, pairs, offsets, task):
    for document in documents:
        try:
            sql_to_prepare = 'CALL LEARNING_TO_NOTE.add_document (?, ?, ?)'
            params = {
                'DOCUMENT_ID': document[0],
                'DOCUMENT_TEXT': NClob(document[1].replace("'", "''")),
                'TASK': task
            }
            psid = cursor.prepare(sql_to_prepare)
            ps = cursor.get_prepared_statement(psid)
            cursor.execute_prepared(ps, [params])
        except Exception, e:
            print 'Error: ', e
    insert_many("INSERT INTO LEARNING_TO_NOTE.USER_DOCUMENTS VALUES (?,?,?,?,?,?)", user_documents)
    insert_many("INSERT INTO LEARNING_TO_NOTE.ENTITIES VALUES (?,?,?,?,?)", entities)
    insert_many("INSERT INTO LEARNING_TO_NOTE.PAIRS VALUES (?,?,?,?,?,?)", pairs)
    insert_many("INSERT INTO LEARNING_TO_NOTE.OFFSETS VALUES (?,?,?,?)", offsets)
    connection.commit()
