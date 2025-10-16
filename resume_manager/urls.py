from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('upload', views.upload_resume, name='upload_resume'),
    path('resumes/', views.resume_list, name='resume_list'),
    path('keywords/', views.keyword_input, name='keyword_input'),
    path('rank/', views.rank_resumes, name='rank_resumes'),
    path('employees/', views.manage_employees, name='manage_employees'), 
    path('hire/<int:resume_id>/', views.hire_candidate, name='hire_candidate'),  # Add this
    path('delete-employee/<int:employee_id>/', views.delete_employee, name='delete_employee'),  # Add this # Already there
    path('delete-resume/<int:resume_id>/', views.delete_resume, name='delete_resume'),
    path('edit-employee-name/<int:employee_id>/', views.edit_employee_name, name='edit_employee_name'),
path('edit-employee-skills/<int:employee_id>/', views.edit_employee_skills, name='edit_employee_skills'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
  path('logout/', views.logout_view, name='logout'),]