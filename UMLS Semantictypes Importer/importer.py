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

cursor = connection.cursor()
cursor.executemany("INSERT INTO LTN_DEVELOP.TYPES(CODE, GROUP_ID, \"GROUP\", NAME) VALUES (?, ?, ?, ?)", types)
connection.commit()

groups = list()
cursor.execute('SELECT DISTINCT "GROUP_ID", "GROUP" FROM LTN_DEVELOP.TYPES')
for row in cursor.fetchall():
    groups.append((row[0], row[0], row[1], row[1]))

cursor.executemany("INSERT INTO LTN_DEVELOP.TYPES(CODE, GROUP_ID, \"GROUP\", NAME) VALUES (?, ?, ?, ?)", groups)
connection.commit()

connection.close()
