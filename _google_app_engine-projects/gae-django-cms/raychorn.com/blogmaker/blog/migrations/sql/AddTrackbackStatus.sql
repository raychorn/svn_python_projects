CREATE TABLE "blogmaker_trackbackstatus" (
    "id" serial NOT NULL PRIMARY KEY,
    "entry_id" integer NOT NULL REFERENCES "blogmaker_entry" ("id") DEFERRABLE INITIALLY DEFERRED,
    "link" varchar(200) NOT NULL,
    "attempted" timestamp with time zone NULL,
    "status" varchar(10) NOT NULL DEFAULT 'NotYet',
    "msg" varchar(255) NOT NULL DEFAULT ''
);
CREATE INDEX blogmaker_trackbackstatus_entry_id ON "blogmaker_trackbackstatus" ("entry_id");
