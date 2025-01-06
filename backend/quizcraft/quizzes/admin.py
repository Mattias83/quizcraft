from django.contrib import admin
from .models import Quiz, Question, Answer


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("name", "creator", "is_public", "created_at", "updated_at")
    search_fields = ("name", "description", "creator__username")
    list_filter = ("is_public", "created_at", "updated_at")
    filter_horizontal = ("invited_users",)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "quiz", "order")
    search_fields = ("text", "quiz__name")
    list_filter = ("quiz",)
    ordering = ("quiz", "order")


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("text", "question", "is_correct")
    search_fields = ("text", "question__text")
    list_filter = ("is_correct",)
