from client.db_client import db_client


class QueryList(list):

    def update(self, **kwargs):
        for item in self:
            item.update(**kwargs)

    def first(self):
        if self:
            return self[0]
        return None

    def last(self):
        if self:
            return self[-1]
        return None


class Vets:
    sql_fields = [
        "id bigint NOT NULL DEFAULT nextval('vet_id_seq'::regclass)",
        'name text COLLATE pg_catalog."default"',
        'age integer',
        'CONSTRAINT vets_pkey PRIMARY KEY (id)'
    ]

    sql_field_number = len(sql_fields)

    def __init__(self, id=None, name=None, age=None):
        self.id = id
        self.name = name
        self.age = age

        exp = '''CREATE TABLE IF NOT EXISTS {table_name} ({fields})'''.format(
            table_name=self.__class__.__name__.lower(),
            fields=','.join(self.sql_fields))

        db_client.query(exp)

    def save(self):
        if self.id:
            update_set = ','.join([
                "{key}=%s".format(key='name'),
                "{key}=%s".format(key='age'),
            ])
            exp = '''UPDATE {table_name} SET {values} WHERE id=%s RETURNING id'''.format(
                table_name=self.__class__.__name__.lower(),
                values=update_set,
            )
            self.id = db_client.fetch(exp, (self.name,
                                            self.age,
                                            self.id))[0][0]
        else:
            exp = '''INSERT INTO {table_name} ({table_fields}) VALUES ({values})'''.format(
                table_name=self.__class__.__name__.lower(),
                table_fields=','.join([
                    '{}'.format('name'),
                    '{}'.format('age')
                ]),
            )

            self.id = db_client.fetch(exp, (self.name,
                                            self.age))[0][0]
        return self

    def update(self, **kwargs):
        set_params = []
        set_values = []

        for key, value in kwargs.items():
            set_params.append("{}=%s".format(key))
            set_values.append(value)

        exp = '''UPDATE {table_name} SET {filter} WHERE id=%s'''.format(
            table_name=self.__class__.__name__.lower(),
            filter=','.join(set_params),
        )
        set_values.append(self.id)
        db_client.query(exp, set_values)
        self.__dict__.update(**kwargs)
        return self

    @classmethod
    def filter(cls, **kwargs):
        params = ['TRUE']
        values = []

        for key, value in kwargs.items():
            params.append("{}=%s".format(key))
            values.append(value)

        exp = '''SELECT * FROM {table_name} ORDER BY id ASC'''.format(
            table_name=cls.__name__.lower().join(params),
        )

        rows = db_client.fetch(exp, values)
        objects = [cls(*row) for row in rows]

        return QueryList(objects)

    @classmethod
    def get(cls, **kwargs):
        return cls.filter(**kwargs).first()

    @classmethod
    def create(cls, **kwargs):
        obj = cls(**kwargs)
        obj.save()
        return obj

