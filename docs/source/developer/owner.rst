Parts Implemented by Ömer Faruk Davarcı
=======================================

Owner
-----

**Owner Model**::

    .. code-block:: python
    from client.db_client import db_client


    class Owners:
        sql_fields = [
            'age character varying(2) COLLATE pg_catalog."default"',
            'name text COLLATE pg_catalog."default"',
            '"phonenumber" character varying(10) COLLATE pg_catalog."default" NOT NULL',
            "id integer NOT NULL DEFAULT nextval('owners_id_seq'::regclass)",
            'address character varying COLLATE pg_catalog."default"',
            'gender character varying COLLATE pg_catalog."default"',
            'treatments character varying COLLATE pg_catalog."default"',
            'CONSTRAINT owners_pkey PRIMARY KEY ("phonenumber")',
            'CONSTRAINT owners_unique UNIQUE ("phonenumber")'
        ]

        sql_field_number = len(sql_fields)

        def __init__(self, age=None, name=None, phonenumber=None, id=None, address=None, gender=None, treatments=None):
            self.id = id
            self.name = name
            self.age = age
            self.phonenumber = phonenumber
            self.address = address
            self.treatments = treatments
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
                    "{key}=%s".format(key='phonenumber'),
                    "{key}=%s".format(key='address'),
                    "{key}=%s".format(key='treatments'),
                    "{key}=%s".format(key='gender'),
                ])
                exp = '''UPDATE {table_name} SET {values} WHERE id=%s RETURNING id'''.format(
                    table_name=self.__class__.__name__.lower(),
                    values=update_set,
                )
                self.id = db_client.fetch(exp, (self.name, self.age,
                                                self.phonenumber, self.address,
                                                self.gender, self.treatments,
                                                self.id))[0][0]
            else:
                exp = '''INSERT INTO {table_name} ({table_fields}) VALUES ({values})'''.format(
                    table_name=self.__class__.__name__.lower(),
                    table_fields=','.join([
                        '{}'.format('age'),
                        '{}'.format('name'),
                        '{}'.format('phonenumber'),
                        '{}'.format('address'),
                        '{}'.format('gender'),
                        '{}'.format('treatments')
                    ]),
                    values=','.join(['%s', '%s', '%s', '%s', '%s', '%s'])
                )
                c = db_client.create(exp, (self.age, self.name, self.phonenumber, self.address, self.gender, self.treatments))
                if c:
                    return c

            return self

        def delete(self, **kwargs):
            set_params = []
            set_values = []

            for key, value in kwargs.items():
                set_params.append("{}=%s".format(key))
                set_values.append(value)

            exp = '''DELETE FROM {table_name} WHERE phonenumber=%s'''.format(
                table_name=self.__class__.__name__.lower(),
            )
            set_values.append(self.phonenumber)
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
                exp = '''SELECT * FROM {table_name} ORDER BY name'''.format(
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



**Owner View**::

    .. code-block:: python
    from flask_login import login_required, current_user
    from flask_restful import reqparse, Resource, abort
    from flask import redirect, flash, request, url_for
    from models.owners import Owners


    class OwnersAPI(Resource):
        method_decorators = [login_required]

        def __init__(self):
            self.parser = reqparse.RequestParser()
            self.parser.add_argument('name', type=str)
            self.parser.add_argument('age', type=str)
            self.parser.add_argument('address', type=str)
            self.parser.add_argument('gender', type=str)
            self.parser.add_argument('treatments', type=str)

        def post(self, phonenumber):
            method = reqparse.RequestParser()
            method.add_argument('_method', type=str)
            method = method.parse_args()
            if method['_method'] == "Delete":
                if OwnersAPI.delete(self, phonenumber):
                    flash("Success, Owner is deleted!")
                else:
                    flash("Fail, Owner is not deleted!")
                next_page = request.args.get("next", url_for("home_page"))
                return redirect(next_page)
            elif method['_method'] == "Update":
                if OwnersAPI.put(self, phonenumber):
                    flash("Success, Owner is updated!")
                else:
                    flash("Fail, Owner is not updated!")
                next_page = request.args.get("next", url_for("home_page"))
                return redirect(next_page)
            else:
                abort(405)

        def get(self, phonenumber):
            u = Owners.get(phonenumber=phonenumber)
            if u:
                owner = u.__dict__
                return owner
            return {}, 404

        def put(self, phonenumber):
            if current_user.is_admin:
                args = self.parser.parse_args()
                u = Owners.get(phonenumber=phonenumber)
                if u and args:
                    u.update(**args)
                    return u.__dict__
            else:
                abort(403)
            return {}, 404

        def delete(self, phonenumber):
            if current_user.is_admin:
                u = Owners.get(phonenumber=phonenumber)
                if u:
                    r = u.__dict__
                    u.delete()
                    return r, 200
            else:
                abort(403)


    class OwnersListAPI(Resource):
        method_decorators = [login_required]

        def __init__(self):
            self.parser = reqparse.RequestParser()
            self.parser.add_argument('age', type=str)
            self.parser.add_argument('name', type=str)
            self.parser.add_argument('phonenumber', type=str)
            self.parser.add_argument('gender', type=str)
            self.parser.add_argument('address', type=str)
            self.parser.add_argument('treatments', type=str)

        def get(self):
            qs = Owners.filter()
            if qs:
                r = [u.__dict__ for u in qs]
                return r
            return {}, 404

        def post(self):
            args = self.parser.parse_args()
            if args:
                u = Owners.create(**args)
                if type(u) is str:
                    flash(u)
                    next_page = request.args.get("next", url_for("home_page"))
                    return redirect(next_page)
                else:
                    flash('You were successfully created Owner!')
                    next_page = request.args.get("next", url_for("home_page"))
                    return redirect(next_page)
            return {}, 404
