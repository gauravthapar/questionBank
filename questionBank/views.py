from django.shortcuts import render , redirect
from django.http import HttpResponse
from . forms import SignupForm, StudentForm, QuestionPaperForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from . models import QuestionPaper, Student, Feedback, QuestionPaperDetail
from django.db.models import Q
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from . decorators import unauthenticated_user

# Create your views here.


@unauthenticated_user
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



@login_required(login_url="loginuser")
def home(request):
    questionPapers = QuestionPaper.objects.all()
    name = questionPapers[0].details.subjectName
    print(name)
    context = {
        'questionPapers':questionPapers,
    }
    return render(request,'questionBank/dashboard.html',context)


@login_required(login_url="loginuser")
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


@unauthenticated_user
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


@login_required(login_url="loginuser")
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


@login_required(login_url="loginuser")
def uploadPage(request):
    form = QuestionPaperForm()
    if request.method == "POST":
        form = QuestionPaperForm(request.POST, request.FILES)
        File1 = request.FILES.get('File1')
        #File2 = request.FILES.get('File2')
        subjectCode = request.POST.get('subjectCode')
        subjectName = request.POST.get('subjectName')
        year = request.POST.get('year')
        examType = request.POST.get('examType')
        paper_qs = None
        print(paper_qs)
        print(File1,subjectCode,subjectName,year,examType)
        #paper_qs  = QuestionPaper.objects.all().filter(subjectCode=subjectCode,subjectName=subjectName,year=year,examType=examType)
        paper = QuestionPaperDetail(
            subjectName=subjectName,
            subjectCode=subjectCode,
            year=year,
            examType=examType
        )
        paper.save()
        paper_file1= QuestionPaper(
            File=File1,
            details=paper
        )
        paper_file1.save()
        '''paper_file2 = QuestionPaper(
            File=File2,
            details=paper
        )
        paper_file2.save()'''
        '''if form.is_valid():
            if paper_qs.exists():
                #raise forms.ValidationError('already exists')
                print('already exists')
            else:
                print('saved')
                form.save()'''
            #return redirect('home')
    context = {
        'form':form
    }
    return render(request, 'questionBank/upload.html', context)


def update(request, pk):
    papers = QuestionPaper.objects.get(id=pk)
    print(papers.details.subjectName)
    print(papers.details.subjectCode)
    print(papers.File)
    context = {
        'papers':papers,
    }
    return render(request,'questionBank/update.html',context)



@login_required(login_url="loginuser")
def contactPage(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        student = request.user.student
        feedback = Feedback(
            student=student,
            name=name,
            email=email,
            message=message
        )
        feedback.save()
        template = render_to_string('questionBank/feedback_template.html',{'name':request.user.student.name})
        email = EmailMessage(
            'Thanks for your feedback',
            template,
            settings.EMAIL_HOST_USER,
            [request.user.email],
        )
        email.fail_silently =False
        email.send()
    return render(request, 'questionBank/contact.html')


def logoutuser(request):
    if request.method == "POST":
        logout(request)
        return redirect('loginuser')

