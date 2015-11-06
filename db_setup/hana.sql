SET SCHEMA "LEARNING_TO_NOTE";

DROP TABLE "PAIRS";
DROP TABLE "DOC_ENTITIES";
DROP TABLE "ENTITIES";
DROP TABLE "DOCUMENTS";


CREATE COLUMN TABLE "DOCUMENTS" (
                "ID" VARCHAR(255) PRIMARY KEY,
                "TEXT" NCLOB
              );

CREATE COLUMN TABLE "ENTITIES" (
                "ID" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
                "TYPE" VARCHAR(255),
                "TEXT" VARCHAR(255)
              );

CREATE COLUMN TABLE "DOC_ENTITIES" (
                "ID" INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                "E_ID" VARCHAR(255),
                "DOC_ID" VARCHAR(255),
                "ENTITY_ID" INT,
                "START" INT,
                "END" INT
              );

CREATE COLUMN TABLE "PAIRS" (
                "ID" INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                "E1_ID" VARCHAR(255),
                "E2_ID" VARCHAR(255),
                "DDI" TINYINT,
                "TYPE" VARCHAR(255)
              );


TRUNCATE TABLE "PAIRS";
TRUNCATE TABLE "DOC_ENTITIES";
TRUNCATE TABLE "ENTITIES";
TRUNCATE TABLE "DOCUMENTS";