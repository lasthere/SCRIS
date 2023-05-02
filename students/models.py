from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Subject(models.Model):
    subj_code = models.CharField(max_length=10)
    subj_name = models.CharField(max_length=255)
    subj_hr_lec = models.FloatField(max_length=10, default=0.0)
    subj_hr_lab = models.FloatField(max_length=10, default=0.0)
    subj_units_lec = models.FloatField(max_length=10, default=0.0)
    subj_units_lab = models.FloatField(max_length=10, default=0.0)
    added_to_curriculum = models.BooleanField(default=False)
    prerequisites = models.ManyToManyField('self', symmetrical=False, blank=True)

class Curriculum(models.Model):
  id = models.AutoField(primary_key=True)
  curriculum_year = models.CharField(max_length=200, verbose_name="Curriculum Year")
  subjects=models.ManyToManyField(Subject)
  def __str__(self):
    return self.curriculum_year

class YearLevel(models.Model):
  year_level = models.IntegerField()
  curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE, related_name='year_levels')
  subjects = models.ManyToManyField(Subject, related_name='year_levels')


class Semester(models.Model):
  semester = models.IntegerField()
  year_level = models.ForeignKey(YearLevel, on_delete=models.CASCADE, related_name='semesters')
  subjects = models.ManyToManyField(Subject, related_name='semesters')

  def __str__(self):
    return f"{self.year_level} - {self.get_semester_display()}"

class CustomUser(AbstractUser):
  user_type_data = ((1, "Hod"), (2, "PA"), (3, "Students"),(4, "Ojt_Officer"))
  user_type = models.CharField(default=1, choices=user_type_data, max_length=10)



class Student(models.Model):
  user = models.OneToOneField(CustomUser,on_delete =models.CASCADE, primary_key=True)
  student_number = models.CharField(max_length=50, null=True,blank=True)
  middle_initial = models.CharField(max_length=2, null=True, blank=True)
  year_level = models.CharField(max_length=50)
  curriculums = models.ManyToManyField(Curriculum, blank=True, related_name='students')
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

class SubjectGrade(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    curriculum =models.ForeignKey(Curriculum,on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='grades')
    subject_grade = models.FloatField(blank=True, null=True,  default=1.0)
    STATUS_CHOICES = [
        ("passed", "Passed"),
        ("failed", "Failed"),
        ("incomplete", "Incomplete"),
        ("dropped", "Dropped"),
        ("noattendance", "No Attendance"),
        ("nograde", "No Grade")
    ]
    status = models.CharField(blank=True, null=False,max_length=12, choices=STATUS_CHOICES)
    objects = models.Manager()

    def save(self, *args, **kwargs):
      if self.status == 'nograde' or self.status == 'dropped' or self.status == 'noattendance':
          self.subject_grade = 0.0
      elif self.status == 'incomplete':
          self.subject_grade = 4.0
      elif self.status == 'failed':
          self.subject_grade = 5.0
      elif self.subject_grade and float(self.subject_grade) >= 1.0 and float(self.subject_grade) <= 3.0:
          self.status = 'passed'
      elif self.subject_grade and float(self.subject_grade) >= 3.1 and float(self.subject_grade) <= 5.0:
          self.status = 'failed'   
      super().save(*args, **kwargs)

class StudentEnrollment(models.Model):
  student = models.ForeignKey(Student, on_delete=models.CASCADE)
  curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE)



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