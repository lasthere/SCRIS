from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import transaction

from django.conf import settings
from django.core.mail import EmailMultiAlternatives, BadHeaderError, send_mail, send_mass_mail
import smtplib

from students.UsernameBackEnd import UsernameBackEnd

from .models import CustomUser, Student, Ojt_Officer, Dept_Head, ProgramAdvisor, Subject, SubjectGrade
from .forms import StudentForm, OjtForm, HodForm, PaForm, SubForm,EditStudentForm,EditStudentFormUser,EditOjtForm,GradeForm

# Create your views here.
# Login

def login(request):
  return render(request,'login.html')

def doLogin(request):
     
    username = request.GET.get('username')
    password = request.GET.get('password')
    # user_type = request.GET.get('user_type')
    if not (username and password):
        messages.error(request, "Please provide all the details!!")
        return render(request, 'login.html')
 
    user = CustomUser.objects.filter(username=username, password=password).last()
    if not user:
        messages.error(request, 'Invalid Login Credentials!!')
        return render(request, 'login.html')
 
    login(request, user)
 
    if user.user_type == CustomUser.Students:
        return redirect('student_index/')
    elif user.user_type == CustomUser.PA:
        return redirect('student/')
    elif user.user_type == CustomUser.Hod:
        return redirect('admin/')
 
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')
# Students

def index(request):
  return render(request, 'PA_Views/index.html', {
    'students': Student.objects.all()

  })

def view_student(request, id):
  student = Student.objects.get(pk=id)
  return HttpResponseRedirect(reverse('index'))

def student_grades(request, user_id):
    student = Student.objects.get(user_id=user_id)
    grades = SubjectGrade.objects.filter(student_id=student)
    return render(request, 'PA_Views/student_grade.html', {'student': student, 'grades': grades, })

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
      messages.success(request, "Student Added Successfully!")
      return render(request, 'PA_Views/add.html', {
        'form': StudentForm(),
        'success': True
      })
  else:
    return render(request, 'PA_Views/add.html', {
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

def delete(request, id):
  if request.method == 'POST':
    student = Student.objects.get(pk=id)
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
    hod = Dept_Head.objects.get(pk=id)
    hod.delete()
  return HttpResponseRedirect(reverse('hod_list'))

def edit_hod(request, id):
  if request.method == 'POST':
    hod = Dept_Head.objects.get(pk=id)
    form = HodForm(request.POST, instance=hod)
    if form.is_valid():
      form.save()
      return render(request, 'PA_Views/edit_hod.html', {
        'form': form,
        'success': True
      })
  else:
    hod = Dept_Head.objects.get(pk=id)
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


      new_PA = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=1)
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
    pa = ProgramAdvisor.objects.get(pk=id)
    pa.delete()
  return HttpResponseRedirect(reverse('pa_list'))

def edit_pa(request, id):
  if request.method == 'POST':
    pa = ProgramAdvisor.objects.get(pk=id)
    form = PaForm(request.POST, instance=pa)
    if form.is_valid():
      form.save()
      return render(request, 'PA_Views/edit_pa.html', {
        'form': form,
        'success': True
      })
  else:
    pa = ProgramAdvisor.objects.get(pk=id)
    form = PaForm(instance=pa)
  return render(request, 'PA_Views/edit_pa.html', {
    'form': form
  })

     #Subjects

def subject_list(request):
  return render(request, 'PA_Views/subject_list.html', {
    'subs': Subject.objects.all()
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
      new_school_year = form.cleaned_data['school_year']
      new_semester_in_school = form.cleaned_data['semester_in_school']
      new_yearlevel = form.cleaned_data['yearlevel']

      new_Subj= Subject(
        subj_code = new_subj_code,
        subj_name = new_subj_name,
        subj_hr_lec = new_subj_hr_lec,
        subj_hr_lab = new_subj_hr_lab,
        subj_units_lec = new_subj_units_lec,
        subj_units_lab = new_subj_units_lab,
        prerequisite = new_prerequisite,
        school_year = new_school_year,
        semester_in_school = new_semester_in_school,
        yearlevel = new_yearlevel,

      )
      new_Subj.save()
      return render(request, 'PA_Views/add_subject.html', {
        'form': SubForm(),
        'success': True
      })
  else:
    form = SubForm()
  return render(request, 'PA_Views/add_subject.html', {
    'form': SubForm()
  })

def delete_subject(request, id):
  if request.method == 'POST':
    subject = Subject.objects.get(pk=id)
    subject.delete()
  return HttpResponseRedirect(reverse('subject_list'))

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
    message += "Click Link: http://127.0.0.1:8000/"

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
  return render(request,'ojt_view/index.html',{
    "students": Student.objects.all()
    })

def ojt_view_students(request, id):
  subject = Student.objects.get(pk=id)
  return HttpResponseRedirect(reverse('index'))



#student views

def student_index(request):
  return render(request,'student_view/index.html',{
    "students": Student.objects.all(),
    'subs': Subject.objects.all()
    })




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

def add_grade(request):
  if request.method == 'POST':
    form = GradeForm(request.POST)
    if form.is_valid():
      subject_id = form.cleaned_data['subject_id']
      student_id = form.cleaned_data['student_id']
      subject_grade = form.cleaned_data['subject_grade']
      status = form.cleaned_data['status']

      newgrade= SubjectGrade(
        subject_id = subject_id,
        student_id = student_id,
        subject_grade = subject_grade,
        status = status,

        )
      newgrade.save()
      
      return render(request, 'PA_Views/add_grade.html', {
        'form': GradeForm(),
        'success': True
      })
  else:
    form = GradeForm()
  return render(request, 'PA_Views/add_grade.html', {
    'form': GradeForm()
  })

