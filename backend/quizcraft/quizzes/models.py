from django.db import models
from django.contrib.auth.models import User


class Quiz(models.Model):
    title: str = models.CharField(max_length=255, verbose_name="Title")
    description: str = models.TextField(blank=True, verbose_name="Description")
    creator: User = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="quizzes",
        verbose_name="Creator",
    )
    is_public: bool = models.BooleanField(
        default=False, verbose_name="Public quiz"
    )
    created_at: models.DateTimeField = models.DateTimeField(
        auto_now_add=True, verbose_name="Created at"
    )

    def __str__(self) -> str:
        return self.title


class Question(models.Model):
    quiz: Quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name="questions",
        verbose_name="Quiz",
    )
    text: str = models.TextField(
        blank=False, null=False, verbose_name="Question text"
    )
    image: models.ImageField = models.ImageField(
        upload_to="question_images/",
        blank=True,
        null=True,
        verbose_name="Image",
    )

    def __str__(self) -> str:
        return self.text


class Answer(models.Model):
    question: Question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="answers",
        verbose_name="Question",
    )
    text: str = models.CharField(max_length=255, verbose_name="Answer text")
    is_correct: bool = models.BooleanField(
        default=False, verbose_name="Correct answer"
    )

    def __str__(self) -> str:
        return self.text
