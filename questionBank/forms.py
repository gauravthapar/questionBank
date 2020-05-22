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


class QuestionPaperForm(ModelForm):
    class Meta:
        model = QuestionPaper
        fields = '__all__'


    
    