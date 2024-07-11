from django.db import models
from djangochamba.models import SoftDeleteModel
from djangochamba.user.models import User

class Professor(SoftDeleteModel):
    class Meta:
        default_permissions = ()
        verbose_name        = "Professor"
        verbose_name_plural = "Professors"

    user   = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    title  = models.CharField(max_length=50, blank=False)
    hours  = models.IntegerField()
    salary = models.FloatField()
    
