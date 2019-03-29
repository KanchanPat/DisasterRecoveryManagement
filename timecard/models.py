from django.db import models
from datetime import datetime

# Create your models here.


class Timecard(models.Model):
    site_code = models.CharField(max_length=50, null=False)
    contractor_name = models.CharField(max_length=50, null=False)
    date = models.DateTimeField(null=False, default=datetime.now())
    status = models.CharField(choices=((0, 'open'), (1, 'review'), (2, 'Finallized')),default='',max_length=10)
    total_hours = models.IntegerField(default=0)
    total_amount = models.IntegerField(default=0)


class Job(models.Model):
    job_code = models.CharField(max_length=10, null=False)
    description = models.CharField(max_length=100, null=False)
    hourly_rate = models.IntegerField(default=0)
    max_hour_perday = models.IntegerField(null=False)


class Machine(models.Model):
    machine_code = models.CharField(max_length=10, null=False)
    description = models.CharField(max_length=100, null=False)
    hourly_rent = models.IntegerField(default=0)
    max_hour_perday = models.IntegerField(null=False)


class Timecard_Details(models.Model):
    sitecode_id = models.ForeignKey(Timecard, on_delete='casscade')
    code = models.models.CharField(max_length=50, null=False)
    code_type = models.CharField(choices=(('J', 'job_code'), ('M', 'machine_code')), default='',max_length=10)
    hours = models.IntegerField(default=0)

