DROP TABLE "PAIRS";
DROP TABLE "ENTITIES";
DROP TABLE "OFFSETS";
DROP TABLE "DOCUMENTS";


CREATE TABLE "DOCUMENTS" (
                "ID" VARCHAR(255) PRIMARY KEY,
                "TEXT" NCLOB
              );

CREATE TABLE "ENTITIES" (
                "ID" VARCHAR(255) PRIMARY KEY,
                "DOC_ID" VARCHAR(255),
                "TYPE" VARCHAR(255)
              );

CREATE TABLE "OFFSETS" (
                "START" INT,
                "END" INT,
                "ENTITY_ID" VARCHAR(255)
              );

CREATE TABLE "PAIRS" (
                "ID" INT PRIMARY KEY AUTOINCREMENT,
                "E1_ID" VARCHAR(255),
                "E2_ID" VARCHAR(255),
                "DDI" TINYINT,
                "TYPE" VARCHAR(255)
              );


TRUNCATE TABLE "PAIRS";
TRUNCATE TABLE "OFFSETS";
TRUNCATE TABLE "ENTITIES";
TRUNCATE TABLE "DOCUMENTS";
