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

def store(documents, name_to_entity, doc_entities, pairs):
    insert_many("INSERT INTO DOCUMENTS VALUES (?,?)", documents)
    insert_many("INSERT INTO ENTITIES VALUES(?,?,?)", name_to_entity)
    insert_many("INSERT INTO DOC_ENTITIES VALUES(NULL,?,?,?,?,?)", doc_entities)
    insert_many("INSERT INTO PAIRS VALUES (NULL,?,?,?,?)", pairs)
    connection.commit()
