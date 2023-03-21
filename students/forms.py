from django import forms 
from django.forms import Form
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import UserCreationForm
from .models import Student, Ojt_Officer, Dept_Head, ProgramAdvisor, Subject, CustomUser, SubjectGrade



choice =(
    ("FRESHMAN", "Freshmen"),
    ("SOPHOMORE", "Sophomore"),
    ("JUNIOR", "Junior"),
    ("SENIOR", "Senior"),
)

sem =(
    ("First Sem", "First Semester"),
    ("Second Sem", "Second Semester"),
)

yer =(
    ("I", "Freshmen"),
    ("II", "Sophomore"),
    ("III", "III"),
    ("IV", "IV"),
)

class StudentForm(forms.Form):
  student_number = forms.CharField(label="Student Number", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
  password = forms.CharField(label="Password", max_length=50, widget=forms.PasswordInput(attrs={"class":"form-control"}))
  email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class":"form-control"}))
  first_name = forms.CharField(label="first_name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
  last_name = forms.CharField(label="last_name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
  middle_initial = forms.CharField(label="middle_initial", max_length=2,  widget=forms.TextInput(attrs={"class":"form-control"}))
  year_level = forms.ChoiceField(choices=choice, widget=forms.Select(attrs={"class":"form-control"}))

class PaForm(forms.ModelForm):
  class Meta:
    model=CustomUser
    fields = ('username','password','first_name', 'last_name', 'email')
    username = forms.CharField(label="Username",  widget=forms.TextInput(attrs={"class":"form-control"}))
    password = forms.CharField(label="Password",  widget=forms.PasswordInput(attrs={"class":"form-control"}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label="first_name", widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label="last_name", widget=forms.TextInput(attrs={"class":"form-control"}))

class EditStudentFormUser(forms.ModelForm):
  class Meta:
    model=CustomUser
    fields = ('username','password','first_name', 'last_name', 'email')
    username = forms.CharField(label="username", max_length=50,  widget=forms.TextInput(attrs={"class":"form-control 'readonly'"}))
    password = forms.CharField(label="Password", max_length=50,  widget=forms.PasswordInput(attrs={"class":"form-control"}))
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label="first_name",max_length=50,  widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label="last_name",max_length=50,  widget=forms.TextInput(attrs={"class":"form-control"}))

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.password = make_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class EditProfile(forms.ModelForm):
  class Meta:
    model=CustomUser
    fields = ('password','email')
    password = forms.CharField(label="Password", max_length=50,  widget=forms.PasswordInput(attrs={"class":"form-control"}))
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class":"form-control"}))
    
    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.password = make_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return use


class EditStudentForm(forms.ModelForm):
  class Meta:
    model=Student
    fields = ('middle_initial','year_level')
    middle_initial = forms.CharField(label="middle_initial", max_length=2, widget=forms.TextInput(attrs={"class":"form-control" 'readonly'}))
    year_level = forms.ChoiceField(choices=choice, widget=forms.Select(attrs={"class":"form-control"}))

   

class OjtForm(forms.ModelForm):
  class Meta:
    model=CustomUser
    fields = ('username','password','first_name', 'last_name', 'email')
    username = forms.CharField(label="Username",max_length=50, widget=forms.TextInput(attrs={"class":"form-control" }))
    password = forms.CharField(label="Password",max_length=50,   widget=forms.PasswordInput(attrs={"class":"form-control"}))
    email = forms.EmailField(label="Email",max_length=50,  widget=forms.EmailInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label="first_name",max_length=50,  widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label="last_name",max_length=50,  widget=forms.TextInput(attrs={"class":"form-control"}))

class EditOjtForm(forms.ModelForm):
  class Meta:
    model=CustomUser
    fields = ('username','password','first_name', 'last_name', 'email')
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={"class":"form-control"}))
    password = forms.CharField(label="Password",  widget=forms.PasswordInput(attrs={"class":"form-control"}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label="first_name", widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label="last_name", widget=forms.TextInput(attrs={"class":"form-control"}))

class HodForm(forms.ModelForm):
  class Meta:
    model=CustomUser
    fields = ('username','password','first_name', 'last_name', 'email')
    username = forms.CharField(label="Username",  widget=forms.TextInput(attrs={"class":"form-control"}))
    password = forms.CharField(label="Password",  widget=forms.PasswordInput(attrs={"class":"form-control"}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label="first_name", widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label="last_name", widget=forms.TextInput(attrs={"class":"form-control"}))




class SubForm(forms.ModelForm):
  class Meta:
    model = Subject
    fields = ['subj_code', 'subj_name','subj_hr_lec','subj_units_lec', 'subj_hr_lab', 'subj_units_lab','prerequisite','yearlevel','semester_in_school', 'school_year']
    labels = {
      'subj_code': 'Subject Code', 
      'subj_name': 'Subject Name', 
      'subj_hr_lec': 'Hours Lec', 
      'subj_units_lec': 'Units Lec',
      'subj_hr_lab': 'Hours Lab',  
      'subj_units_lab': 'Units Lab', 
      'prerequisite': 'Prerequiste',
      'yearlevel': 'Year Level', 
      'school_year': 'S.Y.', 
      'semester_in_school': 'Semester', 
      
    }
    widgets = {
      'subj_code': forms.TextInput(attrs={'class': 'form-control'}),
      'subj_name': forms.TextInput(attrs={'class': 'form-control'}),
      'subj_hr_lec': forms.NumberInput(attrs={'class': 'form-control'}),
      'subj_units_lec': forms.NumberInput(attrs={'class': 'form-control'}),  
      'subj_hr_lab': forms.NumberInput(attrs={'class': 'form-control'}), 
      'subj_units_lab': forms.NumberInput(attrs={'class': 'form-control'}), 
      'prerequisite': forms.TextInput(attrs={'class': 'form-control'}),
      'yearlevel': forms.Select(choices=yer,attrs={'class': 'form-control'}),
      'school_year': forms.TextInput(attrs={'class': 'form-control'}),
      'semester_in_school': forms.Select(choices=sem,attrs={'class': 'form-control',}),
      
    }

class GradeForm(forms.ModelForm):

  subject_grade = forms.FloatField(min_value=1.0, max_value=5.0)
 
  class Meta:
    model = SubjectGrade
    fields = ['subject_id','student_id', 'subject_grade','status']


    def clean_score(self):
      grade = self.cleaned_data['subject_grade']
      if grade < 0.0 or grade >= 5.0:
        raise forms.ValidationError('Score must be between 0 and 5.')
      return grade

    def clean_status(self):
      status = self.cleaned_data['status']
      score = self.cleaned_data['subject_grade']
      if (status is None) and (score <= 3.0) :
        status = 'Pass'
      else:
        status = 'Fail'
      return status

    clean_status
    clean_score
