#schemas.py
from marshmallow import Schema, fields

class UserSch(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)

class CategorySch(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)

class RecordSch(Schema):
    id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    category_id = fields.Int(required=True)
    money_spent = fields.Float(required=True)

class AccountSch(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    balance = fields.Float()

class FundsSch(Schema):
    user_id = fields.Int(required=True)
    amount = fields.Float(required=True)