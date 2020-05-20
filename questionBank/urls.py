from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name="home"),
    path('profile/',views.studentProfile,name='student_profile'),
    path('upload/',views.uploadPage, name="upload_page"),

    #auth usrls
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