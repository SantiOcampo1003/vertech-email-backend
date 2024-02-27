from app.database.db import db


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=False, nullable=False)
    u_email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)

    sent_emails = db.relationship("EmailModel", back_populates="sender", foreign_keys="[EmailModel.sender_id]",
                                  lazy="dynamic")
    received_emails = db.relationship("EmailModel", back_populates="recipient",
                                      foreign_keys="[EmailModel.recipient_id]", lazy="dynamic")

    @classmethod
    def find_by_u_email(cls, email):
        return cls.query.filter_by(u_email=email).first()

    def json(self):
        return {
            "name": self.name,
            "u_email": self.u_email,
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
