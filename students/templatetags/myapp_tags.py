# myapp/templatetags/myapp_tags.py
from django import template
from django.shortcuts import get_object_or_404
from students.models import SubjectGrade


register = template.Library()

@register.simple_tag
def calculate_total_units_semester(semester):
    total_units_semester = 0
    for subject in semester.subjects.all():
        subj_units_lec = subject.subj_units_lec or 0
        subj_units_lab = subject.subj_units_lab or 0
        total_units_semester += subj_units_lec + subj_units_lab
    return total_units_semester

@register.filter
def get_by_id(queryset, id):
    return get_object_or_404(queryset, id=id)

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter(name='has_objects')
def has_objects(queryset):
    return bool(queryset)

@register.filter(name='get_subject_grade')
def get_subject_grade(student, subject):
    subject_grade = SubjectGrade.objects.get(student=student, subject=subject)
    return subject_grade.subject_grade

@register.filter(name='has_grade')
def has_grade(student, subject):
    try:
        grade = SubjectGrade.objects.get(student=student, subject=subject)
        return True
    except SubjectGrade.DoesNotExist:
        return False
        
@register.filter(name='has_grade_any')
def has_grade_any(student, subjects):
    for subject in subjects:
        if SubjectGrade.objects.filter(student=student, subject=subject).exists():
            return True
    return False


@register.simple_tag
def get_subject_status(subject, status):
    try:
        return subject.subjectgrade_set.get(status=status).status
    except SubjectGrade.DoesNotExist:
        return None

@register.filter(name='get_subject_status')
def get_subject_status(student, subject):
    subject_grade = SubjectGrade.objects.get(student=student, subject=subject)
    return subject_grade.status

@register.simple_tag
def get_all_prerequisites(subject, student):
    prerequisites = subject.prerequisite_set.all()
    html = ''
    for prerequisite in prerequisites:
        related_subjects = prerequisite.related_subjects.all()
        if related_subjects:
            html += '<br>'
            for related_subject in related_subjects:
                if student.get_subject_status(related_subject) == 'failed':
                    html += f'<p>{related_subject.subj_code} (failed)</p>'
                else:
                    html += f'<p>{related_subject.subj_code}</p>'
                html += get_all_prerequisites(related_subject, student)
    return html

