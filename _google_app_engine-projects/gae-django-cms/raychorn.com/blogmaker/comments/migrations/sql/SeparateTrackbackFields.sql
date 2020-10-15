ALTER TABLE "comments_comment" ADD COLUMN "trackback_name" varchar(255) NOT NULL DEFAULT '';
ALTER TABLE "comments_comment" ADD COLUMN "trackback_title" varchar(255) NOT NULL DEFAULT '';
ALTER TABLE "comments_comment" ADD COLUMN "trackback_www" varchar(200) NOT NULL DEFAULT '';