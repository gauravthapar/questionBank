import datetime
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from . models import Student, QuestionPaper

class SignupForm(UserCreationForm):
    username = forms.CharField(max_length=30)
    email=forms.EmailField(max_length=200)

    class Meta:
        model = User
        fields = ['username','email','password1','password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError('email already registered')
        return email


class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        exclude = ['user']


class QuestionPaperForm(forms.Form):
    YEAR_CHOICES = [(r,r) for r in range(2005, datetime.date.today().year+1)]
    EXAM_TYPE = (
        ('Minor-1','Minor-1'),
        ('Minor-2','Minor-2'),
        ('Major','Major')
    )
    File = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    subjectName = forms.CharField(max_length=30)
    subjectCode = forms.CharField(max_length=30)
    year = forms.TypedChoiceField(choices=YEAR_CHOICES)  
    examType = forms.TypedChoiceField(choices=EXAM_TYPE)
    
    


    
    