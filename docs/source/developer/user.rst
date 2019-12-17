Parts Implemented by Ömer Faruk Davarcı
=======================================

User
----

**User Model**::

    .. code-block:: python
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


**To Login and Register Login and User View**::

    .. code-block:: python
    from flask_restful import reqparse
    from wtforms import StringField, PasswordField
    from wtforms.validators import DataRequired
    from flask_wtf import FlaskForm
    from flask_login import logout_user, login_user
    from passlib.hash import pbkdf2_sha256 as hasher
    from flask import flash, url_for, redirect, request, render_template
    from views.users import get_user
    from models.users import Users


    class LoginForm(FlaskForm):
        username = StringField("Username", validators=[DataRequired()])
        password = PasswordField("Password", validators=[DataRequired()])


    class RegisterForm(FlaskForm):
        username = StringField("Username", validators=[DataRequired()])
        password = PasswordField("Password", validators=[DataRequired()])


    def login_page():
        form = LoginForm()
        if request.method == "POST":
            if form.validate_on_submit():
                username = form.data["username"]
                user = get_user(username)
                if user is not None:
                    password = form.data["password"]
                    if hasher.verify(password, user.password):
                        login_user(user, remember=True)
                        flash("You have logged in.")
                        next_page = request.args.get("next", url_for("home_page"))
                        return redirect(next_page)
                flash("Invalid credentials.")
        return render_template("login.html", form=form)


    def register_page():
        form = RegisterForm()
        if request.method == "POST":
            if form.validate_on_submit():
                username = form.data["username"]
                user = get_user(username)
                if user is None:
                    parser = reqparse.RequestParser()
                    parser.add_argument('username', type=str)
                    parser.add_argument('password', type=str)
                    parser.add_argument('is_admin', type=bool)
                    parser.add_argument('active', type=bool)
                    args = parser.parse_args()
                    u = Users.create(**args)
                    print(u)
                    print(type(u))
                    flash("You have signed up!")
                    next_page = request.args.get("next", url_for("home_page"))
                    return redirect(next_page)
                flash("Already exist username.")
        return render_template("register.html", form=form)


    def logout_page():
        if request.method == "GET":
            logout_user()
            flash("You have logged out.")
            return redirect(url_for("home_page"))


**Users View To Just Get User Property**::

    .. code-block:: python

    from models.users import Users

    def get_user(user_id):
        u = Users.get(username=user_id)
        if u:
            return u
        return None
