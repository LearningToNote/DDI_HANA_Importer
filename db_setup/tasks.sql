SET SCHEMA LEARNING_TO_NOTE;

DROP PROCEDURE get_document_content;

CREATE PROCEDURE get_document_content(IN document_id varchar(255)) LANGUAGE SQLSCRIPT AS
BEGIN
    DECLARE table_id nvarchar(255);
    SELECT concat(name, '') INTO table_id FROM TASKS t JOIN DOCUMENTS d ON d.task = t.id WHERE d.id = document_id;
    EXECUTE IMMEDIATE 'select * from ' || :table_id || ' where id = ''' || document_id || '''';
END;
