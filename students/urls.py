from django.urls import path, include
from . import views

urlpatterns = [
  path('', views.alogin, name='login'),
  path('logout/', views.logout_view, name='logout'),

  path('hod_home/', views.hod_home, name='hod_home'),

  #pa
  path('doLogin/', views.doLogin, name="doLogin"),
  
  path('home_pa/', views.home_pa, name='home_pa'),
  path('pa_profile/',views.pa_profile, name='pa_profile'),
  path('curriculum/<int:curriculum_id>/subject/', views.curriculum_year_semester_subject_add, name='curriculum_year_semester_subject_add'),

  path('curriculum/', views.curriculum_list, name='curriculum_list'),
  path('delete_curriculum/<int:id>/', views.delete_curriculum, name='delete_curriculum'),
  path('new_curriculum/',views.new_curriculum, name='new_curriculum'),
  path('curriculum_detail/<int:curriculum_id>',views.curriculum_detail,name='curriculum_detail'),
  path('curriculum/<int:curriculum_id>/subject/<int:subject_id>/delete/',views.delete_subject_from_curriculum, name='delete_subject_from_curriculum'),
  path('curriculum/<int:curriculum_id>/subject/<int:subject_id>/edit/', views.edit_subject_from_curriculum, name='edit_subject_from_curriculum'),

  path('curriculum/<int:curriculum_id>/',views.enroll_students, name='enroll_students'),
  



  path('curriculum/<int:curriculum_id>/create_year_level/', views.create_year_level, name='create_year_level'),
  path('curriculum/<int:curriculum_id>/delete_year_level/', views.delete_year_level, name='delete_year_level'),

  path('curriculum/<int:curriculum_id>/year-levels/', views.get_year_levels, name='get_year_levels'),


  path('add_enroll_student/<int:curriculum_id>/', views.add_enroll_student, name='add_enroll_student'),

  path('semesters/', views.get_semesters, name='get_semesters'),

  path('add_semester/', views.add_semester, name='add_semester'),

  path('delete_latest_semester/', views.delete_latest_semester, name='delete_latest_semester'),




  path('student/', views.index, name='index'),
  path('<int:id>', views.view_student, name='view_student'),
  path('add/', views.save_student, name='add'),
  path('edit_student/<int:id>', views.edit_student, name="edit_student"),
  #path('edit_student_save/', views.edit_student_save, name="edit_student_save"),
  #path('edit_student/', views.edit, name='edit'),
  #path('delete/<int:curriculum_id>/', views.delete, name='delete'),
  path('student/delete/<int:id>/', views.student_delete, name='student_delete'),



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


  path('student/<int:user_id>/', views.student_grades, name='student_grades'),

  path('grade_student/<int:user_id>/', views.grade_student, name='grade_student'),


  #ojt
  path('home_ojt/', views.home_ojt, name='home_ojt'),
  path('ojt_index/', views.ojt_index, name='ojt_index'),

  #student
  path('home_student/', views.home_student, name='home_student'),
  path('student_index/', views.student_index, name='student_index'),

  path('student_profile/',views.student_profile, name='student_profile'),

  #sending mail
  path('contact_form/',views.contact_form, name="contact_form"),




]