from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, create_refresh_token, get_jwt_identity
from datetime import timedelta
from ..models.user import UserModel
from ..schemas import UserSchema

from sqlalchemy.exc import IntegrityError

blp = Blueprint("users", __name__, description="Operations on users.")


@blp.route("/api/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel(
            name=user_data["name"],
            u_email=user_data["email"],
            password=pbkdf2_sha256.hash(user_data["password"])
        )
        try:
            user.save_to_db()

            return {"message": "User created successfully."}, 201
        except IntegrityError:
            abort(
                400,
                message="Username already exists."
            )
