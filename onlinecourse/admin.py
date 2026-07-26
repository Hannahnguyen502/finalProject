from django.contrib import admin
# Importing seven model classes as required by the lab criteria
from .models import Course, Lesson, Instructor, Learner, Question, Choice, Submission


# QuestionInline class to embed Questions within LessonAdmin
class QuestionInline(admin.StackedInline):
    model = Question
    extra = 5


# ChoiceInline class to embed Choices within QuestionAdmin
class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 4


# QuestionAdmin class to manage Questions with Choices inline
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ['question_text', 'grade']
    search_fields = ['question_text']


# LessonAdmin class to manage Lessons with Questions inline
class LessonAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ['title', 'order']


# CourseAdmin class to manage Course display
class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline] if 'LessonInline' in globals() else []
    list_display = ('name', 'pub_date')
    list_filter = ['pub_date']
    search_fields = ['name', 'description']


# Register models with their custom Admin interfaces
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)
admin.site.register(Instructor)
admin.site.register(Learner)
