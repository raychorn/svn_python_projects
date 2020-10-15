BEGIN;
CREATE TABLE "blogmaker_entry" (
    "id" serial NOT NULL PRIMARY KEY,
    "pub_date" date NOT NULL,
    "pub_time" time NOT NULL,
    "slug" varchar(50) NOT NULL,
    "headline" varchar(255) NOT NULL,
    "summary" varchar(255) NULL,
    "image" varchar(100) NULL,
    "copyright" varchar(255) NULL,
    "body" text NOT NULL,
    "active" boolean NOT NULL,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "externalId" integer NULL
);
CREATE TABLE "blogmaker_tag" (
    "id" serial NOT NULL PRIMARY KEY,
    "tag" varchar(255) NOT NULL
);
CREATE TABLE "blogmaker_pingurl" (
    "id" serial NOT NULL PRIMARY KEY,
    "ping_url" varchar(200) NOT NULL,
    "blog_url" varchar(200) NOT NULL,
    "blog_name" varchar(200) NOT NULL
);
CREATE TABLE "blogmaker_entry_tags" (
    "id" serial NOT NULL PRIMARY KEY,
    "entry_id" integer NOT NULL REFERENCES "blogmaker_entry" ("id") DEFERRABLE INITIALLY DEFERRED,
    "tag_id" integer NOT NULL REFERENCES "blogmaker_tag" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("entry_id", "tag_id")
);
CREATE TABLE "blogmaker_entry_related_entries" (
    "id" serial NOT NULL PRIMARY KEY,
    "from_entry_id" integer NOT NULL REFERENCES "blogmaker_entry" ("id") DEFERRABLE INITIALLY DEFERRED,
    "to_entry_id" integer NOT NULL REFERENCES "blogmaker_entry" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("from_entry_id", "to_entry_id")
);
CREATE INDEX blogmaker_entry_pub_date ON "blogmaker_entry" ("pub_date");
CREATE INDEX blogmaker_entry_slug ON "blogmaker_entry" ("slug");
CREATE INDEX blogmaker_entry_user_id ON "blogmaker_entry" ("user_id");
COMMIT;
