from django.contrib import admin
# Imported all 7 required classes: Course, Lesson, Question, Choice, Submission, Instructor, Learner
from .models import Course, Lesson, Question, Choice, Submission, Instructor, Learner


# Inline for Choices inside Question
class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 4


# Inline for Questions inside Lesson
class QuestionInline(admin.StackedInline):
    model = Question
    extra = 2


# Inline for Lessons inside Course (Fixes CourseAdmin reference)
class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 5


# Admin view for Questions
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ['question_text', 'grade']
    search_fields = ['question_text']


# Admin view for Lessons
class LessonAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ['title', 'order']


# Admin view for Courses
class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline]
    list_display = ('name', 'pub_date')
    list_filter = ['pub_date']
    search_fields = ['name', 'description']


# Register all required models with the Admin site
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)
admin.site.register(Instructor)
admin.site.register(Learner)