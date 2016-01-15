# DDI-Corpus Importer

1. `pip install -r requirements.txt`.
2. Make sure that [../secrets.json](../secrets.json) contains the right credentials and address to the database. Have a look at [../secrets.json.example](../secrets.json.example) for the format.
3. Make sure the database schema is matching [../db_setup/hana.sql](../db_setup/hana.sql).
2. `python import.py path/to/ddi-corpus/drugbank/dataset/`.
