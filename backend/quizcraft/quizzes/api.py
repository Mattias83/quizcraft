from ninja import NinjaAPI
from django.shortcuts import get_object_or_404
from django.db import transaction
from quizzes.models import Quiz, Question, Answer
from quizzes.schemas import (
    QuizSchema,
    QuizCreateSchema,
    QuizUpdateSchema,
    QuestionSchema,
    AnswerSchema,
)
from typing import List

api = NinjaAPI()


# List all quizzes
@api.get("/quizzes", response=List[QuizSchema])
def list_quizzes(request):
    quizzes = (
        Quiz.objects.prefetch_related("questions__answers")
        .select_related("creator")
        .all()
    )
    return quizzes


# Retrieve a specific quiz
@api.get("/quizzes/{quiz_id}", response=QuizSchema)
def get_quiz(request, quiz_id: str):
    quiz = get_object_or_404(
        Quiz.objects.prefetch_related("questions__answers").select_related(
            "creator"
        ),
        id=quiz_id,
    )
    return quiz


# Create a new quiz
@api.post("/quizzes", response=QuizSchema)
def create_quiz(request, payload: QuizCreateSchema):
    with transaction.atomic():
        quiz = Quiz.objects.create(
            name=payload.name,
            description=payload.description,
            image=payload.image,
            creator=request.user,
            is_public=payload.is_public,
        )
    return quiz


# Update an existing quiz
@api.put("/quizzes/{quiz_id}", response=QuizSchema)
def update_quiz(request, quiz_id: str, payload: QuizUpdateSchema):
    quiz = get_object_or_404(Quiz, id=quiz_id, creator=request.user)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(quiz, attr, value)
    quiz.save()
    return quiz


# Delete a quiz
@api.delete("/quizzes/{quiz_id}", response={204: None})
def delete_quiz(request, quiz_id: str):
    quiz = get_object_or_404(Quiz, id=quiz_id, creator=request.user)
    quiz.delete()
    return 204


# Add questions to a quiz
@api.post("/quizzes/{quiz_id}/questions", response=QuestionSchema)
def add_question(request, quiz_id: str, payload: QuestionSchema):
    quiz = get_object_or_404(Quiz, id=quiz_id, creator=request.user)
    with transaction.atomic():
        question = Question.objects.create(
            quiz=quiz,
            text=payload.text,
            image=payload.image,
            order=payload.order,
        )
        for answer_data in payload.answers:
            Answer.objects.create(
                question=question,
                text=answer_data.text,
                is_correct=answer_data.is_correct,
            )
    return question


# Retrieve questions for a specific quiz
@api.get("/quizzes/{quiz_id}/questions", response=List[QuestionSchema])
def list_questions(request, quiz_id: str):
    quiz = get_object_or_404(
        Quiz.objects.prefetch_related("questions__answers"), id=quiz_id
    )
    return quiz.questions.all()
