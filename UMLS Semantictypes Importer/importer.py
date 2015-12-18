import json
import pyhdb

with open("../secrets.json") as f:
    secrets = json.load(f)

connection = pyhdb.connect(
    host=secrets['host'],
    port=secrets['port'],
    user=secrets['username'],
    password=secrets['password']
)

types = list()

with open("UMLS Semantic Types with Codes and Groups.txt", "r") as f:
    for line in f:
        t = line.strip('\n, ').split("|")
        types.append((t[2], t[0], t[1], t[3]))

connection.cursor().executemany("INSERT INTO LEARNING_TO_NOTE.TYPES(CODE, GROUP_ID, \"GROUP\", NAME) VALUES (?, ?, ?, ?)", types)

connection.commit()
connection.close()
