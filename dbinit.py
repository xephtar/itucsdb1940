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
    '''
    CREATE SEQUENCE IF NOT EXISTS public.owners_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;
    '''
]


def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()


if __name__ == "__main__":
    url = 'postgres://sxmxcsbbhbitaq:374c6268b10c0d0181454a0dc010c322b7dfe53e173b05e7cfdd64ee5d7e042d@ec2-54-217-234-157.eu-west-1.compute.amazonaws.com:5432/det2ikhqat3u6m'
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    initialize(url)

