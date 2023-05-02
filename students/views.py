from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django_pglocks import advisory_lock
from django.forms import formset_factory
from django.views.decorators.http import require_POST



from django.conf import settings
from django.core.mail import EmailMultiAlternatives, BadHeaderError, send_mail, send_mass_mail
import smtplib

from students.templatetags.myapp_tags import calculate_total_units_semester,get_subject_status,has_grade,get_subject_grade
from .models import CustomUser, Student, Ojt_Officer, Dept_Head, ProgramAdvisor, Subject, SubjectGrade, Curriculum, YearLevel, Semester, StudentEnrollment
from .forms import StudentForm, OjtForm, HodForm, PaForm, SubForm,EditStudentForm,EditStudentFormUser,EditOjtForm,EditProfile,StudentSearchForm,CurriculumForm,AddSubjectForm,EnrollStudentForm,GradeForm 

# Create your views here.
# Login

def alogin(request):
  return render(request,'login.html')

def logout_view(request):
  logout(request)
  return redirect('/')

def doLogin(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)

    if user is not None:
      login(request, user)
      if user.user_type == '1':
        return redirect('hod_home')
      elif user.user_type == '2':
        return redirect('home_pa')
      elif user.user_type == '3':
        return redirect('home_student')
      elif user.user_type == '4':
        return redirect('home_ojt')
    else:
      error_message = 'Invalid login credentials'
  else:
    error_message = ''

  return render(request, 'login.html', {'error_message': error_message})


# Students
@login_required
def hod_home(request):
  if request.user.user_type == '1':
    context = {
      'user_name': request.user.get_full_name(),
      'user_id': request.user.id,
    }
    return render(request, 'PA_Views/home_pa.html')
  else:
    return render(request, 'login.html')

def home_pa(request):
  if request.user.user_type == '2':
    context = {
      'user_name': request.user.get_full_name(),
      'user_id': request.user.id,
    }
    return render(request, 'PA_Views/home_pa.html')
  else:
    return render(request, 'login.html')

@login_required
def pa_profile(request):
  if request.user.user_type == '2':
    if request.method == 'POST':
      pa_user = CustomUser.objects.get(id=request.user.id)
      pa = ProgramAdvisor.objects.get(user_id=request.user.id)
      form1 =EditProfile(request.POST, instance=pa_user)
      if form1.is_valid():
        form1.save()
        return render(request, 'PA_Views/profile.html', {
          'form1': form1,
          'success': True
        })
    else:
      pa_user = CustomUser.objects.get(pk=request.user.id)
      form1 =EditProfile(instance=pa_user)
  return render(request, 'PA_Views/profile.html', {
    'form1': form1
  })

@login_required
def home_student(request):
  if request.user.user_type == '3':
    student = Student.objects.get(user_id=request.user.id)
    grades = SubjectGrade.objects.filter(student_id=student).select_related('subject_id')

    subject_count = grades.count()

    failed_count = student.subjectgrade_set.filter(status='failed').count()

    if failed_count > 0:
      message =f"You have { failed_count } failed subjects!"
    else:
      message=f"Your doing great { student.user.first_name }, keep it up!"

    return render(request, 'student_view/home_student.html',{
      'student': student,
      'failed_count':failed_count,
      'message':message,
      'subject_count':subject_count,
      })
  else:
    return render(request, 'login.html')

@login_required
def student_profile(request):
  

  if request.user.user_type == '3':
    student = Student.objects.get(user_id=request.user.id)
    grades = SubjectGrade.objects.filter(student_id=student).select_related('subject_id')

    subject_count = grades.count()

    failed_count = student.subjectgrade_set.filter(status='failed').count()

    if failed_count > 0:
      message =f"You have { failed_count } failed subjects!"
    else:
      message=f"Your doing great { student.user.first_name }, keep it up!"

    if request.method == 'POST':
      student_user = CustomUser.objects.get(id=request.user.id)
      student = Student.objects.get(user_id=request.user.id)
      form1 =EditProfile(request.POST, instance=student_user)
      if form1.is_valid():
        form1.save()
        return render(request, 'student_view/profile.html', {
          'form1': form1,
          'success': True,
        })
    else:
      student_user = CustomUser.objects.get(pk=request.user.id)
      form1 =EditProfile(instance=student_user)
  return render(request, 'student_view/profile.html', {
    'form1': form1,
    'failed_count':failed_count,
    'message':message,

  })
#student views
@login_required
def legible_subjects_to_take (request):
  if request.user.user_type == '3':
    student = Student.objects.get(user_id=request.user.id)
    student_enrollment = get_object_or_404(StudentEnrollment, student=student)
    curriculum = student_enrollment.curriculum
    yearlevels = curriculum.year_levels.all() 

@login_required
def student_index(request):
  if request.user.user_type == '3':
    student = Student.objects.get(user_id=request.user.id)
    grades = SubjectGrade.objects.filter(student_id=student).select_related('subject_id')

    subject_count = grades.count()

    failed_count = student.subjectgrade_set.filter(status='failed').count()

    if failed_count > 0:
      message =f"You have { failed_count } failed subjects!"
    else:
      message=f"Your doing great { student.user.first_name }, keep it up!"

    student_enrollment = get_object_or_404(StudentEnrollment, student=student)
    curriculum = student_enrollment.curriculum
    yearlevels = curriculum.year_levels.all()

    student_subject_grade=SubjectGrade.objects.filter(student=student)

    passed_grades = SubjectGrade.objects.filter(student=student, status='passed')

    total_units_passed = passed_grades.aggregate(total_units=Sum('subject__subj_units_lec')+Sum('subject__subj_units_lab'))['total_units']

    available_subjects = set()
    for subject in Subject.objects.filter(curriculum=curriculum):
      if not subject.prerequisites.all():
        if get_subject_grade(student, subject) == 0.0:
          available_subjects.add(subject)
        elif get_subject_status(student, subject) == 'failed':
          available_subjects.add(subject)
      else:
        prerequisites_passed = True
        for prerequisite in subject.prerequisites.all():
          if get_subject_status(student, prerequisite) != 'passed':
            prerequisites_passed = False
            break
          if prerequisites_passed:
            available_subjects.add(subject)


    no_subjects = set()
    for bad_subjects in Subject.objects.filter(curriculum=curriculum):
      if not bad_subjects.prerequisites.all():
        if get_subject_status (student, bad_subjects) != 'failed':
          if get_subject_grade(student, bad_subjects) != 0.0:
            no_subjects.add(bad_subjects)
          if get_subject_status(student, bad_subjects) == 'incomplete':
            no_subjects.add(bad_subjects)
          elif get_subject_status(student, bad_subjects) == 'passed':
            no_subjects.add(bad_subjects)
      else:
        for prerequisite in bad_subjects.prerequisites.all():
          if get_subject_status(student, prerequisite) != 'passed':
            no_subjects.add(bad_subjects)
            break

    Inc_subjects = []
    for inc in Subject.objects.filter(curriculum=curriculum):
      if get_subject_status(student, inc) == 'incomplete':
        Inc_subjects.append(inc)

    yearlevels1 = YearLevel.objects.filter(curriculum=curriculum)
    semesters = Semester.objects.filter(year_level__in=yearlevels1)
    atotal_units = Subject.objects.filter(curriculum=curriculum).aggregate(total_units=Sum('subj_units_lec')+Sum('subj_units_lab'))['total_units']



    return render(request,'student_view/index.html',{
      'student': student,
      'curriculum':curriculum,
      'yearlevels1':yearlevels1,
      'semesters':semesters,
      'yearlevels':yearlevels,
      'atotal_units': atotal_units,
      'calculate_total_units_semester':calculate_total_units_semester,
      'student_subject_grade':student_subject_grade,
      'total_units_passed': total_units_passed,
      'available_subjects':available_subjects,
      'Inc_subjects':Inc_subjects,
      'no_subjects':no_subjects,
      'failed_count':failed_count,
      'message':message,


      })
  else:
    return render(request, 'login.html')

def home_ojt(request):
  if request.user.user_type == '4':
    context = {
      'user_name': request.user.get_full_name(),
      'user_id': request.user.id,
    }
    return render(request, 'ojt_view/home_ojt.html')
  else:
    return render(request, 'login.html')
  


def student_grades(request, user_id):
    student = Student.objects.get(user_id=user_id)

    student_enrollment = get_object_or_404(StudentEnrollment, student=student)
    curriculum = student_enrollment.curriculum
    yearlevels = curriculum.year_levels.all()
    yearlevels1 = YearLevel.objects.filter(curriculum=curriculum)
    semesters = Semester.objects.filter(year_level__in=yearlevels1)

    student_subject_grade = SubjectGrade.objects.filter(student=student)

    passed_grades = SubjectGrade.objects.filter(student=student, status='passed')
    total_units_passed = passed_grades.aggregate(total_units=Sum('subject__subj_units_lec')+Sum('subject__subj_units_lab'))['total_units']

    atotal_units = Subject.objects.filter(curriculum=curriculum).aggregate(total_units=Sum('subj_units_lec')+Sum('subj_units_lab'))['total_units']

    available_subjects = set()
    for subject in Subject.objects.filter(curriculum=curriculum):
      if not subject.prerequisites.all():
        if get_subject_grade(student, subject) == 0.0:
          available_subjects.add(subject)
        elif get_subject_status(student, subject) == 'failed':
          available_subjects.add(subject)
      else:
        prerequisites_passed = True
        for prerequisite in subject.prerequisites.all():
          if get_subject_status(student, prerequisite) != 'passed':
            prerequisites_passed = False
            break
          if prerequisites_passed:
            available_subjects.add(subject)


    no_subjects = set()
    for bad_subjects in Subject.objects.filter(curriculum=curriculum):
      if not bad_subjects.prerequisites.all():
        if get_subject_status (student, bad_subjects) != 'failed':
          if get_subject_grade(student, bad_subjects) != 0.0:
            no_subjects.add(bad_subjects)
          if get_subject_status(student, bad_subjects) == 'incomplete':
            no_subjects.add(bad_subjects)
          elif get_subject_status(student, bad_subjects) == 'passed':
            no_subjects.add(bad_subjects)
      else:
        for prerequisite in bad_subjects.prerequisites.all():
          if get_subject_status(student, prerequisite) != 'passed':
            no_subjects.add(bad_subjects)
            break

    Inc_subjects = []
    for inc in Subject.objects.filter(curriculum=curriculum):
        if get_subject_status(student, inc) == 'incomplete':
          Inc_subjects.append(inc)


    return render(request, 'PA_Views/student_grade.html', {
        'student': student,
        'curriculum': curriculum,
        'student_subject_grade': student_subject_grade,
        'yearlevels1': yearlevels1,
        'semesters': semesters,
        'yearlevels': yearlevels,
        'atotal_units': atotal_units,
        'calculate_total_units_semester': calculate_total_units_semester,
        'total_units_passed': total_units_passed,
        'available_subjects': available_subjects,
        'Inc_subjects':Inc_subjects,
        'no_subjects':no_subjects,
    })


def index(request):
  students = Student.objects.all().order_by('year_level','user__username','user__first_name','user__last_name','middle_initial') 

  year_level = request.GET.get('year_level')
  if year_level:
    students = Student.objects.filter(year_level=year_level)


  form1 = StudentSearchForm(request.GET or None)
  if form1.is_valid():
    if form1.cleaned_data['submit']:
      query = form1.cleaned_data['query']
      students = Student.objects.filter(
        Q(user__first_name__icontains=query) |
        Q(user__last_name__icontains=query) |
        Q(user__username__icontains=query)
      )
  return render(request, 'PA_Views/index.html', {
    'students': students,
    'form1':form1,
    'form': StudentForm(),

  })

def view_student(request, id):
  student = Student.objects.get(pk=id)
  return HttpResponseRedirect(reverse('index'))

def save_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['student_number']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            middle_initial = form.cleaned_data['middle_initial']
            email = form.cleaned_data['email']
            year_level = form.cleaned_data['year_level']
            middle_initial == middle_initial.upper()

            user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=3)
            user.student.middle_initial=middle_initial
            user.student.year_level=year_level
            user.save()
            message = 'Subject successfully added'
            messages.success(request, message)
            return HttpResponseRedirect(reverse('index'), {
                'form': StudentForm(),
                'message':message
            })
        else:
            message='Failed to save!'
            return HttpResponseRedirect(reverse('index'), {
                'form': StudentForm(),
                'message':message,
            })
    else:
        return render(request, 'PA_Views/index.html', {
            'form': StudentForm()
        })


    
def edit_student(request, id):
  if request.method == 'POST':
    student_user = CustomUser.objects.get(pk=id)
    student = Student.objects.get(pk=id)
    form = EditStudentForm(request.POST, instance=student)
    form1 =EditStudentFormUser(request.POST, instance=student_user)
    if form.is_valid() and form1.is_valid():
      form.save()
      form1.save()
      return render(request, 'PA_Views/edit.html', {
        'form': form,
        'form1': form1,
        'success': True
      })
  else:
    student = Student.objects.get(pk=id)
    form = EditStudentForm(instance=student)
    student_user = CustomUser.objects.get(pk=id)
    form1 =EditStudentFormUser(instance=student_user)
  return render(request, 'PA_Views/edit.html', {
    'form': form,
    'form1': form1
  })

def student_delete(request, id):
  if request.method == 'POST':
    student = Student.objects.get(pk=id)
    student_user = CustomUser.objects.get(pk=id)
    student_user.delete()
    student.delete()
  return HttpResponseRedirect(reverse('index'))


 # Ojt Officers Account


def ojt_list(request):
  return render(request, 'PA_Views/ojt_list.html', {
    'officers': Ojt_Officer.objects.all()
  })

def view_officer(request, id):
  officer = Ojt_Officer.objects.get(pk=id)
  return HttpResponseRedirect(reverse('ojt_list'))


def add_ojt(request):
  if request.method == 'POST':
    form = OjtForm(request.POST)
    if form.is_valid():
      username = form.cleaned_data['username']
      password = form.cleaned_data['password']
      email = form.cleaned_data['email']
      first_name = form.cleaned_data['first_name']
      last_name = form.cleaned_data['last_name']



      new_officer = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=4)
      new_officer.save()
      return render(request, 'PA_Views/add_ojt.html', {
        'form': OjtForm(),
        'success': True
      })
  else:
    form = OjtForm()
  return render(request, 'PA_Views/add_ojt.html', {
    'form': form,
  })






def edit_officer(request, id):
  if request.method == 'POST':
    officer = CustomUser.objects.get(pk=id)
    form = EditOjtForm(request.POST, instance=officer)
    if form.is_valid():
      form.save()
      return render(request, 'PA_Views/edit_ojt.html', {
        'form': form,
        'success': True
      })
  else:
    officer = CustomUser.objects.get(pk=id)
    form = EditOjtForm(instance=officer)
  return render(request, 'PA_Views/edit_ojt.html', {
    'form': form
  })

def delete_officer(request, id):
  if request.method == 'POST':
    officer = CustomUser.objects.get(pk=id)
    officer.delete()
  return HttpResponseRedirect(reverse('ojt_list'))
  #HOD Account


def hod_list(request):
  return render(request, 'PA_Views/hod_list.html', {
    'hods': Dept_Head.objects.all()
  })

def view_hod(request, id):
  hod = Dept_Head.objects.get(pk=id)
  return HttpResponseRedirect(reverse('hod_list'))

def add_hod(request):
  if request.method == 'POST':
    form = HodForm(request.POST)
    if form.is_valid():
      username = form.cleaned_data['username']
      password = form.cleaned_data['password']
      first_name = form.cleaned_data['first_name']
      last_name = form.cleaned_data['last_name']


      new_head = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=1)
      new_head.save()
      return render(request, 'PA_Views/add_hod.html', {
        'form': HodForm(),
        'success': True
      })
  else:
    form = HodForm()
  return render(request, 'PA_Views/add_hod.html', {
    'form': HodForm()
  })

def delete_hod(request, id):
  if request.method == 'POST':
    hod = CustomUser.objects.get(pk=id)
    hod.delete()
  return HttpResponseRedirect(reverse('hod_list'))

def edit_hod(request, id):
  if request.method == 'POST':
    hod = CustomUser.objects.get(pk=id)
    form = HodForm(request.POST, instance=hod)
    if form.is_valid():
      form.save()
      return render(request, 'PA_Views/edit_hod.html', {
        'form': form,
        'success': True
      })
  else:
    hod = CustomUser.objects.get(pk=id)
    form = HodForm(instance=hod)
  return render(request, 'PA_Views/edit_hod.html', {
    'form': form
  })


    #PA Account



def pa_list(request):
  return render(request, 'PA_Views/pa_list.html', {
    'pas': ProgramAdvisor.objects.all()
  })

def view_pa(request, id):
  pa = ProgramAdvisor.objects.get(pk=id)
  return HttpResponseRedirect(reverse('pa_list'))

def add_pa(request):
  if request.method == 'POST':
    form = PaForm(request.POST)
    if form.is_valid():
      username = form.cleaned_data['username']
      password = form.cleaned_data['password']
      first_name = form.cleaned_data['first_name']
      last_name = form.cleaned_data['last_name']
      email =form.cleaned_data['email']


      new_PA = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=2)
      new_PA.save()
      return render(request, 'PA_Views/add_pa.html', {
        'form': PaForm(),
        'success': True
      })
  else:
    form = PaForm()
  return render(request, 'PA_Views/add_pa.html', {
    'form': PaForm()
  })

def delete_pa(request, id):
  if request.method == 'POST':
    pa = CustomUser.objects.get(pk=id)
    pa.delete()
  return HttpResponseRedirect(reverse('pa_list'))

def edit_pa(request, id):
  if request.method == 'POST':
    pa = CustomUser.objects.get(pk=id)
    form = PaForm(request.POST, instance=pa)
    if form.is_valid():
      form.save()
      return render(request, 'PA_Views/edit_pa.html', {
        'form': form,
        'success': True
      })
  else:
    pa = CustomUser.objects.get(pk=id)
    form = PaForm(instance=pa)
  return render(request, 'PA_Views/edit_pa.html', {
    'form': form
  })

     #Subjects

def subject_list(request):
  subs= Subject.objects.all()
  form = StudentSearchForm(request.GET)
  if form.is_valid():
    query = form.cleaned_data['query']
    subs = Subject.objects.filter(
      Q(subj_name__icontains=query)|
      Q(subj_code__icontains=query)
      )
  return render(request, 'PA_Views/subject_list.html', {
    'subs': subs,
    'form':form,
  })

def view_subject(request, id):
  subject = Subject.objects.get(pk=id)
  return HttpResponseRedirect(reverse('subject_list'))

def add_subject(request):
  if request.method == 'POST':
    form = SubForm(request.POST)
    if form.is_valid():
      new_subj_code = form.cleaned_data['subj_code']
      new_subj_name = form.cleaned_data['subj_name']
      new_subj_hr_lec = form.cleaned_data['subj_hr_lec']
      new_subj_hr_lab = form.cleaned_data['subj_hr_lab']
      new_subj_units_lec = form.cleaned_data['subj_units_lec']
      new_subj_units_lab = form.cleaned_data['subj_units_lab']
      new_prerequisite = form.cleaned_data['prerequisite']

      new_Subj= Subject(
        subj_code = new_subj_code,
        subj_name = new_subj_name,
        subj_hr_lec = new_subj_hr_lec,
        subj_hr_lab = new_subj_hr_lab,
        subj_units_lec = new_subj_units_lec,
        subj_units_lab = new_subj_units_lab,
        prerequisite = new_prerequisite,
      )
      new_Subj.save()
      return render(request, 'PA_Views/add_subject.html', {
        'form': SubForm(),
        'success': True
      })
  else:
    form = SubForm()
  return render(request, 'PA_Views/add_subject.html', {
    'form': form,
  })


#sending mail

def contact_form(request):
  students = Student.objects.all()
  context = {
      'students':students
  }
  if request.method == 'POST':
    name = "Program Advisor"
    email = settings.EMAIL_HOST_USER
    message = "From: "+ email + "\n" 
    message += "Sender Name: "+ name + "\n\r\n\r" 
    message += "--------------------------------------------------------------------------------------------------------"
    message += "\n\r\n\r"
 
    message += request.POST['message']
    message += "\n\r\n\r"
    message += "http://joseprotacio.pythonanywhere.com/"

    recievers = [student.user.email for student in students] 


    try:

      messages = [(name, message, email, [recipient]) for recipient in recievers]
      send_mass_mail(messages)

            #send_mail(
            #    'SITE Inquiry - '+ name,
            #    message,
            #    email,
            #    recievers,
            #)
      context = {'mail_response':True}
    except Exception as err:
      raise err
 
  return render(request,'PA_Views/send_email.html',context) 


# csrf exmpt





#ojt officer views

def ojt_index(request):
    passed_grades = SubjectGrade.objects.filter(status='passed')

    student_subject_units = passed_grades.values('student_id', 'subject_id').annotate(
        total_units=Sum('subject_id__subj_units_lec')+Sum('subject_id__subj_units_lab')
    )

    student_units = {}
    for data in student_subject_units:
        student_id = data['student_id']
        subject_units = data['total_units']
        if student_id not in student_units:
            student_units[student_id] = subject_units
        else:
            student_units[student_id] += subject_units

    students = Student.objects.filter(year_level='4').distinct()

    student_data = []
    for student in students:
        number = student.user.username
        my_id = student.user.id
        name = student.user.get_full_name()
        middle_initial = student.middle_initial
        units = student_units.get(student.pk,0)
        year = student.year_level
        ojtstatus=""
        if (units >= 109.0):
            ojtstatus="\u2713"
        else:
            ojtstatus="X"
        student_data.append({'name': name, 'my_id':my_id,'units': units, 'number':number,'middle_initial':middle_initial,'ojtstatus':ojtstatus,'year':year})
        
    numstudent = len(student_data)

    count_passed = 0
    for student in student_data:
        if student['ojtstatus'] == "\u2713":
            count_passed += 1

    return render(request,'ojt_view/index.html', {
    "students":student_data,
    "numstudent":numstudent,
    "count_passed":count_passed,
    })

def ojt_student_grades(request, user_id):
    student = Student.objects.get(user_id=user_id)

    student_enrollment = get_object_or_404(StudentEnrollment, student=student)
    curriculum = student_enrollment.curriculum
    yearlevels = curriculum.year_levels.all()
    yearlevels1 = YearLevel.objects.filter(curriculum=curriculum)
    semesters = Semester.objects.filter(year_level__in=yearlevels1)

    student_subject_grade = SubjectGrade.objects.filter(student=student)

    passed_grades = SubjectGrade.objects.filter(student=student, status='passed')
    total_units_passed = passed_grades.aggregate(total_units=Sum('subject__subj_units_lec')+Sum('subject__subj_units_lab'))['total_units']

    atotal_units = Subject.objects.filter(curriculum=curriculum).aggregate(total_units=Sum('subj_units_lec')+Sum('subj_units_lab'))['total_units']

    available_subjects = set()
    for subject in Subject.objects.filter(curriculum=curriculum):
      if not subject.prerequisites.all():
        if get_subject_grade(student, subject) == 0.0:
          available_subjects.add(subject)
        elif get_subject_status(student, subject) == 'failed':
          available_subjects.add(subject)
      else:
        prerequisites_passed = True
        for prerequisite in subject.prerequisites.all():
          if get_subject_status(student, prerequisite) != 'passed':
            prerequisites_passed = False
            break
          if prerequisites_passed:
            available_subjects.add(subject)


    no_subjects = set()
    for bad_subjects in Subject.objects.filter(curriculum=curriculum):
      if not bad_subjects.prerequisites.all():
        if get_subject_status (student, bad_subjects) != 'failed':
          if get_subject_grade(student, bad_subjects) != 0.0:
            no_subjects.add(bad_subjects)
          if get_subject_status(student, bad_subjects) == 'incomplete':
            no_subjects.add(bad_subjects)
          elif get_subject_status(student, bad_subjects) == 'passed':
            no_subjects.add(bad_subjects)
      else:
        for prerequisite in bad_subjects.prerequisites.all():
          if get_subject_status(student, prerequisite) != 'passed':
            no_subjects.add(bad_subjects)
            break

    Inc_subjects = []
    for inc in Subject.objects.filter(curriculum=curriculum):
        if get_subject_status(student, inc) == 'incomplete':
          Inc_subjects.append(inc)


    return render(request, 'ojt_view/ojt_student_grade.html', {
        'student': student,
        'curriculum': curriculum,
        'student_subject_grade': student_subject_grade,
        'yearlevels1': yearlevels1,
        'semesters': semesters,
        'yearlevels': yearlevels,
        'atotal_units': atotal_units,
        'calculate_total_units_semester': calculate_total_units_semester,
        'total_units_passed': total_units_passed,
        'available_subjects': available_subjects,
        'Inc_subjects':Inc_subjects,
        'no_subjects':no_subjects,
    })

def ojt_view_students(request, id):
  subject = Student.objects.get(pk=id)
  return HttpResponseRedirect(reverse('index'))



@csrf_exempt
def check_email_exist(request):
  email = request.POST.get("email")
  user_obj = CustomUser.objects.filter(email=email).exists()
  if user_obj:
    return HttpResponse(True)
  else:
    return HttpResponse(False)


@csrf_exempt
def check_username_exist(request):
  username = request.POST.get("username")
  user_obj = CustomUser.objects.filter(username=username).exists()
  if user_obj:
    return HttpResponse(True)
  else:
    return HttpResponse(False)


def curriculum_list(request):
  return render(request, 'PA_Views/curriculum_list.html', {
    'curriculum': Curriculum.objects.all().order_by('-curriculum_year'),
    'form':CurriculumForm(request.POST),
  })

def view_curriculum(request, id):
  curriculum = Curriculum.objects.get(pk=id)
  yearlevel_count = YearLevel.objects.filter(curriculum=curriculum).count()

  return HttpResponseRedirect(reverse('curriculum_list'))

def delete_curriculum(request, id):
    if request.method == 'POST':
        with transaction.atomic():
            curriculum = Curriculum.objects.get(pk=id)
            year_levels = curriculum.year_levels.all()
            for year_level in year_levels:
                semesters = year_level.semesters.all()
                for semester in semesters:
                    semester.subjects.clear()
                year_level.subjects.clear()
                year_level.delete()
            curriculum.subjects.clear()
            curriculum.delete()
    return HttpResponseRedirect(reverse('curriculum_list'))

def new_curriculum(request):
  if request.method == 'POST':
    form = CurriculumForm(request.POST)
    if form.is_valid():
      curriculum_year = form.cleaned_data['curriculum_year']
      if Curriculum.objects.filter(curriculum_year=curriculum_year).exists():

        emessage = 'Curriculum already exists!'
        return render(request,'PA_Views/curriculum_list.html',{
          'curriculum': Curriculum.objects.all().order_by('-curriculum_year'),
          'emessage':emessage,
          'form':CurriculumForm()
        })
      else:
        newcurriculum = Curriculum(
          curriculum_year=curriculum_year,
          )
        newcurriculum.save()
        message = 'Successfully added!'

        return render(request,'PA_Views/curriculum_list.html',{
          'curriculum': Curriculum.objects.all().order_by('-curriculum_year'),
          'message':message,
          'form':CurriculumForm()
          })
  else:
    form = CurriculumForm()
  return render(request,'PA_Views/add_curriculum.html',{\
    'form':CurriculumForm()
  })

def get_total_units_semester(semester):
    total_units = 0
    for subject in semester.subjects.all():
        subj_units_lec = subject.subj_units_lec or 0
        subj_units_lab = subject.subj_units_lab or 0
        total_units += subj_units_lec + subj_units_lab
    return total_units

def curriculum_detail(request, curriculum_id, message=None):
    curriculum = get_object_or_404(Curriculum, pk=curriculum_id)
    students = Student.objects.all()
    student_enrollments = StudentEnrollment.objects.filter(curriculum=curriculum)
    enrolled_students = [enrollment.student for enrollment in student_enrollments]

    yearlevels = curriculum.year_levels.all()

    for yearlevel in yearlevels:
        yearlevel.total_units = 0
        for semester in yearlevel.semesters.all():
            semester.total_units = get_total_units_semester(semester)
            yearlevel.total_units += semester.total_units

    count_enrolled_student = StudentEnrollment.objects.filter(curriculum=curriculum).count()
    yearlevels1 = YearLevel.objects.filter(curriculum=curriculum)
    semesters = Semester.objects.filter(year_level__in=yearlevels1)
    added_subjects = Subject.objects.filter(curriculum=curriculum)
    yearlevel_count = YearLevel.objects.filter(curriculum=curriculum).count()
    subject_count = Subject.objects.filter(curriculum=curriculum).count()
    total_units = Subject.objects.filter(curriculum=curriculum).aggregate(total_units=Sum('subj_units_lec')+Sum('subj_units_lab'))['total_units']
    return render(request, 'PA_Views/curriculum_details.html', {
        'curriculum': curriculum, 
        'students':students,
        'enrolled_students':enrolled_students,
        'count_enrolled_student':count_enrolled_student,
        'added_subjects':added_subjects,
        'yearlevel_count':yearlevel_count,
        'subject_count':subject_count,
        'total_units':total_units,
        'yearlevels1':yearlevels1,
        'semesters':semesters,
        'calculate_total_units_semester':calculate_total_units_semester,
        'yearlevels':yearlevels,
        'get_total_units_semester': get_total_units_semester, 
    })

def delete_subject_from_curriculum(request, curriculum_id, subject_id):
    curriculum = get_object_or_404(Curriculum, id=curriculum_id)
    yearlevel = YearLevel.objects.filter(curriculum=curriculum)
    subject = get_object_or_404(Subject, id=subject_id)
    subject.delete()
    messages.success(request, 'Subject successfully deleted.')
    return redirect('curriculum_detail', curriculum_id=curriculum_id)

def edit_subject_from_curriculum(request, curriculum_id, subject_id):
    curriculum = get_object_or_404(Curriculum, id=curriculum_id)
    yearlevel = YearLevel.objects.filter(curriculum=curriculum)
    subject = get_object_or_404(Subject, id=subject_id)

    if request.method == 'POST':
        subject.subj_code = request.POST.get('subj_code')
        subject.subj_name = request.POST.get('subj_name')
        subject.subj_hr_lec = request.POST.get('subj_hr_lec')
        subject.subj_hr_lab = request.POST.get('subj_hr_lab')
        subject.subj_units_lec = request.POST.get('subj_units_lec')
        subject.subj_units_lab = request.POST.get('subj_units_lab')

        subject.prerequisites.clear()

        prerequisites = request.POST.getlist('prerequisites')
        for prerequisite_id in prerequisites:
            if prerequisite_id:
                prerequisite = get_object_or_404(Subject, id=prerequisite_id)
                subject.prerequisites.add(prerequisite)

        subject.save()
        messages.success(request, f'Subject {subject.subj_code} has been updated.')
        return redirect('curriculum_detail', curriculum_id=curriculum.id)



def create_year_level(request, curriculum_id):
    try:
        curriculum = get_object_or_404(Curriculum, pk=curriculum_id)
        with transaction.atomic():
            year_levels = YearLevel.objects.filter(curriculum=curriculum).order_by('-year_level')
            if year_levels.exists():
                new_year_level_num = year_levels.first().year_level + 1
            else:
                new_year_level_num = 1
            new_year_level = YearLevel(year_level=new_year_level_num, curriculum=curriculum)
            new_year_level.save()
        message = f"Year level {new_year_level.year_level} created successfully"
        return JsonResponse({'message': message})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def delete_year_level(request, curriculum_id):
    try:
        curriculum = get_object_or_404(Curriculum, pk=curriculum_id)
        with transaction.atomic():
            year_levels = YearLevel.objects.filter(curriculum=curriculum).order_by('-year_level')
            if year_levels.exists():
                latest_year_level = year_levels.first()
                latest_year_level.delete()
                message = f"Year level {latest_year_level.year_level} deleted successfully"
            else:
                message = "No year level found to delete"
        return JsonResponse({'message': message})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def add_semester(request):
    if request.method == 'POST':
        yearlevel_id = request.POST.get('yearlevel_id')
        semester_num = request.POST.get('semester')
        year_level = get_object_or_404(YearLevel, id=yearlevel_id)
        try:
            with transaction.atomic():
                semesters = Semester.objects.filter(year_level=year_level)
                if semesters.exists():
                    new_semester_num = semesters.latest('semester').semester + 1
                else:
                    new_semester_num = 1

                new_semester = Semester(semester=new_semester_num, year_level=year_level)
                new_semester.save()

            message = f"Semester {new_semester.semester} added to Year Level {year_level.year_level}"
            semesters = Semester.objects.filter(year_level_id=yearlevel_id)
            data = [{"id": s.id, "semester": s.semester} for s in semesters]
            return JsonResponse({'message': message, 'data': data})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@require_POST
def delete_latest_semester(request):
    yearlevel_id = request.POST.get('yearlevel_id')
    latest_semester = Semester.objects.filter(year_level=yearlevel_id).order_by('-id').first()

    if latest_semester:
        latest_semester.delete()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'No semester found for the selected year level.'})


def get_year_levels(request, curriculum_id):
    year_levels = YearLevel.objects.filter(curriculum_id=curriculum_id).values('id', 'year_level')
    return JsonResponse(list(year_levels), safe=False)



def get_semesters(request):
  yearlevel_id = request.GET.get("yearlevel_id")
  semesters = Semester.objects.filter(year_level_id=yearlevel_id)
  data = [{"id": s.id, "semester": s.semester} for s in semesters]
  return JsonResponse(data, safe=False)

def curriculum_yearlevel(request, yearlevel_id):
  yearlevel = get_object_or_404(YearLevel, id=yearlevel_id)
  curriculum = yearlevel.curriculum
  added_subjects = yearlevel.subjects.all()
  semester = Semester.objects.filter(year_level=yearlevel)
  semester_count = yearlevel.semesters.count()

  yearlevel_count = YearLevel.objects.filter(curriculum=curriculum).count()
  subject_count = yearlevel.subjects.count()
  total_units = added_subjects.aggregate(total_units=Sum('subj_units_lec')+Sum('subj_units_lab'))['total_units']
  
  return render(request, 'PA_Views/curriculum_year.html', {
    'semester':Semester.objects.filter(year_level=yearlevel).order_by('semester'),
    'curriculum': curriculum, 
    'yearlevel': yearlevel,
    'yearlevel_count':yearlevel_count,
    'subject_count':subject_count,
    'total_units':total_units,
    'added_subjects':added_subjects,
    'semester_count':semester_count,
    })

def curriculum_year_semester(request, semester_id):
  semester = get_object_or_404(Semester, id=semester_id)
  semesters = semester.subjects
  yearlevel = semester.year_level
  curriculum = yearlevel.curriculum
  added_subjects = semester.subjects.all()
  subjects= Subject.objects.filter(semesters=semester)
  subject_in_curriculum = curriculum.subjects.all()
  semester_count = Semester.objects.filter(year_level=yearlevel).count()
  yearlevel_count = YearLevel.objects.filter(curriculum=curriculum).count()
  subject_count = semester.subjects.count()
  total_units = added_subjects.aggregate(total_units=Sum('subj_units_lec')+Sum('subj_units_lab'))['total_units']
  
  return render(request, 'PA_Views/curriculum_year_semester.html', {
    'curriculum': curriculum, 
    'subjects':subjects,
    'yearlevel': yearlevel,
    'semester': semester,
    'yearlevel_count': yearlevel_count,
    'subject_count': subject_count,
    'total_units': total_units,
    'added_subjects': added_subjects,
    'semester_count': semester_count,
    'subject_in_curriculum':subject_in_curriculum,

  })



def grade_student(request, user_id):
    student = Student.objects.get(user_id=user_id)
    enrollment = StudentEnrollment.objects.get(student=student)
    curriculum = enrollment.curriculum
    year_level = YearLevel.objects.filter(curriculum=curriculum)
    subjects = Subject.objects.filter(curriculum=curriculum).order_by("year_levels")
    subjectgrade = SubjectGrade.objects.filter(curriculum=curriculum, student=student)

    subject_grade = SubjectGrade.objects.all()


    if request.method == 'POST':
      post_data = request.POST.dict()
      for subject in subjects:
          grade = post_data.get(f'grade-{subject.id}')
          status = post_data.get(f'status-{subject.id}')
          if grade is not None and status is not None:
              subject_grade, created = SubjectGrade.objects.get_or_create(
                  curriculum=curriculum,
                  subject=subject,
                  student=student
              )
              subject_grade.subject_grade = grade
              subject_grade.status = status
              subject_grade.save()

      messages.success(request, 'Grades saved successfully')
      return redirect('grade_student', user_id=user_id)

    return render(request, 'PA_Views/grade_student.html', {
        'student': student,
        'curriculum': curriculum,
        'subjects': subjects,
        'subject_grade':subject_grade,
    })


def curriculum_year_semester_subject_add(request, curriculum_id, subject_id=None):

    curriculum = get_object_or_404(Curriculum, id=curriculum_id)

    if request.method == 'POST':
        subj_code = request.POST['subj_code']
        subj_name = request.POST['subj_name']
        subj_hr_lec = request.POST['subj_hr_lec']
        subj_hr_lab = request.POST['subj_hr_lab']
        subj_units_lec = request.POST['subj_units_lec']
        subj_units_lab = request.POST['subj_units_lab']
        prerequisites = request.POST.getlist('prerequisite[]')
        prerequisites = list(map(int, prerequisites))

        year_level_id = request.POST.get('yearlevels')
        yearlevel = get_object_or_404(YearLevel, id=year_level_id)

        semester_id = request.POST.get('semesters')
        semester = get_object_or_404(Semester, id=semester_id)
        similar_subjects = curriculum.subjects.filter(Q(subj_code=subj_code) | Q(subj_name=subj_name))
        if similar_subjects.exists():
            message = 'Subject already exists'
            messages.error(request, message, extra_tags='danger')
        else:
            subject = Subject.objects.create(
                subj_code=subj_code,
                subj_name=subj_name,
                subj_hr_lec=subj_hr_lec,
                subj_hr_lab=subj_hr_lab,
                subj_units_lec=subj_units_lec,
                subj_units_lab=subj_units_lab,
                added_to_curriculum=True,
            )
            for prereq_id in prerequisites:
              prereq = get_object_or_404(Subject, id=prereq_id)
              subject.prerequisites.add(prereq)

            yearlevel.subjects.add(subject)
            semester.subjects.add(subject)
            curriculum.subjects.add(subject)

            message = 'Subject successfully added'
            messages.success(request, message)

        redirect_url = reverse('curriculum_detail', kwargs={'curriculum_id': curriculum_id})
        return redirect(redirect_url)

    else:
        subject = None
        prerequisites = None

    return render(request, 'PA_Views/curriculum_details.html', {
        'subject': subject,
        'prerequisites': prerequisites,
        'curriculum': curriculum,
    })

def delete_subject(request, id):
  curriculum = get_object_or_404(Curriculum, id=curriculum_id)
  if request.method == 'POST':
    subject = Subject.objects.get(pk=id)
    subject.delete()
  return HttpResponseRedirect(reverse('curriculum_detail', kwargs={'curriculum_id': curriculum_id}))

def edit_subject(request, id):
  if request.method == 'POST':
    subject = Subject.objects.get(pk=id)
    form = SubForm(request.POST, instance=subject)
    if form.is_valid():
      form.save()
      return render(request, 'PA_Views/edit_subject.html', {
        'form': form,
        'success': True
      })
  else:
    subject = Subject.objects.get(pk=id)
    form = SubForm(instance=subject)
  return render(request, 'PA_Views/edit_subject.html', {
    'form': form
  })


def enroll_students(request, curriculum_id):
    curriculum = Curriculum.objects.get(id=curriculum_id)
    students = Student.objects.all()
    if request.method == 'POST':
        student_ids = request.POST.getlist('students')
        for student_id in student_ids:
            student = Student.objects.get(user_id=student_id)
            enrollment, created = StudentEnrollment.objects.get_or_create(student=student, curriculum=curriculum)
            if created:
                messages.success(request, f'{student.user.first_name} enrolled in {curriculum.curriculum_year}')
            else:
                messages.error(request, f'{student.user.first_name} is already enrolled in {curriculum.curriculum_year}')

        return redirect(reverse('curriculum_detail', kwargs={'curriculum_id': curriculum_id}))

    context = {
        'curriculum': curriculum,
        'students': students,
        'yearlevels':YearLevel.objects.filter(curriculum=curriculum).order_by('year_level'),
    }
    return render(request, 'PA_Views/curriculum_details.html', context)

def delete_year_curriculum(request, curriculum_id, yearlevel_id):
    if request.method == 'POST':
        curriculum = get_object_or_404(Curriculum, id=curriculum_id)
        yearlevel = get_object_or_404(YearLevel, id=yearlevel_id)
        yearlevel.delete()
        message = f"Year Level '{yearlevel.year_level}' has been deleted."
        messages.success(request, message)
        redirect_url = reverse('curriculum_detail', kwargs={'curriculum_id': curriculum_id})
        redirect_url += f'?message={message}'
        return redirect(redirect_url)
    return HttpResponseRedirect(reverse('curriculum_detail', kwargs={'curriculum_id': curriculum_id}))






