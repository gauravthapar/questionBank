from django.contrib import admin
from . models import Student, QuestionPaperDetail, QuestionPaper, Feedback
# Register your models here.

class QuestionPaperDetailAdmin(admin.ModelAdmin):
    list_display = ("id", "subjectName", "subjectCode", "year", "examType")
    search_fields = ("subjectName", "subjectCode", "year")
    list_filter = ("examType", "year",)
    list_display_links = ("subjectName",)

admin.site.register(Student)
admin.site.register(QuestionPaper)
admin.site.register(QuestionPaperDetail, QuestionPaperDetailAdmin)
admin.site.register(Feedback)