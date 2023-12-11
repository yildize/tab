from marshmallow import Schema, fields, validates_schema, ValidationError
from dataclasses import dataclass
from typing import Optional


@dataclass
class AnswerFeedback:
    is_rag: bool
    is_liked: bool
    user_question: str

    matched_question: Optional[str] = None
    matched_answer: Optional[str] = None
    suggested_answer: Optional[str] = None

    rag_answer: Optional[str] = None
    sources: Optional[str] = None


class AnswerFeedbackSchema(Schema):

    is_rag = fields.Bool(required=True, error_messages={'required': 'is_rag:bool field is required.'})
    is_liked = fields.Bool(required=True, error_messages={'required': 'is_liked:bool field is required.'})
    user_question = fields.Str(required=True, error_messages={'required': 'user_question:str field is required.'})

    matched_question = fields.Str()
    matched_answer = fields.Str()
    suggested_answer = fields.Str()

    rag_answer = fields.Str()
    sources = fields.Str()

    @validates_schema
    def validate_feedback_type(self, data, **kwargs):
        if data.get('is_rag'):
            if data.get('rag_answer') is None:
                raise ValidationError('rag_answer is required for rag feedbacks')
            if data.get('sources') is None:
                raise ValidationError('sources is required for rag feedbacks')
        else:
            if data.get('matched_question') is None:
                raise ValidationError('matched_question is required for non-rag feedbacks')
            if data.get('matched_answer') is None:
                raise ValidationError('matched_answer is required for non-rag feedbacks')


answer_feedback_schema = AnswerFeedbackSchema()