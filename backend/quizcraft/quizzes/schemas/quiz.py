from typing import Optional, TYPE_CHECKING
from ninja import Schema


if TYPE_CHECKING:
    from quizzes.schemas.question import QuestionSchema


class QuizSchema(Schema):
    title: str
    description: str
    questions: list[QuestionSchema]


class QuizCreateSchema(Schema):
    title: str
    description: Optional[str] = None


class QuizUpdateSchema(Schema):
    title: Optional[str] = None
    description: Optional[str] = None
