from marshmallow import Schema, fields, validate
from dataclasses import dataclass
from typing import Optional


@dataclass
class RAGQuery:
    question: str
    k: Optional[int] = 5
    cross_encoder_input_k: Optional[int] = 20


class RagQuerySchema(Schema):
    question = fields.Str(required=True, error_messages={'required': 'question field is required.'})
    k = fields.Int(error_messages={'validator_failed': 'k field must be an integer.'})
    cross_encoder_input_k = fields.Int(validate=validate.Range(min=1, max=100), error_messages={'validator_failed': 'cross_encoder_input_k field must be an integer between 1 and 100.'})
# If content is not there, error will be thrown since it is required.
# If a new field is there, error will be thrown during load.


rag_query_schema = RagQuerySchema()


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
metadata_schema = MetadataSchema()