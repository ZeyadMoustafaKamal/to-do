# Generated by Django 4.1.6 on 2023-02-23 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_userprofile_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='code',
            field=models.IntegerField(default=0),
        ),
    ]
