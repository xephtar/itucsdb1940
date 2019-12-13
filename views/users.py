from models.users import Users


def get_user(user_id):
    u = Users.get(username=user_id)
    if u:
        user = Users(user_id, u[2]) if u[2] else None
        return user
    return None
