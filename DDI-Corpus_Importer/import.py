import xml.etree.ElementTree as ET
import os
import sys
import datetime

import inserter_hana as inserter

from collections import namedtuple


Type = namedtuple("Type", ["id", "base_type"])
NoType = Type(id=None, base_type=None)


def load_stop_words():
    stops = []
    with open('stopwords.txt', 'r') as f:
        for line in f:
            stops.append(line.translate(None, '\r\n'))
    return stops

if len(sys.argv) != 4:
    print 'Usage: python import.py <initial> <username> <path>'
    print '\t initial: whether types and users should be created'
    print '\t username: name of importer user, e.g. DDI-IMPORTER'
    print '\t path: path to DDI xml files, e.g. ../../DDICorpus/Train/DrugBank/'
    exit()

initial = sys.argv[1] in ['true', 'True', '1', 'y', 'yes']
USERNAME = sys.argv[2]
filepath = os.path.join(sys.argv[3], '')
files = []
e_id_counter = 0
types = {
    'drug': Type(id=0, base_type='T200'),
    'group': Type(1, 'T071'),
    'brand': Type(2, 'T121'),
    'drug_n': Type(3, 'T200')}
relation_types = {
    'mechanism': Type(4, 'T067'),
    'effect': Type(5, 'T067'),
    'advise': Type(6, 'T067'),
    'int': Type(7, 'T067')}
task = None

if initial:
    print "Inserting User..."
    inserter.store_user(USERNAME, USERNAME, "", "Drug-Drug Interaction Corpus Importer", "")
    print "Done."

    print "Inserting Task..."
    task = inserter.create_task(USERNAME)
    print "Done."

    print "Inserting Stopwords"
    inserter.insert_stop_words(load_stop_words())
    print "Done."

    print "Inserting Types..."
    for label, template in types.items():
        inserter.insert_task_types(template, relation=False, task=task, label=label)
    for label, template in relation_types.items():
        inserter.insert_task_types(template, relation=True, task=task, label=label)
    print "Done."
else:
    print "Preparing Task..."
    task = inserter.get_task_id()
    if task is None:
        task = inserter.create_task(USERNAME)
    print "Done."

for filename in os.listdir(filepath):
    if ".xml" in filename:
        files.append(filepath + filename)

for filename in files:
    print filename

    documents = []
    user_documents = []
    entities = []
    pairs = []
    offsets = []

    tree = ET.parse(filename)
    root = tree.getroot()
    for document in root.iter('document'):
        text_offset = 0
        doc_id = document.get('id')
        user_doc_id = USERNAME + "_" + doc_id
        sentences = []
        for sentence in document.findall('sentence'):
            sentence_text = sentence.get('text')
            sentences.append(sentence_text)

            for entity in sentence.findall('entity'):
                entity_type = entity.get('type')
                entity_text = entity.get('text')
                e_id = entity.get('id')
                entity_obj = (e_id, user_doc_id, types.get(entity_type, NoType).id, None, entity_text)
                entities.append(entity_obj)

                offset_list = entity.get('charOffset').split(';')
                for offset in offset_list:
                    offset_start, offset_end = map(int, offset.split('-'))
                    offset_start += text_offset
                    offset_end += text_offset + 1  # end offsets in DDI are offset by 1
                    offsets.append((offset_start, offset_end, entity_obj[0], user_doc_id))

            for pair in sentence.findall('pair'):
                pair_e1 = pair.get('e1')
                pair_e2 = pair.get('e2')
                pair_ddi = 1 if pair.get('ddi') == "true" else 0
                pair_type = pair.get('type')
                pairs.append((pair_e1, pair_e2, user_doc_id, pair_ddi, relation_types.get(pair_type, NoType).id,
                              pair_type))

            text_offset += len(sentence_text) + 1

        text = ' '.join(sentences)
        documents.append((doc_id, text))
        user_documents.append((user_doc_id, USERNAME, doc_id, 1, datetime.datetime.now(), datetime.datetime.now()))

    inserter.store(documents, user_documents, entities, pairs, offsets, task)
