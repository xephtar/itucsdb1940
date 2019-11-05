import os
import psycopg2 as db


class Client(object):

    def __init__(self):
        self.dsn = 'postgres://sxmxcsbbhbitaq:374c6268b10c0d0181454a0dc010c322b7dfe53e173b05e7cfdd64ee5d7e042d@ec2-54-217-234-157.eu-west-1.compute.amazonaws.com:5432/det2ikhqat3u6m'
        self.connection = db.connect(self.dsn)
        self.cursor = self.connection.cursor()

    def query(self, statement, params=None):
        try:
            self.cursor.execute(statement, params)
            self.connection.commit()
        except:
            self.connection.rollback()
            raise

    def fetch(self, statement, params=None):
        try:
            self.cursor.execute(statement, params)
            self.connection.commit()
            return self.cursor.fetchall()
        except:
            self.connection.rollback()
            raise

    def create(self, statement, params=None):
        try:
            self.cursor.execute(statement, params)
            self.connection.commit()
        except:
            self.connection.rollback()
            raise

    def __del__(self):
        self.connection.close()
        self.cursor.close()


db_client = Client()
