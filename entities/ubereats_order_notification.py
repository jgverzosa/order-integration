from dataclasses import field
from email.mime import image
from json import load
from typing import List
from unicodedata import category
from marshmallow import Schema, fields, EXCLUDE, missing, pre_load


class MetaSchema(Schema):
    class Meta:
        unknown = EXCLUDE
    resource_id = fields.String(required=True)
    status = fields.String(required=True)
    user_id = fields.String(required=True)


class WebhookMeta(Schema):
    class Meta:
        unknown = EXCLUDE
    client_id = fields.String()
    webhook_config_id = fields.String()
    webhook_msg_timestamp = fields.Integer()
    webhook_msg_uuid = fields.String()


class OrderNotification(Schema):
    class Meta:
        unknown = EXCLUDE
    event_id = fields.String(required=True)
    event_time = fields.Integer()
    event_type = fields.String(required=True)
    meta = fields.Nested(MetaSchema)
    resource_href = fields.String(required=True)
    webhook_meta = fields.Nested(WebhookMeta)