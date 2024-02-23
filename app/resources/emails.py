from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..schemas import PlainEmailSchema
from ..models.email import EmailModel
from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint("emails", __name__, description="Operation on emails")


@blp.route("/api/emails/received")
class EmailReceivedList(MethodView):
    # Converts response into a list
    @jwt_required()
    @blp.response(200, PlainEmailSchema(many=True))
    def get(self):
        current_user = get_jwt_identity()
        return EmailModel.find_all_received_by_user(id=current_user)


@blp.route("/api/emails/sent")
class EmailSentList(MethodView):
    @jwt_required()
    @blp.response(200, PlainEmailSchema(many=True))
    def get(self):
        current_user = get_jwt_identity()
        return EmailModel.find_all_received_by_user(id=current_user)


@blp.route("/api/emails")
class Email(MethodView):
    @jwt_required(fresh=True)
    @blp.arguments(PlainEmailSchema)  # Adds API information to Swagger UI Docs
    @blp.response(201, PlainEmailSchema)
    def post(self, email_data):
        current_user = get_jwt_identity()
        # pass email data as keyword arguments
        # TODO: add check for recipient_id
        email = EmailModel(sender_id=current_user, **email_data)

        try:
            email.save_to_db()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the comment.")

        return email
