from flask_restful import Resource, reqparse
import sqlite3
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field is required and can't left empty"
                        )

    def post(self, username):
        user = UserModel.get_by_username(username)
        if user is not None:
            return {"message": "Username is already used and it MUST be unique!"}, 404

        data = UserRegister.parser.parse_args()
        new_user = UserModel(username, data['password'])

        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # insert_query = "INSERT INTO users VALUES (NULL, ?, ?)"
        # cursor.execute(insert_query, new_user)
        #
        # connection.commit()
        # connection.close()

        new_user.save_to_db()
        return {'message': "User successfully created"}, 201

    def delete(self, username):
        user = UserModel.get_by_username(username)
        if user is None:
            return {"message": "User not found!"}

        user.delete_from_db()
        return {"message": "User successfully deleted!"}


