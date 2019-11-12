from client.db_client import db_client
from models.vets import Vets
from models.owners import Owners


class Vets_to_Owners:
    sql_fields = [
        'owner_phone character varying(10) COLLATE pg_catalog."default" NOT NULL',
        'vet_id bigint NOT NULL',
        'CONSTRAINT vets_to_owners_pkey PRIMARY KEY(owner_phone, vet_id)',
        '''CONSTRAINT owner_phone_fkey FOREIGN KEY(owner_phone)
        REFERENCES public.owners(phonenumber) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID''',
        '''CONSTRAINT vet_id_fkey FOREIGN KEY(vet_id)
        REFERENCES public.vets(id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID'''
    ]

    sql_field_number = len(sql_fields)

    def __init__(self, phonenumber=None, vet_id=None):
        self.phonenumber = phonenumber
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
        # v = Vets.get(id=self.vet_id)
        # o = Owners.get(phonenumber=self.phonenumber)
        # if v and o:
        c = db_client.create(exp_relation_table, (self.phonenumber, self.vet_id))
        if c:
            return '{}'.format(404)
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
                    '{}'.format('owner_phone'),
                ]),
                values=','.join(['%s'])
            )
        else:
            exp = '''SELECT * FROM {table_name} ORDER BY vet_id ASC'''.format(
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

    @classmethod
    def create(cls, **kwargs):
        obj = cls(**kwargs)
        return obj.save()
