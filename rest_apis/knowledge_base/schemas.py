from marshmallow import Schema, fields
from dataclasses import dataclass
from typing import Optional

@dataclass
class KBQuery:
    content: str
    k: Optional[int] = None


class KBQuerySchema(Schema):
    content = fields.Str(required=True, error_messages={'required': 'content field is required.'})
    k = fields.Int(error_messages={'validator_failed': 'k field must be an integer.'})

kb_query_schema = KBQuerySchema()


#
# class MetadataSchema(Schema):
#     source = fields.Str()
#     page = fields.Int()
#     retrieval_info = fields.Dict()
#
#
# class DocSchema(Schema):
#     page_content = fields.Str()
#     metadata = fields.Nested(MetadataSchema())
