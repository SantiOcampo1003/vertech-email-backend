from ..database.db import db

class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=False)
    u_email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)

    sent_emails = db.relationship("EmailModel", back_populates="sender", lazy="dynamic")
    received_emails = db.relationship("EmailModel", back_populates="recipient", lazy="dynamic")

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.u_email,
            "received_emails": self.received_emails,
            "sent_emails": self.sent_emails
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()