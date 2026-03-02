from django.contrib import admin
from .models import Choice
from .models import Question

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline]
    list_display = ["question_text", "pub_date", "was_published_recently"]
    list_filter = ["pub_date"]
    search_fields = ["question_text"]
    
admin.site.register(Question, QuestionAdmin)


# class ChoiceAdmin(admin.ModelAdmin):
#     list_display = ["question", "choice_text", "votes"]
#     list_filter = ["question", "choice_text", "votes"]
#     ordering = ["question", "choice_text", "votes"]
#     search_fields = ["choice_text", "votes", "foreign_key__related_fieldname"]
#     pass
# admin.site.register(Choice, ChoiceAdmin)

# admin.site.register(Choice)