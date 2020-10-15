ALTER TABLE "blogmaker_entry" ALTER COLUMN "pub_date" TYPE timestamp with time zone USING CAST("pub_date" || ' ' || "pub_time" || ' EDT' AS "timestamp");
ALTER TABLE "blogmaker_entry" DROP COLUMN "pub_time";
