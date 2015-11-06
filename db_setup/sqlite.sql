DROP TABLE "PAIRS";
DROP TABLE "DOC_ENTITIES";
DROP TABLE "ENTITIES";
DROP TABLE "DOCUMENTS";


CREATE TABLE "DOCUMENTS" (
                "ID" VARCHAR(255) PRIMARY KEY,
                "TEXT" NCLOB
              );

CREATE TABLE "ENTITIES" (
                "ID" INT PRIMARY KEY,
                "TYPE" VARCHAR(255),
                "TEXT" VARCHAR(255)
              );

CREATE TABLE "DOC_ENTITIES" (
                "ID" INTEGER PRIMARY KEY AUTOINCREMENT,
                "E_ID" VARCHAR(255),
                "DOC_ID" VARCHAR(255),
                "ENTITY_ID" INT,
                "START" INT,
                "END" INT
              );

CREATE TABLE "PAIRS" (
                "ID" INTEGER PRIMARY KEY AUTOINCREMENT,
                "E1_ID" VARCHAR(255),
                "E2_ID" VARCHAR(255),
                "DDI" TINYINT,
                "TYPE" VARCHAR(255)
              );
