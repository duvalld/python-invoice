BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "sales_representatives" (
	"id"	INTEGER,
	"name"	TEXT NOT NULL,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "customers" (
	"id"	INTEGER,
	"name"	TEXT NOT NULL,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "vendors" (
	"id"	INTEGER,
	"name"	TEXT NOT NULL,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "products" (
	"id"	INTEGER,
	"name"	TEXT NOT NULL,
	"vendor_id"	INTEGER NOT NULL,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "invoice" (
	"id"	INTEGER,
	"sales_rep_id"	TEXT NOT NULL,
	"customer_id"	INTEGER NOT NULL,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "invoice_items" (
	"id"	INTEGER,
	"invoice_id"	TEXT NOT NULL,
	"product_id"	INTEGER NOT NULL,
	PRIMARY KEY("id")
);
INSERT INTO "sales_representatives" VALUES (1,'Mark');
INSERT INTO "sales_representatives" VALUES (2,'Duvall');
INSERT INTO "customers" VALUES (1,'Shellsoft');
INSERT INTO "vendors" VALUES (1,'StackTrek');
INSERT INTO "products" VALUES (1,'Shirt',1);
INSERT INTO "invoice" VALUES (1,'1',1);
INSERT INTO "invoice_items" VALUES (1,'1',1);
INSERT INTO "invoice_items" VALUES (2,'1',1);
COMMIT;
