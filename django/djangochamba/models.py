from django.db import models
from django.utils import timezone

class SoftDeleteModel(models.Model):
    class Meta: 
        abstract = True
        
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField()

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def recover(self):
        self.deleted_at = None
        self.save()

    def hard_delete(self):
        super(SoftDeleteModel,self).delete()
