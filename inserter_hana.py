# this assumes a schema db called LEARNING_TO_NOTE is created
# use db_setup/hana.sql

import json
import math

import pyhdb
import pyhdb.exceptions

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

def store_user(id, name, token):
    cursor.execute("INSERT INTO LEARNING_TO_NOTE.USERS VALUES(?,?,?)", (id, name, token))
    connection.commit()

def store(documents, user_documents, entities, pairs, offsets):
    insert_many("INSERT INTO LEARNING_TO_NOTE.DOCUMENTS VALUES(?,?)", documents)
    insert_many("INSERT INTO LEARNING_TO_NOTE.USER_DOCUMENTS VALUES(?,?,?,?,?,?)", user_documents)
    insert_many("INSERT INTO LEARNING_TO_NOTE.ENTITIES VALUES(?,?,?)", entities)
    insert_many("INSERT INTO LEARNING_TO_NOTE.PAIRS VALUES(?,?,?,?)", pairs)
    insert_many("INSERT INTO LEARNING_TO_NOTE.OFFSETS VALUES(?,?,?)", offsets)
    connection.commit()
