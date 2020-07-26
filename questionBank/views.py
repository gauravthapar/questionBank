from django.shortcuts import render , redirect
from django.http import HttpResponse
from questionBank.forms import SignupForm, StudentForm, QuestionPaperForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from questionBank.models import QuestionPaper, Student, Feedback, QuestionPaperDetail
from django.db.models import Q
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from questionBank.decorators import unauthenticated_user
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from questionBank.services.email import send_email_verification_link, feedback_reply_email
from questionBank.services.user_verification import get_user_from_uidb64, get_uidb64_from_user
from questionBank.services.signup_verification_link import verified_user_activation
from questionBank.services.files import check_file_extension

# Create your views here.


@unauthenticated_user
def signupuser(request):
    form = SignupForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            uidb64 = get_uidb64_from_user(user)
            if send_email_verification_link(request, user):
                return render(request, 'questionBank/verification_link_sent.html',{'link_sent':True, 'user':uidb64})
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
    if verified_user_activation(uidb64, token):
        user = get_user_from_uidb64(uidb64)
        user.is_active = True
        user.save()
        return redirect('loginuser')
    else:
        return HttpResponse('Activation link is invalid!')


def resend_verification_link(request, uidb64):
    user = get_user_from_uidb64(uidb64)
    if user.is_active == False:
        send_email_verification_link(request, user)
        return render(request, 'questionBank/verification_link_sent.html',{'link_resent':True, 'user':uidb64})
    else:
        return HttpResponse('Account is already verified.')
    

@login_required(login_url="loginuser")
def home(request):
    questionPapers = QuestionPaperDetail.objects.all().order_by('-date_created')
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
        request_user = User.objects.get(username=request.POST['username'])
        uidb64 = get_uidb64_from_user(request_user)
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            context = {
                'not_active': True,
                'user': uidb64, 
            }
            return render(request, 'questionBank/verification_link_sent.html', context)
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
        files = request.FILES.getlist('File')
        if not check_file_extension(files):
            return render(request, 'questionBank/upload1.html', {"errors":"Please check the format of the file"})
        paper, created = QuestionPaperDetail.objects.get_or_create(
            subjectName=subjectName,
            subjectCode=subjectCode,
            year=year,
            examType=examType
        )
        for file in files:
            paper_file = QuestionPaper(
                File=file,
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
        user = request.user
        feedback_reply_email(user)
        return redirect('home')
    else:
        student = request.user.student
        return render(request, 'questionBank/contact.html',{'student':student})



def logoutuser(request):
    if request.method == "POST":
        logout(request)
        return redirect('loginuser')

