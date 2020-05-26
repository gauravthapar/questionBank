from django.db import models
from django.contrib.auth.models import User
from phone_field import PhoneField

# Create your models here.

class Student(models.Model):
    CLASS = (
        ('B.Tech-CSE','B.Tech-CSE'),
        ('B.Tech-ECE','B.Tech-ECE'),
        ('B.Tech-ECSE','B.Tech-ECSE'),
        ('M.Tech-CSE','M.Tech-CSE'),
        ('M.Tech-ECE','M.Tech-ECE'),
        ('M.Tech-ECSE','M.Tech-ECSE'),
    )
    SEMESTER = (
        ('1','1'),
        ('2','2'),
        ('3','3'),
        ('4','4'),
        ('5','5'),
        ('6','6'),
        ('7','7'),
        ('8','8'),
    )
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length = 200, null=True)
    email = models.EmailField(null=True)
    contact_no = models.CharField(max_length=13,blank=True, help_text='contact phone number')
    Class = models.CharField(max_length=20, null=True, choices=CLASS)
    semester = models.CharField(max_length=5, null=True, choices=SEMESTER)
    roll_no = models.CharField(max_length=15, null=True)

    
    def __str__(self):
        return self.name
    

class QuestionPaperDetail(models.Model):
    EXAMTYPE = (
        ('Minor-1','Minor-1'),
        ('Minor-2','Minor-2'),
        ('Major','Major')
    )
    subjectName = models.CharField(max_length=100, null=True)
    subjectCode = models.CharField(max_length=15, null=True)
    year = models.CharField(max_length=4, null=True)
    examType = models.CharField(max_length=50, null=True, choices=EXAMTYPE)
    

    def __str__(self):
        return self.subjectName

    

class QuestionPaper(models.Model):
    File = models.FileField(null=True, blank=True)
    details = models.ForeignKey(QuestionPaperDetail, null=True, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)


    @property
    def fileURL(self):
        try:
            url = self.File.url
        except:
            url = ''
        return url


class Feedback(models.Model):
    student = models.ForeignKey(Student, null=True,blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True)
    message = models.TextField(null=True)
    
    def __str__(self):
        return self.name