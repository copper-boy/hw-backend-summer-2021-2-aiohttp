from marshmallow import Schema, fields


class AdminSchema(Schema):
    id = fields.Integer(required=False)
    email = fields.Str(required=True)
    password = fields.Str(required=True)


class AdminRequestSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)


class AdminResponseSchema(Schema):
    id = fields.Integer(required=True)
    email = fields.Str(required=True)


