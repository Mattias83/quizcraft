from ninja import Schema
from typing import List, Optional
from uuid import UUID
from datetime import datetime


class UserSchema(Schema):
    id: int
    username: str


class AnswerSchema(Schema):
    id: int
    text: str
    is_correct: bool


class QuestionSchema(Schema):
    id: int
    text: str
    image: Optional[str]
    order: int
    answers: List[AnswerSchema]


class QuizCreateSchema(Schema):
    name: str
    description: Optional[str]
    image: Optional[str]
    is_public: bool


class QuizUpdateSchema(Schema):
    name: Optional[str]
    description: Optional[str]
    image: Optional[str]
    is_public: Optional[bool]


class QuizSchema(Schema):
    id: UUID
    name: str
    description: Optional[str]
    image: Optional[str]
    creator: UserSchema
    created_at: datetime
    updated_at: datetime
    is_public: bool
    questions: List[QuestionSchema]
