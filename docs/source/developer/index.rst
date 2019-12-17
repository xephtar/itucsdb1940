Developer Guide
===============

Database Design
---------------

I have four tables. One is a relational table.

    .. figure:: er.png
        :scale: 100 %
        :alt: er diagram

        E/R Diagram

Code
----

**The server.py to run app**::

    .. code-block:: python
    from flask import Flask
    from flask_restful import Api
    from models.users import Users
    from views.vets import VetsAPI, VetsListAPI
    from views.vets_to_owners import VetsOwnersList, VetsOwners
    from views.owners import OwnersAPI, OwnersListAPI
    from views.url import owner_register, vet_register, home_page, vet_profile, vet_profiles, owner_profile, owner_profiles, relations
    import secrets
    from flask_login import LoginManager, confirm_login
    from views.login import login_page, logout_page, register_page


    lm = LoginManager()


    @lm.user_loader
    def load_user(user_id):
        reg_user = Users.get(username=user_id)
        if reg_user:
            if user_id == reg_user.get_id():
                return reg_user
        return None


    app = Flask(__name__, template_folder='template')
    app.secret_key = secrets.token_urlsafe(16)
    app.url_map.strict_slashes = False
    api = Api(app)
    lm.init_app(app)
    lm.login_view = "login_page"


    @app.before_request
    def before_request():
        confirm_login()


    api.add_resource(VetsOwners, '/relation/<int:vet_id>')
    api.add_resource(VetsOwnersList, '/relation/')
    api.add_resource(VetsAPI, '/vets/<int:id>')
    api.add_resource(VetsListAPI, '/vets/')
    api.add_resource(OwnersAPI, '/owners/<phonenumber>')
    api.add_resource(OwnersListAPI, '/owners/')
    app.add_url_rule("/profile/relations/", view_func=relations, methods=["GET"])
    app.add_url_rule("/profile/vet/<int:id>", view_func=vet_profile, methods=["GET"])
    app.add_url_rule("/profile/vets/", view_func=vet_profiles, methods=["GET"])
    app.add_url_rule("/profile/owner/<phonenumber>", view_func=owner_profile, methods=["GET"])
    app.add_url_rule("/profile/owners/", view_func=owner_profiles, methods=["GET"])
    app.add_url_rule("/owner_register/", view_func=owner_register, methods=["GET"])
    app.add_url_rule("/vet_register/", view_func=vet_register, methods=["GET"])
    app.add_url_rule("/", view_func=home_page)
    app.add_url_rule("/login", view_func=login_page, methods=["GET", "POST"])
    app.add_url_rule("/register", view_func=register_page, methods=["GET", "POST"])
    app.add_url_rule("/logout", view_func=logout_page, methods=["GET"])

    if __name__ == '__main__':
        app.run(debug=False)

**I have database client**::

    .. code-block:: python
    import os
    import psycopg2 as db


    class Client(object):

        def __init__(self):
            self.dsn = 'postgres://sxmxcsbbhbitaq:374c6268b10c0d0181454a0dc010c322b7dfe53e173b05e7cfdd64ee5d7e042d@ec2-54-217-234-157.eu-west-1.compute.amazonaws.com:5432/det2ikhqat3u6m'
            self.connection = db.connect(self.dsn)
            self.cursor = self.connection.cursor()

        def query(self, statement, params=None):
            try:
                self.cursor.execute(statement, params)
                self.connection.commit()
            except:
                self.connection.rollback()
                raise

        def fetch(self, statement, params=None):
            try:
                self.cursor.execute(statement, params)
                self.connection.commit()
                return self.cursor.fetchall()
            except:
                self.connection.rollback()
                raise

        def create(self, statement, params=None):
            try:
                self.cursor.execute(statement, params)
                self.connection.commit()
            except Exception as err:
                self.connection.rollback()
                return '{}'.format(err)

        def __del__(self):
            self.connection.close()
            self.cursor.close()


    db_client = Client()

I have base template and others extend from it.

    .. figure:: jinja.png
        :scale: 100 %
        :alt: jinja example

        Template Example

I have models and views to route endpoints.

.. toctree::

   vet
   owner
   relation
   user
   
