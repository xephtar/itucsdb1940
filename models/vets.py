from client.db_client import db_client


class Vets:
    sql_fields = [
        "id bigint NOT NULL DEFAULT nextval('vet_id_seq'::regclass)",
        'name text COLLATE pg_catalog."default"',
        'age integer',
        'address character varying COLLATE pg_catalog."default"',
        'profession character varying COLLATE pg_catalog."default"',
        'gender character varying COLLATE pg_catalog."default"',
        'CONSTRAINT vets_pkey PRIMARY KEY (id)'
    ]

    sql_field_number = len(sql_fields)

    def __init__(self, id=None, name=None, age=None, address=None, profession=None, gender=None):
        self.id = id
        self.name = name
        self.age = age
        self.address = address
        self.profession = profession
        self.gender = gender

        exp = '''CREATE TABLE IF NOT EXISTS {table_name} ({fields})'''.format(
            table_name=self.__class__.__name__.lower(),
            fields=','.join(self.sql_fields))

        db_client.query(exp)

    def save(self):
        if self.id:
            update_set = ','.join([
                "{key}=%s".format(key='name'),
                "{key}=%s".format(key='age'),
                "{key}=%s".format(key='address'),
                "{key}=%s".format(key='profession'),
                "{key}=%s".format(key='gender')
            ])
            exp = '''UPDATE {table_name} SET {values} WHERE id=%s RETURNING id'''.format(
                table_name=self.__class__.__name__.lower(),
                values=update_set,
            )
            self.id = db_client.fetch(exp, (self.name, self.age,
                                            self.address, self.profession,
                                            self.gender, self.id))[0][0]
        else:
            exp = '''INSERT INTO {table_name} ({table_fields}) VALUES ({values})'''.format(
                table_name=self.__class__.__name__.lower(),
                table_fields=','.join([
                    '{}'.format('name'),
                    '{}'.format('age'),
                    '{}'.format('address'),
                    '{}'.format('profession'),
                    '{}'.format('gender'),
                ]),
                values=','.join(['%s', '%s', '%s', '%s', '%s'])
            )

            c = db_client.create(exp, (self.name, self.age, self.address, self.profession, self.gender))
            if c:
                return {}, 404

        return self

    def delete(self, **kwargs):
        set_params = []
        set_values = []

        for key, value in kwargs.items():
            set_params.append("{}=%s".format(key))
            set_values.append(value)

        exp = '''DELETE FROM {table_name} WHERE id=%s'''.format(
            table_name=self.__class__.__name__.lower(),
        )
        set_values.append(self.id)
        db_client.query(exp, set_values)
        self.__dict__.update(**kwargs)
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

