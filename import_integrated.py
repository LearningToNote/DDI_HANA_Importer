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
    # dict (name(lowercased), type) -> entity_id
    name_to_entity = {}
    # dict new_id -> [old_id1, old_id2, ...]
    old_to_new_entity = {}
    e_id_counter = 0

    doc_entities = []
    pairs = []

    tree = ET.parse(filename)
    root = tree.getroot()
    for document in root.iter('document'):
        doc_id = document.get('id')
        doc_text = ""
        for sentence in document.findall('sentence'):
            # join all sentences of a document
            doc_text += ' ' + sentence.get('text')

            for entity in sentence.findall('entity'):
                entity_text = entity.get('text').lower()
                entity_type = entity.get('type')

                # find or create entity
                if (entity_text, entity_type) in name_to_entity:
                    entity_obj = name_to_entity[entity_text, entity_type]
                else:
                    entity_obj = (e_id_counter, entity_text, entity_type)
                    e_id_counter += 1
                    name_to_entity[entity_text, entity_type] = entity_obj

                old_to_new_entity[entity.get('id')] = entity_obj[0]

                offsets = entity.get('charOffset').split(';', 1)
                for offset in offsets:
                    offset_start, offset_end = map(int, offset.split('-'))
                    doc_entities.append((doc_id, entity[0], offset_start, offset_end))

            for pair in sentence.findall('pair'):
                pair_e1 = old_to_new_entity[pair.get('e1')]
                pair_e2 = old_to_new_entity[pair.get('e2')]
                pair_ddi = 1 if pair.get('ddi') == "true" else 0
                pair_type = pair.get('type')
                pairs.append((pair_e1, pair_e2, pair_ddi, pair_type))

        documents.append( (doc_id, doc_text) )


    insert_many("INSERT INTO mp12015.DOCUMENT VALUES (?,?)", documents)
    insert_many("INSERT INTO mp12015.ENTITY VALUES(?,?,?)", name_to_entity.values())
    insert_many("INSERT INTO mp12015.DOC_ENTITY VALUES(?,?,?,?)", doc_entities)
    insert_many("INSERT INTO mp12015.PAIR VALUES (?,?,?,?)", pairs)
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
