from django.contrib import admin
from . models import Student, QuestionPaper, Feedback
# Register your models here.

admin.site.register(Student)
admin.site.register(QuestionPaper)
admin.site.register(Feedback)