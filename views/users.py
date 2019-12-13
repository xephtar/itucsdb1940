from models.users import Users


def get_user(user_id):
    u = Users.get(username=user_id)
    print(u.username)
    password = u.password
    print(password)
    if u:
        return u
    return None
