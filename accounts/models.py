from django.db import models
from tasks.models import Task
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    # just two fiels the one for the User and the other one for the tasks
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    tasks = models.ManyToManyField(Task)
