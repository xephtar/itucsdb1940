from client.db_client import db_client


class Vets_to_Owners:
    sql_fields = [
        'owner_phone character varying(10) COLLATE pg_catalog."default" NOT NULL',
        'vet_id bigint NOT NULL',
        'CONSTRAINT vets_to_owners_pkey PRIMARY KEY(owner_phone, vet_id)',
        '''CONSTRAINT owner_phone_fkey FOREIGN KEY(owner_phone)
        REFERENCES public.owners(phonenumber) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        ''',
        '''CONSTRAINT vet_id_fkey FOREIGN KEY(vet_id)
        REFERENCES public.vets(id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        '''
    ]

    sql_field_number = len(sql_fields)

    def __init__(self, owner_phone=None, vet_id=None):
        self.owner_phone = owner_phone
        self.vet_id = vet_id

        exp = '''CREATE TABLE IF NOT EXISTS {table_name} ({fields})'''.format(
            table_name=self.__class__.__name__.lower(),
            fields=','.join(self.sql_fields))

        db_client.query(exp)

    def save(self):
        exp_relation_table = '''INSERT INTO {table_name} ({table_fields}) VALUES ({values})'''.format(
            table_name=self.__class__.__name__.lower(),
            table_fields=','.join([
                '{}'.format('owner_phone'),
                '{}'.format('vet_id'),
            ]),
            values=','.join(['%s', '%s'])
        )
        print(self.owner_phone)
        print(self.vet_id)
        c = db_client.create(exp_relation_table, (self.owner_phone, self.vet_id))
        if c:
            return {}, 404
        return self

    @classmethod
    def filter(cls, **kwargs):
        params = []
        values = []

        for key, value in kwargs.items():
            params.append("{}=%s".format(key))
            values.append(value)
        if bool(kwargs.items()):
            exp = '''SELECT * FROM {table_name} WHERE {params} ORDER BY vet_id DESC'''.format(
                table_name=cls.__name__.lower(),
                params=' AND '.join(params),
            )
        else:
            exp = '''SELECT * FROM {table_name} ORDER BY vet_id'''.format(
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
        return cls.filter(**kwargs)

    @classmethod
    def create(cls, **kwargs):
        obj = cls(**kwargs)
        return obj.save()
