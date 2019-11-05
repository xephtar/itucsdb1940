from client.db_client import db_client


class Owners:
    sql_fields = [
        'age character varying(2) COLLATE pg_catalog."default"',
        'name text COLLATE pg_catalog."default"',
        '"phonenumber" character varying(10) COLLATE pg_catalog."default" NOT NULL',
        "id integer NOT NULL DEFAULT nextval('owners_id_seq'::regclass)",
        'CONSTRAINT owners_pkey PRIMARY KEY ("phonenumber")',
        'CONSTRAINT owners_unique UNIQUE ("phonenumber")'
    ]

    sql_field_number = len(sql_fields)

    def __init__(self, age=None, name=None, phonenumber=None, id=None):
        self.id = id
        self.name = name
        self.age = age
        self.phonenumber = phonenumber

        exp = '''CREATE TABLE IF NOT EXISTS {table_name} ({fields})'''.format(
            table_name=self.__class__.__name__.lower(),
            fields=','.join(self.sql_fields))

        db_client.query(exp)

    def save(self):
        if self.id:
            update_set = ','.join([
                "{key}=%s".format(key='name'),
                "{key}=%s".format(key='age'),
                "{key}=%s".format(key='phonenumber'),
            ])
            exp = '''UPDATE {table_name} SET {values} WHERE id=%s RETURNING id'''.format(
                table_name=self.__class__.__name__.lower(),
                values=update_set,
            )
            self.id = db_client.fetch(exp, (self.name,
                                            self.age,
                                            self.phonenumber,
                                            self.id))[0][0]
        else:
            exp = '''INSERT INTO {table_name} ({table_fields}) VALUES ({values})'''.format(
                table_name=self.__class__.__name__.lower(),
                table_fields=','.join([
                    '{}'.format('age'),
                    '{}'.format('name'),
                    '{}'.format('phonenumber'),
                ]),
                values=','.join(['%s', '%s', '%s'])
            )
            db_client.create(exp, (self.age, self.name, self.phonenumber))

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

        if kwargs.items():
            exp = '''SELECT * FROM {table_name} WHERE {table_fields} = {values}'''.format(
                table_name=cls.__name__.lower(),
                table_fields=','.join([
                    '{}'.format('phonenumber'),
                ]),
                values=','.join(['%s'])
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

    def save_relation(self):
        exp_relation_table = '''INSERT INTO {table_name} ({table_fields}) VALUES ({values})'''.format(
            table_name='vets_to_owners',
            table_fields=','.join([
                '{}'.format('owner_phone'),
                '{}'.format('vet_id'),
            ]),
            values=','.join(['%s', '%s'])
        )

        u = self.get(phonenumber=self.phonenumber)
        if u:
            db_client.create(exp_relation_table, (self.phonenumber, self.vet))

    @classmethod
    def get(cls, **kwargs):
        return cls.filter(**kwargs).__getitem__(0)

    @classmethod
    def create(cls, **kwargs):
        obj = cls(**kwargs)
        return obj.save()

