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
from . token_generator import account_verification_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.models import User
from django.core.paginator import Paginator

# Create your views here.


@unauthenticated_user
def signupuser(request):
    form = SignupForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('questionBank/account_verification.html',{
                'user':user,
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_verification_token.make_token(user),
            })
            email = EmailMessage(
                'Verify your Account',
                message,
                settings.EMAIL_HOST_USER,
                [form.cleaned_data.get('email')],
            )
            email.fail_silently = False
            email.send()
            return HttpResponse('We have sent you an email, please confirm your email address to continue')
        else:
            context = {
                'form':form,
                'error':form.errors
            }
            return render(request, 'questionBank/signupuser.html',context)
    else:
        context = {
            'form':form
        }
        return render(request, 'questionBank/signupuser.html', context)


def verify_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExists):
        user = None
    if user is not None and account_verification_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('loginuser')
    else:
        return HttpResponse('Activation link is invalid!')



@login_required(login_url="loginuser")
def home(request):
    questionPapers = QuestionPaperDetail.objects.all()
    paginator = Paginator(questionPapers, 10)
    page = request.GET.get('page')
    questionPapers = paginator.get_page(page)
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
        questionPapers = QuestionPaperDetail.objects.all().filter(Q(subjectName__icontains=query) | Q(subjectCode__icontains=query) | Q(year__icontains=query) |Q(examType__icontains=query))
        paginator = Paginator(questionPapers, 10)
        page = request.GET.get('page')
        questionPapers = paginator.get_page(page)
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
        'student':student,
    }
    return render(request, 'questionBank/profile.html',context)

    
@login_required(login_url="loginuser")
def uploadPage(request):
    form = QuestionPaperForm()
    if request.method == "POST":
        form = QuestionPaperForm(request.POST, request.FILES)
        subjectName = request.POST.get('subjectName').lower()
        subjectCode = request.POST.get('subjectCode').lower()
        year = request.POST.get('year')
        examType = request.POST.get('examType').lower()
        Files = request.FILES.getlist('File')
        paper_qs  = QuestionPaperDetail.objects.all().filter(
            subjectCode=subjectCode,
            subjectName=subjectName,
            year=year,
            examType=examType
            )
        
        if paper_qs.exists():
            return render(request,'questionBank/upload_error.html')
        else:
            paper = QuestionPaperDetail(
            subjectName=subjectName,
            subjectCode=subjectCode,
            year=year,
            examType=examType
            )   
            paper.save()
            for f in Files:
                paper_file = QuestionPaper(
                    File=f,
                    details=paper
                )
                paper_file.save()
            return redirect('home')
    context = {
        'form':form,
    }
    return render(request, 'questionBank/upload1.html', context)


@login_required(login_url="loginuser")
def viewPage(request, pk):
    questionPaperDetails = QuestionPaperDetail.objects.get(id=pk)
    questionPaperFiles = questionPaperDetails.questionpaper_set.all()
    context = {
        'questionPaperDetails':questionPaperDetails,
        'questionPaperFiles':questionPaperFiles,
    }
    return render(request,'questionBank/view_papers.html',context)



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

