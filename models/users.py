from flask_login import UserMixin
from client.db_client import db_client


class Users(UserMixin):
    def __init__(self, id, username, password, active, is_admin):
        self.id = id
        self.username = username
        self.password = password
        self.active = active
        self.is_admin = is_admin

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
            return '{}'.format(404)

    @classmethod
    def get(cls, **kwargs):
        return cls.filter(**kwargs).__getitem__(0)
