from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Task(models.Model):
    # very simple juct the name and check if the task is done or not
    name = models.CharField(max_length=100)
    is_done = models.BooleanField(default = False)