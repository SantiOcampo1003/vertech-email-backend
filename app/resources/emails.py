from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..schemas import EmailFormSchema
from ..models.email import EmailModel
from sqlalchemy.exc import SQLAlchemyError
from ..models.user import UserModel


blp = Blueprint("emails", __name__, description="Operation on emails")


@blp.route("/api/emails")
class Email(MethodView):
    @jwt_required()
    @blp.arguments(EmailFormSchema)
    @blp.response(201, EmailFormSchema)
    def post(self, email_data):
        current_user_id = get_jwt_identity()
        recipient = UserModel.query.filter(
            UserModel.u_email == email_data["recipient_email"]
        ).first()

        email = EmailModel(sender_id=current_user_id,
                           recipient_id=recipient.id , body=email_data["body"], subject=email_data["subject"])
        
        try:
            email.save_to_db()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the comment.")

       