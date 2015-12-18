SET SCHEMA LEARNING_TO_NOTE;

INSERT INTO USERS VALUES ('dr.schneider', 'Dr. Michael Schneider', 'secret');
INSERT INTO USER_DOCUMENTS VALUES ('dr.schneider_DDI-DrugBank.d532', 'dr.schneider', 'DDI-DrugBank.d532', 0, current_timestamp, current_timestamp);

INSERT INTO ENTITIES VALUES ('XDDI-DrugBank.d532.s0.e0', 'dr.schneider_DDI-DrugBank.d532', 0, 'drug', '');
INSERT INTO OFFSETS VALUES (37, 46, 'XDDI-DrugBank.d532.s0.e0', 'dr.schneider_DDI-DrugBank.d532');

INSERT INTO ENTITIES VALUES ('XDDI-DrugBank.d532.s1.e0', 'dr.schneider_DDI-DrugBank.d532', 0, 'drug', '');
INSERT INTO OFFSETS VALUES (72, 85, 'XDDI-DrugBank.d532.s1.e0', 'dr.schneider_DDI-DrugBank.d532');

INSERT INTO ENTITIES VALUES ('XDDI-DrugBank.d532.s2.e0', 'dr.schneider_DDI-DrugBank.d532', 0, 'drug', '');
INSERT INTO OFFSETS VALUES (307, 311, 'XDDI-DrugBank.d532.s2.e0', 'dr.schneider_DDI-DrugBank.d532');

INSERT INTO ENTITIES VALUES ('XDDI-DrugBank.d532.s2.e1', 'dr.schneider_DDI-DrugBank.d532', 0, 'drug', '');
INSERT INTO OFFSETS VALUES (315, 320, 'XDDI-DrugBank.d532.s2.e1', 'dr.schneider_DDI-DrugBank.d532');

INSERT INTO ENTITIES VALUES ('XDDI-DrugBank.d532.s2.e2', 'dr.schneider_DDI-DrugBank.d532', 1, 'group', '');
INSERT INTO OFFSETS VALUES (320, 356, 'XDDI-DrugBank.d532.s2.e2', 'dr.schneider_DDI-DrugBank.d532');

INSERT INTO ENTITIES VALUES ('XDDI-DrugBank.d532.s2.e3', 'dr.schneider_DDI-DrugBank.d532', 2, 'test', '');
INSERT INTO OFFSETS VALUES (358, 385, 'XDDI-DrugBank.d532.s2.e3', 'dr.schneider_DDI-DrugBank.d532');
