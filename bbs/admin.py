from django.contrib import admin

# Register your models here.

from .models import Question
from .models import Choice


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    # fields = ['pub_date', 'question_text'],

    fieldsets = [
        ('Fieldset1', {'fields': ['question_text']}),
        ('Fieldset2', {'fields': ['pub_date']}),
    ]

    inlines = [ChoiceInline]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)

