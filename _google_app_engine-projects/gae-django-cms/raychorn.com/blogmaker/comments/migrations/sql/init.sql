BEGIN;
CREATE TABLE "comments_comment" (
    "id" serial NOT NULL PRIMARY KEY,
    "content_type_id" integer NOT NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED,
    "object_id" integer NOT NULL,
    "comment" text NOT NULL,
    "person_name" varchar(50) NOT NULL,
    "person_email" varchar(75) NOT NULL,
    "person_www" varchar(200) NOT NULL,
    "submit_date" timestamp with time zone NOT NULL,
    "is_public" boolean NOT NULL,
    "ip_address" inet NOT NULL,
    "approved" boolean NOT NULL,
    "site_id" integer NOT NULL REFERENCES "django_site" ("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE INDEX comments_comment_content_type_id ON "comments_comment" ("content_type_id");
CREATE INDEX comments_comment_site_id ON "comments_comment" ("site_id");
COMMIT;
