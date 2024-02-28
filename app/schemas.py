from marshmallow import Schema, fields


class PlainUserSchema(Schema):
    #id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    u_email = fields.Email(required=True)
    # Never return password
    password = fields.Str(required=True, load_only=True)


class PlainEmailSchema(Schema):
    id = fields.Int(dump_only=True)
    subject = fields.Str(required=True)
    body = fields.Str(required=True)
    timestamp = fields.DateTime()
    sender_id = fields.Int(required=True)
    recipient_id = fields.Int(required=True)

class EmailFormSchema(Schema):
    subject = fields.Str(required=True)
    timestamp = fields.DateTime()
    body = fields.Str(required=True)
    recipient_email = fields.Email(required=True)

class UserLoginSchema(Schema):
    u_email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)


class EmailSchema(PlainEmailSchema):
    sender = fields.Nested(PlainUserSchema(), dump_only=True)
    #recipient = fields.Nested(PlainUserSchema(), dump_only=True)


class UserSchema(PlainUserSchema):
    received_emails = fields.List(fields.Nested(PlainEmailSchema()), dump_only=True)
    sent_emails = fields.List(fields.Nested(PlainEmailSchema()), dump_only=True)


