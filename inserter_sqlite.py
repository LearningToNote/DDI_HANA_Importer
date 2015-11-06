# this assumes a db called testdb is created
# use db_setup/sqlite.sql
# cat db_setup/sqlite.sql | sqlite3 testdb

import sqlite3
import math

CHUNK_SIZE = 1000
connection = sqlite3.connect('testdb')
cursor = connection.cursor()

def insert_many(statement, values):
    if len(values) > 0:
        number_of_chunks = int(math.ceil(len(values)/float(CHUNK_SIZE)))

        for i in range(number_of_chunks):
            cursor.executemany(
                statement,
                values[i*CHUNK_SIZE:i*CHUNK_SIZE+CHUNK_SIZE])

def store(documents, entities, pairs, offsets):
    insert_many("INSERT INTO LEARNING_TO_NOTE.DOCUMENTS VALUES(?,?)", documents)
    insert_many("INSERT INTO LEARNING_TO_NOTE.ENTITIES VALUES(?,?,?)", entities)
    insert_many("INSERT INTO LEARNING_TO_NOTE.PAIRS VALUES(NULL,?,?,?,?)", pairs)
    insert_many("INSERT INTO LEARNING_TO_NOTE.OFFSETS VALUES(?,?,?)", offsets)
    connection.commit()
