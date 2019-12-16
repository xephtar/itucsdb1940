from flask_login import UserMixin
from client.db_client import db_client
from passlib.hash import pbkdf2_sha256 as hasher


class Users(UserMixin):
    sql_fields = [
        "id integer NOT NULL DEFAULT nextval('users_id_seq'::regclass)",
        'username character varying COLLATE pg_catalog."default" NOT NULL',
        'password character varying COLLATE pg_catalog."default" NOT NULL',
        'is_admin boolean',
        'active boolean',
        'CONSTRAINT users_pkey PRIMARY KEY (id, username)'
    ]

    sql_field_number = len(sql_fields)

    def __init__(self, id=None, username=None, password=None, is_admin=None, active=None):
        self.id = id
        self.username = username
        self.password = password
        self.active = is_admin
        self.is_admin = active

        exp = '''CREATE TABLE IF NOT EXISTS {table_name} ({fields})'''.format(
            table_name=self.__class__.__name__.lower(),
            fields=','.join(self.sql_fields))
        db_client.query(exp)

    def save(self):
        if self.id:
            update_set = ','.join([
                "{key}=%s".format(key='username'),
                "{key}=%s".format(key='password'),
                "{key}=%s".format(key='is_admin'),
                "{key}=%s".format(key='active')
            ])
            exp = '''UPDATE {table_name} SET {values} WHERE id=%s RETURNING id'''.format(
                table_name=self.__class__.__name__.lower(),
                values=update_set,
            )
            self.id = db_client.fetch(exp, (self.username, self.password,
                                            self.is_admin, self.active,
                                            self.id))[0][0]
        else:
            exp = '''INSERT INTO {table_name} ({table_fields}) VALUES ({values})'''.format(
                table_name=self.__class__.__name__.lower(),
                table_fields=','.join([
                    '{}'.format('username'),
                    '{}'.format('password'),
                    '{}'.format('is_admin'),
                    '{}'.format('active'),
                ]),
                values=','.join(['%s', '%s', '%s', '%s'])
            )
            self.password = hasher.hash(self.password)
            self.active = True
            c = db_client.create(exp, (self.username, self.password, self.is_admin, self.active))
            if c:
                return {}, 404

        return self

    def get_id(self):
        return self.username

    @property
    def is_active(self):
        return self.active

    @classmethod
    def filter(cls, **kwargs):
        params = []
        values = []

        for key, value in kwargs.items():
            params.append("{}=%s".format(key))
            values.append(value)
        if bool(kwargs.items()):
            exp = '''SELECT * FROM {table_name} WHERE {params} ORDER BY id DESC'''.format(
                table_name=cls.__name__.lower(),
                params=' AND '.join(params),
            )
        else:
            exp = '''SELECT * FROM {table_name} ORDER BY id ASC'''.format(
                table_name=cls.__name__.lower()
            )

        rows = db_client.fetch(exp, values)
        if rows:
            objects = [cls(*row) for row in rows]
            return objects
        else:
            return {}, 404

    @classmethod
    def get(cls, **kwargs):
        return cls.filter(**kwargs).__getitem__(0)

    @classmethod
    def create(cls, **kwargs):
        obj = cls(**kwargs)
        return obj.save()
