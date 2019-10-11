import os
import sys

import psycopg2 as dbapi2


INIT_STATEMENTS = [
    "CREATE TABLE IF NOT EXISTS DUMMY (NUM INTEGER)",
    '''
    CREATE SEQUENCE IF NOT EXISTS public.vet_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 99999999
    CACHE 1;
    ''',
    '''CREATE TABLE IF NOT EXISTS public.vets
    (
    id bigint NOT NULL DEFAULT nextval('vet_id_seq'::regclass),
    name text COLLATE pg_catalog."default",
    age integer,
    CONSTRAINT vets_pkey PRIMARY KEY (id)
    )''',
]


def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()


if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    initialize(url)

