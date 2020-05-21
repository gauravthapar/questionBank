from django.shortcuts import render , redirect
from django.http import HttpResponse
from . forms import SignupForm, StudentForm, QuestionPaperForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from . models import QuestionPaper
from . filters import QuestionpaperFilter
from django.db.models import Q
# Create your views here.

def home(request):
    questionPapers = QuestionPaper.objects.all()
    context = {
        'questionPapers':questionPapers,
    }
    return render(request,'questionBank/dashboard.html',context)


def signupuser(request):
    form = SignupForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            messages.success(request,'Account created successfully for '+ username)
            return redirect('loginuser')
        else:
            context = {
                'form':form,
                'error':form.errors
            }
            print(context['error'])
            return render(request, 'questionBank/signupuser.html',context)
    else:
        context = {
            'form':form
        }
        return render(request, 'questionBank/signupuser.html', context)


def searchResult(request):
    questionPapers = None
    query = None
    if 'q' in request.GET:
        query = request.GET.get('q')
        questionPapers = QuestionPaper.objects.all().filter(Q(subjectName__icontains=query) | Q(subjectCode__icontains=query) | Q(year__icontains=query) |Q(examType__icontains=query))
    context = {
        'questionPapers':questionPapers,
        'query':query,
    }
    return render(request, 'questionBank/search.html',context)

def loginuser(request):
    if request.method == "POST":
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            context = {
                'form': AuthenticationForm(),
                'error': 'username and password does not match' 
            }
            return render(request,'questionBank/loginuser.html', context)
        else:
            login(request,user)
            return redirect('home')
    else:
        context = {
            'form': AuthenticationForm(),
        }
        return render(request,'questionBank/loginuser.html',context)


def studentProfile(request):
    student = request.user.student
    form = StudentForm(instance=student)
    if request.method == "POST":
        form = StudentForm(request.POST,instance=student)
        if form.is_valid():
            form.save()
            messages.success(request,'Profile updated successfully')
    context = {
        'form':form,
    }
    return render(request, 'questionBank/profile.html',context)


def uploadPage(request):
    form = QuestionPaperForm()
    if request.method == "POST":
        form = QuestionPaperForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {
        'form':form
    }
    return render(request, 'questionBank/upload.html', context)


def logoutuser(request):
    if request.method == "POST":
        logout(request)
        return redirect('loginuser')

