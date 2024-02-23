from marshmallow import Schema, fields
class PlainUserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True)
    # Never return password
    password = fields.Str(required=True, load_only=True)

class PlainEmailSchema(Schema):
    id = fields.Int(dump_only=True)
    subject = fields.Str(required=True)
    body = fields.Str(required=True)
    timestamp = fields.DateTime()
    sender_id = fields.Int(required=True)
    recipient_id = fields.Int(required=True)

class UserSchema(PlainUserSchema):
    emails = fields.List(fields.Nested(PlainEmailSchema()), dump_only=True)

