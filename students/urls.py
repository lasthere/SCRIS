from django.urls import path, include
from . import views

urlpatterns = [
  path('', views.alogin, name='login'),
  path('logout/', views.logout_view, name='logout'),

  path('hod_home/', views.hod_home, name='hod_home'),

  #pa
  path('doLogin/', views.doLogin, name="doLogin"),
  
  path('home_pa/', views.home_pa, name='home_pa'),

  path('search/',views.student_search, name='search'),
  
  path('student/', views.index, name='index'),
  path('<int:id>', views.view_student, name='view_student'),
  path('add/', views.save_student, name='add'),
  path('edit_student/<int:id>', views.edit_student, name="edit_student"),
  #path('edit_student_save/', views.edit_student_save, name="edit_student_save"),
  #path('edit_student/', views.edit, name='edit'),
  path('delete/<int:id>/', views.delete, name='delete'),

  path('add_ojt/', views.add_ojt,name='add_ojt'),
  path('ojt_list/', views.ojt_list, name='ojt_list'), 
  path('<int:id>', views.view_officer, name='view_officer'),
  #path('edit_officer_view/<officert_id>', views.edit_officerview, name="edit_officer"),
  path('edit_officer/<int:id>/', views.edit_officer, name='edit_officer'),
  path('delete_officer/<int:id>/', views.delete_officer, name='delete_officer'),

  path('add_hod/', views.add_hod,name='add_hod'),
  path('hod_list/', views.hod_list, name='hod_list'), 
  path('<int:id>', views.view_hod, name='view_hod'),
  path('edit_hod/<int:id>/', views.edit_hod, name='edit_hod'),
  path('delete_hod/<int:id>/', views.delete_hod, name='delete_hod'),

  path('add_pa/', views.add_pa,name='add_pa'),
  path('pa_list/', views.pa_list, name='pa_list'), 
  path('<int:id>', views.view_pa, name='view_pa'),
  path('edit_pa/<int:id>/', views.edit_pa, name='edit_pa'),
  path('delete_pa/<int:id>/', views.delete_pa, name='delete_pa'),

  path('add_subject/', views.add_subject,name='add_subject'),
  path('subject_list/', views.subject_list, name='subject_list'), 
  path('<int:id>', views.view_subject, name='view_subject'),
  path('edit_subject/<int:id>/', views.edit_subject, name='edit_subject'),
  path('delete_subject/<int:id>/', views.delete_subject, name='delete_subject'),

  path('add_grade',views.add_grade, name='add_grade'),

  path('student/<int:user_id>/', views.student_grades, name='student_grades'),


  #ojt
  path('home_ojt/', views.home_ojt, name='home_ojt'),
  path('ojt_index/', views.ojt_index, name='ojt_index'),

  #student
  path('home_student/', views.home_student, name='home_student'),
  path('student_index/', views.student_index, name='student_index'),
  path('students/year/<str:year_level>/', views.students_by_year_view, name='students_by_year'),
  path('student_profile/',views.student_profile, name='student_profile'),

  #sending mail
  path('contact_form/',views.contact_form, name="contact_form"),



]