from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Subject(models.Model):
  id = models.AutoField(primary_key=True)
  class YearLvl(models.TextChoices):
    FRESHMAN = 'I', _('Freshman')
    SOPHOMORE = 'II', _('Sophomore')
    JUNIOR = 'III', _('Junior')
    SENIOR = 'IV', _('Senior')

  class SchlSemester(models.TextChoices):
    first_sem = 'First Sem', _('First Semester')
    second_sem = 'Second Sem', _('Second Semester')

  subj_code = models.CharField(max_length=10)
  subj_name = models.CharField(max_length=255)
  subj_hr_lec = models.FloatField(max_length=10, default=0.0)
  subj_hr_lab = models.FloatField(max_length=10, default=0.0)
  subj_units_lec = models.FloatField(max_length=10, default=0.0)
  subj_units_lab =  models.FloatField(max_length=10, default=0.0)
  prerequisite = models.CharField(blank=True,max_length=50)
  semester_in_school = models.CharField(max_length=20, choices=SchlSemester.choices,default=SchlSemester.first_sem)
  school_year = models.CharField(max_length=50, default="2023-2024")
  yearlevel = models.CharField(max_length=3,choices=YearLvl.choices,default=YearLvl.FRESHMAN)
  objects = models.Manager()

  def __str__(self):
    return f'{self.subj_code},  {self.subj_name} '


class CustomUser(AbstractUser):
  user_type_data = ((1, "Hod"), (2, "PA"), (3, "Students"),(4, "Ojt_Officer"))
  user_type = models.CharField(default=1, choices=user_type_data, max_length=10)



class Student(models.Model):
  user = models.OneToOneField(CustomUser,on_delete =models.CASCADE, primary_key=True)
  student_number = models.CharField(max_length=50, null=True,blank=True)
  middle_initial = models.CharField(max_length=2, null=True, blank=True)
  year_level = models.CharField(max_length=50)
  subject = models.ManyToManyField(Subject, through="SubjectGrade")
  objects = models.Manager()

  def __str__(self):
    return f'{self.user.first_name} Year Level: {self.year_level} '

class ProgramAdvisor(models.Model):
  user = models.OneToOneField(CustomUser,on_delete =models.CASCADE, primary_key=True)
  teacher_id = models.IntegerField(null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = models.Manager()

class Dept_Head(models.Model):
  user = models.OneToOneField(CustomUser,on_delete =models.CASCADE, primary_key=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = models.Manager()

class Ojt_Officer(models.Model):
  user = models.OneToOneField(CustomUser,on_delete =models.CASCADE, primary_key=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = models.Manager()



#ang sa tables na nin dapita





class Prereq(models.Model):
  id = models.AutoField(primary_key=True)
  subject_id =models.ForeignKey(Subject, on_delete=models.CASCADE,null=True, verbose_name="Sub")
  prerequisite =models.ManyToManyField(Subject, related_name='Subject_prerequisite')
  objects = models.Manager()


  def get_absolute_url(self):
    return reverse('Prereq-details',args[str(self.id)])


  def get_prerequisite(self):
    return "\n".join([p.prerequisite for p in self.prerequisite.all()])

#grading system

class SubjectGrade(models.Model):
  id = models.AutoField(primary_key=True)
  subject_id =models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Subject")
  student_id = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Students")
  subject_grade = models.FloatField(null=True, blank=True, default=1.0)
  status = models.CharField(max_length=12,blank=True,null=False,choices=[("passed", "Passed"), ("failed", "Failed"), ("incomplete", "Incomplete"), ("dropped", "Dropped"), ("noattendance", "No Attendance")])
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = models.Manager()

  def save(self, *args, **kwargs):

    if (self.status == "incomplete") or (self.status == "dropped") or (self.status == "noattendance"):
       self.subject_grade = None
    else:
      if(self.status is None) or ((self.subject_grade >= 1.0) and (self.subject_grade <= 3.0 )):
        self.status ="passed"
      else:
        self.status="failed"

    super().save(*args, **kwargs)

  def __str__(self):
    return f'Student Suject Grades:{self.student_id}, {self.subject_grade}, {self.status}'

class TotalUnits(models.Model):
  studentgrade_id =models.ForeignKey(SubjectGrade, on_delete=models.CASCADE, verbose_name="Subject Grades")
  totalgrades = models.FloatField(max_length=5, default=0)
  totalunits = models.FloatField(max_length=5, default=0)
  objects = models.Manager()

  def get_absolute_url(self):
    return reverse('TotalUnits-details',args[str(self.id)])
  def __str__(self):
    return f'Student Total Grades:{self.studentgrade_id}, {self.totalgrades}, {self.totalunits}'

class OjtStatus(models.Model):
  id = models.AutoField(primary_key=True)
  class Rem(models.TextChoices):
    PASSED ='Passed', _('Passed')
    FAILED = 'Failed', _('Failed')
    INC = 'Incomplete', _('Incomplete')
    DROPPED = 'Dropped', _('Dropped')
    NOATTENDANCE= 'NoAttendance', _('No Attendance')
  studentgrade_id =models.ForeignKey(SubjectGrade, on_delete=models.CASCADE)
  totalunits_id =models.ForeignKey(TotalUnits, on_delete=models.CASCADE)
  ojt_remarks =models.CharField(max_length=20, choices=Rem.choices, default=Rem.FAILED, verbose_name="Remarks")
  objects = models.Manager()
  def get_absolute_url(self):
    return reverse('OjtStatus-details',args[str(self.id)])

  def __str__(self):
    return f'Student Status: {self.totalunits_id}, {self.ojt_remarks} '

@receiver(post_save, sender=CustomUser)
# Now Creating a Function which will automatically insert data in HOD, Staff or Student
def create_user_profile(sender, instance, created, **kwargs):
  if created:
    if instance.user_type == 1:
      Dept_Head.objects.create(user=instance)
    if instance.user_type == 2:
      ProgramAdvisor.objects.create(user=instance)
    if instance.user_type == 3:
      Student.objects.create(user=instance)
    if instance.user_type == 4:
      Ojt_Officer.objects.create(user=instance)
    

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
  if instance.user_type == 1:
    instance.Dept_Head.save()
  if instance.user_type == 2:
    instance.programadvisor.save()
  if instance.user_type == 3:
    instance.student.save()
  if instance.user_type == 4:
    instance.ojt_officer.save()