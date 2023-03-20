from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Student,ProgramAdvisor,Dept_Head,Ojt_Officer,Subject,SubjectGrade,Prereq,CustomUser

# Register your models here.
class UserModel(UserAdmin):
    pass


admin.site.register(CustomUser, UserModel)


#admin.register(Student)

#admin.register(ProgramAdvisor)
#admin.register(Dept_Head)
#admin.register(Ojt_Officer)
#admin.register(Subject)
#admin.register(SY)
#admin.register(SubjectGrade)
#admin.register(OjtStatus)
#admin.register(Prereq)
#admin.register(TotalUnits)


