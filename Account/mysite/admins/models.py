from django.db import models
from django.utils import timezone


import json
from django.db import models
from django.utils import timezone
from django.core.mail import send_mail


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,editable=False)
    updated_at = models.DateTimeField(auto_now=True,editable=True)

    class Meta:
        abstract = True


class Admins(BaseModel):
    admin_id = models.AutoField(primary_key=True)
    admin_email = models.EmailField(max_length=55, unique=True)
    username = models.CharField(max_length=55, unique=True)
    password = models.CharField(max_length=255)


    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super(Admins, self).save(*args, **kwargs)

    def __str__(self):
        return self.username
