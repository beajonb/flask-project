from werkzeug.security import safe_str_cmp
from models.user import UserModel

####################################################################
# This is an alternate approach to authenticate with in-memory user
####################################################################
# users = [
#     User(1, 'Rodlf', 'asdfg')
# ]
#
# username_mapping = {u.username: u for u in users}
# userid_mapping = {u.id: u for u in users}
#
#
# def authenticate(username, password):
#     user = username_mapping.get(username, None)
#     if user and safe_str_cmp(user.password, password):
#         return user
#
#
# def identity(payload):
#     user_id = payload['identity']
#     return userid_mapping.get(user_id, None)


####################################################################
# This is authentication approach with database in use
####################################################################
def authenticate(username, password):
    user = UserModel.get_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return UserModel.get_by_id(user_id)
