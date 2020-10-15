ALTER TABLE blogmaker_trackbackstatus RENAME COLUMN "msg" TO "message";
ALTER TABLE blogmaker_trackbackstatus ADD COLUMN "trackbackUrl" varchar(200) NOT NULL DEFAULT '';

