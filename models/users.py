from flask_login import UserMixin
from client.db_client import db_client


class Users(UserMixin):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.active = True
        self.is_admin = False

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

        user = db_client.fetch(exp, values)
        if user:
            return user
        else:
            return '{}'.format(404)

    @classmethod
    def get(cls, **kwargs):
        return cls.filter(**kwargs).__getitem__(0)
