ALTER TABLE blogmaker_entry_id_seq RENAME TO blog_entry_id_seq;
ALTER TABLE blogmaker_entry_related_entries_id_seq RENAME TO blog_entry_related_entries_id_seq;
ALTER TABLE blogmaker_entry_tags_id_seq RENAME TO blog_entry_tags_id_seq;
ALTER TABLE blogmaker_pingurl_id_seq RENAME TO blog_pingurl_id_seq;
ALTER TABLE blogmaker_tag_id_seq RENAME TO blog_tag_id_seq;
ALTER TABLE blogmaker_trackbackstatus_id_seq RENAME TO blog_trackbackstatus_id_seq;

ALTER TABLE blog_trackbackstatus DROP CONSTRAINT blogmaker_trackbackstatus_entry_id_fkey;
ALTER TABLE blog_entry_tags DROP CONSTRAINT blogmaker_entry_tags_entry_id_fkey;
ALTER TABLE blog_entry_related_entries DROP CONSTRAINT blogmaker_entry_related_entries_from_entry_id_fkey;
ALTER TABLE blog_entry_related_entries DROP CONSTRAINT blogmaker_entry_related_entries_to_entry_id_fkey;
ALTER TABLE blog_entry DROP CONSTRAINT blogmaker_entry_pkey;

ALTER TABLE blog_entry_tags DROP CONSTRAINT blogmaker_entry_tags_tag_id_fkey;
ALTER TABLE blog_tag DROP CONSTRAINT blogmaker_tag_pkey;

ALTER TABLE blog_entry ADD CONSTRAINT blog_entry_pkey PRIMARY KEY(id);

ALTER TABLE blog_entry DROP CONSTRAINT blogmaker_entry_user_id_fkey;
ALTER TABLE blog_entry
  ADD CONSTRAINT blog_entry_user_id_fkey FOREIGN KEY (user_id)
      REFERENCES auth_user (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE blog_entry_related_entries DROP CONSTRAINT blogmaker_entry_related_entries_pkey;
ALTER TABLE blog_entry_related_entries
  ADD CONSTRAINT blog_entry_related_entries_pkey PRIMARY KEY(id);

ALTER TABLE blog_entry_related_entries
  ADD CONSTRAINT blog_entry_related_entries_from_entry_id_fkey FOREIGN KEY (from_entry_id)
      REFERENCES blog_entry (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE blog_entry_related_entries
  ADD CONSTRAINT blog_entry_related_entries_to_entry_id_fkey FOREIGN KEY (to_entry_id)
      REFERENCES blog_entry (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED;


ALTER TABLE blog_entry_related_entries DROP CONSTRAINT blogmaker_entry_related_entries_from_entry_id_key;
ALTER TABLE blog_entry_related_entries
  ADD CONSTRAINT blog_entry_related_entries_from_entry_id_key UNIQUE(from_entry_id, to_entry_id);

ALTER TABLE blog_entry_tags DROP CONSTRAINT blogmaker_entry_tags_pkey;
ALTER TABLE blog_entry_tags
  ADD CONSTRAINT blog_entry_tags_pkey PRIMARY KEY(id);

ALTER TABLE blog_entry_tags
  ADD CONSTRAINT blog_entry_tags_entry_id_fkey FOREIGN KEY (entry_id)
      REFERENCES blog_entry (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE blog_entry_tags DROP CONSTRAINT blogmaker_entry_tags_entry_id_key;
ALTER TABLE blog_entry_tags
  ADD CONSTRAINT blog_entry_tags_entry_id_key UNIQUE(entry_id, tag_id);

ALTER TABLE blog_pingurl DROP CONSTRAINT blogmaker_pingurl_pkey;
ALTER TABLE blog_pingurl
  ADD CONSTRAINT blog_pingurl_pkey PRIMARY KEY(id);

ALTER TABLE blog_tag
  ADD CONSTRAINT blog_tag_pkey PRIMARY KEY(id);

ALTER TABLE blog_entry_tags
  ADD CONSTRAINT blog_entry_tags_tag_id_fkey FOREIGN KEY (tag_id)
      REFERENCES blog_tag (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE blog_trackbackstatus DROP CONSTRAINT blogmaker_trackbackstatus_pkey;
ALTER TABLE blog_trackbackstatus
  ADD CONSTRAINT blog_trackbackstatus_pkey PRIMARY KEY(id);

ALTER TABLE blog_trackbackstatus
  ADD CONSTRAINT blog_trackbackstatus_entry_id_fkey FOREIGN KEY (entry_id)
      REFERENCES blog_entry (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED;
