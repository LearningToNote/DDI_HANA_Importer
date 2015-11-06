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


def insert_content(filename):
    global e_id_counter
    print filename

    documents = []
    entities = []
    pairs = []
    offsets = []
    old_to_new_entity_id = {}

    tree = ET.parse(filename)
    root = tree.getroot()
    for document in root.iter('document'):
        text_offset = 0
        doc_id = document.get('id')
        sentences = []
        for sentence in document.findall('sentence'):
            sentence_text = sentence.get('text')
            sentences.append(sentence_text)

            for entity in sentence.findall('entity'):
                entity_type = entity.get('type')

                entity_obj = (e_id_counter, doc_id, entity_type)
                old_to_new_entity_id[entity.get('id')] = e_id_counter
                e_id_counter += 1
                entities.append(entity_obj)

                offset_list = entity.get('charOffset').split(';')
                for offset in offset_list:
                    offset_start, offset_end = map(int, offset.split('-'))
                    offset_start += text_offset
                    offset_end += text_offset + 1 # end offsets in DDI are offset by 1
                    offsets.append((offset_start, offset_end, entity_obj[0]))

            for pair in sentence.findall('pair'):
                pair_e1 = str(old_to_new_entity_id[pair.get('e1')])
                pair_e2 = str(old_to_new_entity_id[pair.get('e2')])
                pair_ddi = 1 if pair.get('ddi') == "true" else 0
                pair_type = pair.get('type')
                pairs.append((pair_e1, pair_e2, pair_ddi, pair_type))

            text_offset += len(sentence_text) + 1

        text = ' '.join(sentences)
        documents.append( (doc_id, text) )

        inserter.store(documents, entities, pairs, offsets)


#Looks for all files in the directory with .xml in it
for filename in os.listdir(filepath):
    if (".xml" in filename):
        files.append(filepath+filename)

for filename in files:
    insert_content(filename)
