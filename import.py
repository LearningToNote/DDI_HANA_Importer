import xml.etree.ElementTree as ET
import os
import sys
import importlib

if len(sys.argv) > 2:
    inserter = importlib.import_module(sys.argv[2])
else:
    import inserter_hana as inserter

filepath = sys.argv[1]
files = []
e_id_counter = 0

documents = []
# dict (name(lowercased), type) -> entity_id
name_to_entity = {}
# dict new_id -> [old_id1, old_id2, ...]
old_to_new_entity = {}

doc_entities = []
pairs = []

def insert_content(filename):
    global e_id_counter
    print filename

    tree = ET.parse(filename)
    root = tree.getroot()
    for document in root.iter('document'):
        doc_id = document.get('id')
        doc_text = ""
        for sentence in document.findall('sentence'):
            # join all sentences of a document
            text_offset = len(doc_text) + 1
            doc_text = ' '.join([doc_text, sentence.get('text')])

            for entity in sentence.findall('entity'):
                entity_text = entity.get('text').lower()
                entity_type = entity.get('type')
                old_entity_id = entity.get('id')

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
                    offset_start += text_offset
                    offset_end += text_offset
                    doc_entities.append((old_entity_id, doc_id, entity_obj[0], offset_start, offset_end))

            for pair in sentence.findall('pair'):
                pair_e1 = pair.get('e1')
                pair_e2 = pair.get('e2')
                pair_ddi = 1 if pair.get('ddi') == "true" else 0
                pair_type = pair.get('type')
                pairs.append((pair_e1, pair_e2, pair_ddi, pair_type))
        documents.append( (doc_id, doc_text) )


#Looks for all files in the directory with .xml in it
for filename in os.listdir(filepath):
    if (".xml" in filename):
        files.append(filepath+filename)

for filename in files:
    insert_content(filename)
inserter.store(documents, name_to_entity.values(), doc_entities, pairs)
