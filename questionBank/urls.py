from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name="home"),
    path('profile/',views.studentProfile,name='student_profile'),
    path('upload/',views.uploadPage, name="upload_page"),
    path('search/',views.searchResult, name="searchResult"),
    path('contactus/',views.contactPage, name="contactus"),
    path('view/<str:pk>',views.viewPage, name="viewpage"),

    #auth usrls
    path('verify/<uidb64>/<token>', views.verify_account, name="verify_account"),
    path('resend_verification_link/<str:uidb64>',views.resend_verification_link, name='resend_verification_link'),
    path('signup/',views.signupuser, name="signupuser"),
    path('login/',views.loginuser, name="loginuser"),
    path('logout/',views.logoutuser, name="logoutuser"),
    path('password_reset/',
        auth_views.PasswordResetView.as_view(template_name = 'questionBank/password_reset.html'), 
        name = "password_reset"
    ),
    path('password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name = 'questionBank/password_reset_sent.html'), 
        name = "password_reset_done"
    ),
    path('password_reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name = 'questionBank/password_reset_form.html'), 
        name = "password_reset_confirm"
    ),
    path('password_reset/complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name = 'questionBank/password_reset_done.html'), 
        name = "password_reset_complete"
    ),
    path('password_change',
        auth_views.PasswordChangeView.as_view(template_name = 'questionBank/password_change.html'), 
        name = "password_change"
    ),

    path('password_change/done',
        auth_views.PasswordChangeDoneView.as_view(template_name = 'questionBank/password_change_done.html'), 
        name = "password_change_done"
    ),
]