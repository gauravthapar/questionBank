from django.contrib import admin
from . models import Student, QuestionPaperDetail, QuestionPaper, Feedback
import os
# Register your models here.

class QuestionPaperDetailAdmin(admin.ModelAdmin):
    list_display = ("id", "subjectName", "subjectCode", "year", "examType")
    search_fields = ("subjectName", "subjectCode", "year")
    list_filter = ("examType", "year",)
    list_display_links = ("subjectName",)

class QuestionPaperAdmin(admin.ModelAdmin):
    list_display = ("details_id", "subjectName", "subjectCode", "year", "examType", "file_extension")
    list_select_related = ("details",)
    list_filter = ("details__examType", "details__year",)
    search_fields = ("details__subjectName", "details__subjectCode", "details__year")
    list_display_links = ("details_id","subjectName",)

    def details_id(self, object):
        return object.details.id

    def subjectName(self, object):
        return object.details.subjectName
    
    def subjectCode(self, object):
        return object.details.subjectCode
    
    def year(self, object):
        return object.details.year

    def examType(self, object):
        return object.details.examType
    
    def file_extension(self, object):
        return os.path.splitext(object.File.name)[1]  

class StudentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "contact_no", "roll_no")
    search_fields = ("id", "name", "email", "contact_no", "roll_no")
    list_filter = ("Class",)
    list_display_links = ("name",)

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("student_id", "name", "email", "student_roll_no")
    list_select_related = ("student",)
    search_fields = ("student__id", "name", "email", "student__roll_no")
    list_filter = ("student__Class",)
    list_display_links = ("name",)

    def student_id(self, object):
        return object.student.id

    def student_roll_no(self, object):
        return object.student.roll_no

admin.site.register(Student, StudentAdmin)
admin.site.register(QuestionPaper, QuestionPaperAdmin)
admin.site.register(QuestionPaperDetail, QuestionPaperDetailAdmin)
admin.site.register(Feedback,FeedbackAdmin)