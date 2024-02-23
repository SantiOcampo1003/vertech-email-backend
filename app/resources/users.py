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
            u_email=user_data["u_email"],
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


@blp.route("/api/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        # TODO: add class method find_by_username
        user = UserModel.query.filter(
            UserModel.u_email == user_data["u_email"]
        ).first()
        # user = UserModel.find_by_username(user_data["email"])

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True, expires_delta=timedelta(weeks=1))
            return {"access_token": access_token, "u_email": user.u_email}, 200

        abort(401, message="Invalid credentials.")
