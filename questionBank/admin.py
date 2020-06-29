from django.contrib import admin
from . models import Student, QuestionPaperDetail, QuestionPaper, Feedback
# Register your models here.

admin.site.register(Student)
admin.site.register(QuestionPaper)
admin.site.register(QuestionPaperDetail)
admin.site.register(Feedback)