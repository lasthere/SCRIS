from django import forms 
from django.forms import Form
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import UserCreationForm
from .models import Student, Ojt_Officer, Dept_Head, ProgramAdvisor, Subject, CustomUser, SubjectGrade, Curriculum, Prerequisite



choice =(
    ("1", "I"),
    ("2", "II"),
    ("3", "III"),
    ("4", "IV"),
)
choices =(
    ("1", "1st"),
    ("2", "2nd"),
    ("3", "3rd"),
    ("4", "4th"),
)

class StudentSearchForm(forms.Form):
  query = forms.CharField(label='Search', max_length=100, required=False)
  submit = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

class StudentForm(forms.Form):
  student_number = forms.CharField(label='student_number:',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder':'Username/StudentID:',
                'id': 'student_number'
            }
        ),
    )
  password = forms.CharField(label='password:',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder':'Password:',
                'id': 'password'
            }
        ),
    )
  email = forms.CharField(label='email:',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder':'Email:',
                'id': 'email'
            }
        ),
    )
  first_name = forms.CharField(label='first_name:',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder':'First Name:',
                'id': 'first_name'
            }
        ),
    )
  last_name = forms.CharField(label='last_name:',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder':'Last Name:',
                'id': 'last_name'
            }
        ),
    )
  middle_initial = forms.CharField(label='middle_initial:',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder':'Middle Intial:',
                'id': 'middle_initial'
            }
        ),
    )

  year_level = forms.ChoiceField(
        label='Year Level:',
        widget=forms.Select(
            attrs={
                'class': 'form-select',
                'id': 'year_level'
            }
        ),
        choices=[('1', 'First Year'), ('2', 'Second Year'), ('3', 'Third Year'), ('4', 'Fourth Year')]
    )


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

class PrerequisiteForm(forms.ModelForm):
    prerequisites = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        label="Prerequisites",
    )
    prerequisite = forms.CharField(max_length=50, label="Additional Prerequisite", required=False)

    class Meta:
        model = Prerequisite
        fields = ('prerequisite', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['prerequisites'].initial = self.instance.subject_set.all()

    def save(self, commit=True):
        prerequisite = super().save(commit=False)
        if commit:
            prerequisite.save()
        if self.cleaned_data['prerequisites']:
            prerequisite.subject_set.set(self.cleaned_data['prerequisites'])
        return prerequisite

class SubForm(forms.ModelForm):
  
  class Meta:
    model = Subject
    fields = ['subj_code', 'subj_name','subj_hr_lec','subj_units_lec', 'subj_hr_lab', 'subj_units_lab']

    widgets = {
      'subj_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Subject Code:'}),
      'subj_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Subject Name:'}),
      'subj_hr_lec': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'Hours Lecture:'}),
      'subj_units_lec': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'Units Lecture:'}),  
      'subj_hr_lab': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'Hours Laboratory:'}), 
      'subj_units_lab': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'Units Laboratory:'}), 
      
    }
    labels = {
      'subj_code': 'Subject Code', 
      'subj_name': 'Subject Name', 
      'subj_hr_lec': 'Hours Lec', 
      'subj_units_lec': 'Units Lec',
      'subj_hr_lab': 'Hours Lab',  
      'subj_units_lab': 'Units Lab', 
      
    }

class GradeForm(forms.ModelForm):

  subject_grade = forms.FloatField(min_value=1.0, max_value=5.0)
 
  class Meta:
    model = SubjectGrade
    fields = ['subject_id', 'student_id', 'subject_grade','status']

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
    clean_score
    clean_status

class CurriculumForm(forms.ModelForm):
  curriculum_year= forms.CharField(label="Curriculum Name: ",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Curriculum Name:'}))
  semester = forms.ChoiceField(
        label='Semester:',
        widget=forms.Select(
            attrs={
                'class': 'form-select',
                'id': 'year_level'
            }
        ),
        choices=[('1', 'First Semester'), ('2', 'Second Semester'),]
    )
  year_level = forms.ChoiceField(
        label='Year Level:',
        widget=forms.Select(
            attrs={
                'class': 'form-select',
                'id': 'year_level'
            }
        ),
        choices=[('1', 'First Year'), ('2', 'Second Year'), ('3', 'Third Year'), ('4', 'Fourth Year')]
    )

  class Meta:
    model=Curriculum
    fields=['curriculum_year', 'semester', 'year_level']




class AddSubjectForm(forms.Form):
  subjects = forms.ModelMultipleChoiceField(
    queryset=Subject.objects.all(),
    widget=forms.SelectMultiple (attrs={
      'class': 'form-select form-floating',
      'placeholder': ' Select Subject',
      'aria-label': 'multiple select example',
        }),
    )

  def __init__(self, added_subjects, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['subjects'].queryset = Subject.objects.exclude(
      id__in=[s.id for s in added_subjects]
        )


