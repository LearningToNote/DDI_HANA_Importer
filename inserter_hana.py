# this assumes a schema db called LEARNING_TO_NOTE is created
# use db_setup/hana.sql

import pyhdb
import pyhdb.exceptions
import json
import math

CHUNK_SIZE = 1000

#Load credentials
with open("secrets.json") as f:
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

def store(documents, name_to_entity, doc_entities, pairs):
    insert_many("INSERT INTO LEARNING_TO_NOTE.DOCUMENTS VALUES (?,?)", documents)
    insert_many("INSERT INTO LEARNING_TO_NOTE.ENTITIES VALUES(?,?,?)", name_to_entity)
    insert_many("INSERT INTO LEARNING_TO_NOTE.DOC_ENTITIES VALUES(?,?,?,?,?)", doc_entities)
    insert_many("INSERT INTO LEARNING_TO_NOTE.PAIRS VALUES (?,?,?,?)", pairs)
    connection.commit()
