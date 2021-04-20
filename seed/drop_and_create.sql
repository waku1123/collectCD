DROP TABLE "public"."artists" cascade;
DROP TABLE "public"."albums";
DROP TABLE "public"."users";

CREATE TABLE "public"."users" (
                                  "id" serial NOT NULL,
                                  "name" varchar,
                                  "email" varchar NOT NULL,
                                  "password" varchar,
                                  "created_at" timestamp,
                                  "updated_at" timestamp,
                                  PRIMARY KEY ("id")
);

CREATE TABLE "public"."artists" (
                                    "id" serial NOT NULL,
                                    "name" varchar(255) NOT NULL,
                                    "created_at" timestamp(0) NOT NULL DEFAULT '2021-01-01 00:00:00'::timestamp without time zone,
                                    "updated_at" timestamp(0),
                                    PRIMARY KEY ("id")
);

CREATE TABLE "public"."albums" (
                                   "id" serial NOT NULL,
                                   "artist_id" int8 NOT NULL,
                                   "order" int2,
                                   "name" varchar NOT NULL,
                                   "publish_year" int2,
                                   "publish_month" int2,
                                   "possession" bool NOT NULL DEFAULT false,
                                   "created_at" timestamp(0) NOT NULL DEFAULT '2021-01-01 00:00:00'::timestamp without time zone,
                                   "updated_at" timestamp(0),
                                   CONSTRAINT "albums_artist_id_fkey" FOREIGN KEY ("artist_id") REFERENCES "public"."artists"("id"),
                                   PRIMARY KEY ("id")
);
