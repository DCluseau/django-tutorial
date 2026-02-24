from django.contrib import admin

from .models import Question
from .models import Choice

class QuestionAdmin(admin.ModelAdmin):
    list_display = ["question_text", "pub_date"]
    list_filter = ["question_text", "pub_date"]
    ordering = ["-pub_date", "question_text"]
    search_fields = ["question_text", "pub_date"]
    pass
admin.site.register(Question, QuestionAdmin)

class ChoiceAdmin(admin.ModelAdmin):
    list_display = ["question", "choice_text", "votes"]
    list_filter = ["question", "choice_text", "votes"]
    ordering = ["question", "choice_text", "votes"]
    search_fields = ["choice_text", "votes", "foreign_key__related_fieldname"]
    pass
admin.site.register(Choice, ChoiceAdmin)

