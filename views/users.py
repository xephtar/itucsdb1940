from models.users import Users


def get_user(user_id):
    u = Users.get(username=user_id)
    if u:
        return u
    return None
