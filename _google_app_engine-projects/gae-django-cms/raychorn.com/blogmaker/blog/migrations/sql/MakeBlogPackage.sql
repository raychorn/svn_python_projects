-- psql -c "update dbmigration_migrationhistory set app_name='blogmaker.blog' where app_name='blogmaker';"
-- psql -c "update dbmigration_migrationhistory set app_name='blogmaker.comments' where app_name='comments';"

DROP INDEX blogmaker_entry_pub_date;
DROP INDEX blogmaker_entry_slug;
DROP INDEX blogmaker_entry_user_id;
DROP INDEX blogmaker_trackbackstatus_entry_id;

ALTER TABLE blogmaker_entry RENAME TO blog_entry;
ALTER TABLE blogmaker_entry_related_entries RENAME TO blog_entry_related_entries;
ALTER TABLE blogmaker_entry_tags RENAME TO blog_entry_tags;
ALTER TABLE blogmaker_pingurl RENAME TO blog_pingurl;
ALTER TABLE blogmaker_tag RENAME TO blog_tag;
ALTER TABLE blogmaker_trackbackstatus RENAME TO blog_trackbackstatus;

CREATE INDEX blog_entry_pub_date ON "blog_entry" ("pub_date");
CREATE INDEX blog_entry_slug ON "blog_entry" ("slug");
CREATE INDEX blog_entry_user_id ON "blog_entry" ("user_id");
CREATE INDEX blog_trackbackstatus_entry_id ON "blog_trackbackstatus" ("entry_id");

UPDATE django_content_type set app_label='blog' WHERE app_label='blogmaker';
