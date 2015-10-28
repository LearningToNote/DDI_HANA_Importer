import xml.etree.ElementTree as ET
import pyhdb
import pyhdb.exceptions
import os
import yaml
import math


CHUNK_SIZE = 1000
filepath = os.getcwd()+"/APIforDDICorpus/DDICorpus/Train/DrugBank/"
files = []

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

def insert_content(filename):
    documents = []
    sentences = []
    entities = []
    pairs = []
    offsets = []

    tree = ET.parse(filename)
    root = tree.getroot()
    for document in root.iter('document'):
        doc_id = document.get('id')
        documents.append( (doc_id,) )
        for sentence in document.findall('sentence'):
            sentence_id = sentence.get('id')
            sentence_text = sentence.get('text')
            sentences.append((sentence_id, sentence_text, doc_id))
            for entity in sentence.findall('entity'):
                entity_id = entity.get('id')
                entity_offsets = entity.get('charOffset').split(';', 1)

                for offset in entity_offsets:
                    offset_start, offset_end = offset.split('-')
                    offset_start = int(offset_start)
                    offset_end = int(offset_end)
                    offsets.append((offset_start, offset_end, entity_id))

                entity_type = entity.get('type')
                entity_text = entity.get('text')
                entities.append((
                    entity_id,
                    entity_type,
                    entity_text,
                    sentence_id))

            for pair in sentence.findall('pair'):
                pair_id = pair.get('id')
                pair_e1 = pair.get('e1')
                pair_e2 = pair.get('e2')
                pair_ddi = 1 if pair.get('ddi') == "true" else 0
                pair_type = pair.get('type')
                pairs.append((pair_id, pair_e1, pair_e2, pair_ddi, pair_type))

    insert_many("INSERT INTO mp12015.DOCUMENT VALUES (?)", documents)
    insert_many("INSERT INTO mp12015.SENTENCE VALUES (?,?,?)", sentences)

    insert_many("INSERT INTO mp12015.ENTITY VALUES(?,?,?,?)", entities)
    insert_many("INSERT INTO mp12015.PAIR VALUES (?,?,?,?,?)", pairs)
    insert_many("INSERT INTO mp12015.OFFSET VALUES (?,?,?)", offsets)
    connection.commit()



#Load credentials
f = open('config.yaml', 'r')
config = yaml.load(f)

connection = pyhdb.connect(
    host=config['credentials']['host'],
    port=config['credentials']['port'],
    user=config['credentials']['user'],
    password=config['credentials']['password']
)

cursor = connection.cursor()

#Looks for all files in the directory with .xml in it
for filename in os.listdir(filepath):
    if (".xml" in filename):
        files.append(filepath+filename)

for filename in files:
    insert_content(filename)