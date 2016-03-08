SET SCHEMA "LTN_DEVELOP";

DROP TABLE "PAIRS";
DROP TABLE "OFFSETS";
DROP TABLE "ENTITIES";
DROP TABLE "USER_DOCUMENTS";
DROP TABLE "USERS";
DROP TABLE "DOCUMENTS";
DROP TABLE "TYPES";
DROP TABLE "POS_TAGS";


CREATE COLUMN TABLE "DOCUMENTS" (
    "ID" VARCHAR(255) PRIMARY KEY,
    "TASK" INT
);

CREATE COLUMN TABLE "USERS" (
    "ID" VARCHAR(255) PRIMARY KEY,
    "NAME" VARCHAR(255),
    "TOKEN" VARCHAR(1024),
    "DESCRIPTION" NVARCHAR(255),
    "IMAGE" CLOB
);

CREATE COLUMN TABLE "USER_DOCUMENTS" (
    "ID" VARCHAR(255) PRIMARY KEY,
    "USER_ID" VARCHAR(255),
    "DOCUMENT_ID" VARCHAR(255),
    "VISIBILITY" TINYINT,
    "CREATED_AT" TIMESTAMP,
    "UPDATED_AT" TIMESTAMP

    -- FOREIGN KEY("USER_ID") REFERENCES "USERS",
    -- FOREIGN KEY("DOCUMENT_ID") REFERENCES "DOCUMENTS"
);

CREATE COLUMN TABLE "TYPES" (
    "ID" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    "CODE" VARCHAR(255),
    "GROUP_ID" VARCHAR(255),
    "GROUP" VARCHAR(255),
    "NAME" VARCHAR(255)
);

CREATE COLUMN TABLE "ENTITIES" (
    "ID" VARCHAR(255),
    "USER_DOC_ID" VARCHAR(255),
    "TYPE_ID" INT,
    "LABEL" VARCHAR(255),
    "TEXT" VARCHAR(255),

    PRIMARY KEY("ID", "USER_DOC_ID")
    -- FOREIGN KEY("USER_DOC_ID") REFERENCES "USER_DOCUMENTS",
    -- FOREIGN KEY("TYPE_ID") REFERENCES "TYPES"
);

CREATE COLUMN TABLE "OFFSETS" (
    "START" INT,
    "END" INT,
    "ENTITY_ID" VARCHAR(255),
    "USER_DOC_ID" VARCHAR(255)

    -- FOREIGN KEY("ENTITY_ID", "USER_DOC_ID") REFERENCES "ENTITIES"("ID", "USER_DOC_ID")
);

CREATE COLUMN TABLE "PAIRS" (
    "ID" INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "E1_ID" VARCHAR(255),
    "E2_ID" VARCHAR(255),
    "USER_DOC_ID" VARCHAR(255),
    "DDI" TINYINT,
    "TYPE_ID" INT,
    "LABEL" VARCHAR(255)

    -- FOREIGN KEY("E1_ID", "USER_DOC_ID") REFERENCES "ENTITIES"("ID", "USER_DOC_ID"),
    -- FOREIGN KEY("E2_ID", "USER_DOC_ID") REFERENCES "ENTITIES"("ID", "USER_DOC_ID"),
    -- FOREIGN KEY("TYPE_ID") REFERENCES "TYPES"
);

CREATE COLUMN TABLE "POS_TAGS" (
    "ID" INTEGER GENERATED BY DEFAULT AS IDENTITY, 
    "POS" VARCHAR(255)
);



DELETE FROM "PAIRS";
DELETE FROM "OFFSETS";
DELETE FROM "ENTITIES";
DELETE FROM "USER_DOCUMENTS";
DELETE FROM "USERS";
DELETE FROM "DOCUMENTS";
DELETE FROM "TYPES";
DELETE FROM "POS_TAGS";
