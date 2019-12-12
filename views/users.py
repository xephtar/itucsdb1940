from models.users import Users


PASSWORDS = {
    "admin": "$pbkdf2-sha256$29000$15rTmnMOIaQ0xhhjLGUMgQ$aIT92svRQOP.sQ8lX6WHzBu5JRRgiXwcJtWRLJzu4D8",
    "normaluser": '$pbkdf2-sha256$29000$Umqt9R4DAMB4733P.V/r/Q$B5KvyqisOFVOiJySv.PjXsot7xTU5KcrST7ml2jdoXU',
}

ADMIN_USERS = ["admin"]


def get_user(user_id):
    u = Users.get(username=user_id)
    print(u)
    user = Users(user_id, u[2]) if u[2] else None
    return user
