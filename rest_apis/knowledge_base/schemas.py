from marshmallow import Schema, fields
from dataclasses import dataclass
from typing import Optional


@dataclass
class KBQuery:
    content: str
    k: Optional[int] = None
    cross_encoder_input_k: Optional[int] = None


class QuestionSchema(Schema):
    user_question = fields.Str(required=True)
    k = fields.Int()
    sender = fields.Str()
    time_tag = fields.DateTime()

question_schema = QuestionSchema()


class KBQuerySchema(Schema):
    content = fields.Str(required=True, error_messages={'required': 'content field is required.'})
    k = fields.Int(error_messages={'validator_failed': 'k field must be an integer.'})
    cross_encoder_input_k = fields.Int(error_messages={'validator_failed': 'k field must be an integer.'})
# If content is not there, error will be thrown since it is required.
# If a new field is there, error will be thrown during load.

kb_query_schema = KBQuerySchema()


# Following schemas will be used for dump. If the fields are not there it is no problem for dump.
class RetrievalInfoSchema(Schema):
    q = fields.Str()
    dist = fields.Float()
    token_len = fields.Int()
    # for some type of docs there will be also:
    cross_encoder_score = fields.Float()


class MetadataSchema(Schema):
    source = fields.Str()
    page = fields.Int()
    retrieval_info = fields.Nested(RetrievalInfoSchema())
    answer = fields.Str()
    # for some type of docs there will be also:
    doc_index = fields.Int()
    page_summary = fields.Str()


class DocSchema(Schema):
    page_content = fields.Str()
    metadata = fields.Nested(MetadataSchema())


doc_schema = DocSchema()