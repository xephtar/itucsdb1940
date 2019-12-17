Parts Implemented by Ömer Faruk Davarcı
=======================================

Vet
---

**Vet Model**::

    .. code-block:: python
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


**Vet View**::

    .. code-block:: python
    from flask_login import login_required, current_user
    from flask_restful import reqparse, Resource
    from flask import redirect, abort, flash, request, url_for
    from models.vets import Vets


    class VetsAPI(Resource):
        method_decorators = [login_required]

        def __init__(self):
            self.parser = reqparse.RequestParser()
            self.parser.add_argument('name', type=str)
            self.parser.add_argument('age', type=str)
            self.parser.add_argument('address', type=str)
            self.parser.add_argument('profession', type=str)
            self.parser.add_argument('gender', type=str)

        def post(self, id):
            method = reqparse.RequestParser()
            method.add_argument('_method', type=str)
            method = method.parse_args()
            if method['_method'] == "Delete":
                if VetsAPI.delete(self, id):
                    flash("Success, Vet is deleted!")
                else:
                    flash("Fail, Vet is not deleted!")
                next_page = request.args.get("next", url_for("home_page"))
                return redirect(next_page)
            elif method['_method'] == "Update":
                if VetsAPI.put(self, id):
                    flash("Success, Vet is updated!")
                else:
                    flash("Fail, Vet is not updated!")
                next_page = request.args.get("next", url_for("home_page"))
                return redirect(next_page)
            else:
                abort(405)

        def get(self, id):
            u = Vets.get(id=id)
            if u:
                vet = u.__dict__
                return vet
            return {}, 404

        def put(self, id):
            if current_user.is_admin:
                args = self.parser.parse_args()
                u = Vets.get(id=id)
                if u and args:
                    u.update(**args)
                    return u.__dict__
            else:
                abort(403)
            return {}, 404

        def delete(self, id):
            if current_user.is_admin:
                u = Vets.get(id=id)
                if u:
                    r = u.__dict__
                    u.delete()
                    return r, 200
            else:
                abort(403)


    class VetsListAPI(Resource):
        method_decorators = [login_required]

        def __init__(self):
            self.parser = reqparse.RequestParser()
            self.parser.add_argument('name', type=str)
            self.parser.add_argument('age', type=str)
            self.parser.add_argument('address', type=str)
            self.parser.add_argument('gender', type=str)
            self.parser.add_argument('profession', type=str)

        def get(self):
            if current_user.is_admin:
                qs = Vets.filter()
                if qs:
                    r = [u.__dict__ for u in qs]
                    return r
            else:
                abort(403)
            abort(404)

        def post(self):
            args = self.parser.parse_args()
            if args:
                if Vets.create(**args):
                    vet = Vets.filter(**args).__getitem__(0)
                    flash('You were successfully created Vet!')
                    next_page = request.args.get("next", url_for("home_page"))
                    return redirect(next_page)
                else:
                    flash('You were failed to create Vet!')
                    next_page = request.args.get("next", url_for("home_page"))
                    return redirect(next_page)
            return {}, 404

