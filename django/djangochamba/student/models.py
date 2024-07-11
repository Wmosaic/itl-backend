from django.db import models
from djangochamba.models import SoftDeleteModel
from djangochamba.user.models import User

class Student(SoftDeleteModel):
    class Meta:
        default_permissions = ()
        verbose_name        = "Student"
        verbose_name_plural = "Students"

    user                 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    semester             = models.IntegerField()
    social_service_hours = models.IntegerField()
    extra_activity       = models.CharField(max_length=30) 
