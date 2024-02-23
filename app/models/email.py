from app.database.db import db


class EmailModel(db.Model):
    __tablename__ = "emails"

    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.Text, nullable=False)
    body = db.Column(db.Text, nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=False, nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=False, nullable=False)
    sender = db.relationship("UserModel", foreign_keys=[sender_id], back_populates="sent_emails")
    recipient = db.relationship("UserModel", foreign_keys=[recipient_id], back_populates="received_emails")

    def json(self):
        return {
            "id": self.id,
            "body": self.body,
            "sender": self.sender,
            "recipient": self.recipient
        }

    @classmethod
    def find_all_sent_by_user(cls, id):
        return cls.query.filter_by(sender_id=id).all()

    @classmethod
    def find_all_received_by_user(cls, id):
        return cls.query.filter_by(recipient_id=id).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
