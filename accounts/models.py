from django.db import models
from tasks.models import Task
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    code = models.IntegerField(default = 0)
    verified = models.BooleanField(default = False)
    tasks = models.ManyToManyField(Task)
