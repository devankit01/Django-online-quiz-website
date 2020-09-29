"""Django_Main_App URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Quiz_App.views import *    
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home , name = 'home'),
    path('dashboard', dashboard , name = 'dashboard'),

    path('single_quiz/quiz/<id>', quiz , name = 'quiz'),
    path('create_category', create_category , name = 'create_category'),
    path('add_question/<id>', add_question , name = 'add_question'),
    path('final_submit/<id>', final_submit , name = 'final_submit'),
    path('render_result', render_result , name = 'render_result'),

    path('all_quiz', all_quiz , name = 'all_quiz'),
    path('single_quiz/<id>', single_quiz , name = 'single_quiz'),
    path('register', register , name = 'register'),
    path('login', login , name = 'login'),
    path('logout', logout , name = 'logout'),
    path('profile', profile , name = 'profile'),
    path('created_quiz', created_quiz , name = 'created_quiz'),
    path('submissions', submissions , name = 'submissions'),
    path('my_quiz', my_quiz , name = 'my_quiz'),
    path('quiz_delete/<id>', delete_quiz , name = 'delete_quiz'),
    path('all_submissions/', all_submissions , name = 'all_submissions'),
    path('get_answers/<id>', get_answers , name = 'get_answers'),




    
    path('reset-password', auth_views.PasswordResetView.as_view(template_name = 'password/password_reset.html') , name = 'password_reset'),
    path('reset-password-done', auth_views.PasswordResetDoneView.as_view(template_name = 'password/password_reset_done.html') , name = 'password_reset_done'),
    path('reset-password-confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name = 'password/password_reset_confirm.html') , name = 'password_reset_confirm'),
    path('reset-password-complete', auth_views.PasswordResetCompleteView.as_view(template_name = 'password/password_reset_complete.html') , name = 'password_reset_complete'),

   




    







   



]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root= settings.STATIC_ROOT)