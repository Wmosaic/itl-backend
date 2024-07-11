from django.db import models
from djangochamba.student.models import Student
from djangochamba.professor.models import Professor
from djangochamba.models import SoftDeleteModel

class Classroom(SoftDeleteModel):
    class Meta:
        default_permissions = ()
        verbose_name        = "Classroom"
        verbose_name_plural = "Classrooms"

    classroom_number = models.CharField(max_length=5, blank=False)

class Student_Classroom(SoftDeleteModel):
    class Meta:
        default_permissions = ()
        verbose_name        = "Student_Classroom_Record"
        verbose_name_plural = "Student_Classroom_Records"

    student   = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="student_classrooms")
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name="student_classrooms")
    
class Professor_Classroom(SoftDeleteModel):
    class Meta:
        default_permissions = ()
        verbose_name        = "Professor_Classroom_Record"
        verbose_name_plural = "Professor_Classroom_Records"


    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name="professor")
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name="classroom")
