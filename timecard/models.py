from django.db import models
from datetime import datetime
from django.urls import reverse
# Create your models here.

class Job(models.Model):
    job_code = models.CharField(max_length=25, null=False)
    description = models.CharField(max_length=100, null=False)
    hourly_rate = models.IntegerField(default=0)
    max_hour_perday = models.IntegerField(null=False)

    def get_absolute_url(self):
        return reverse('job_management', kwargs={'pk': self.pk})

    def __str__(self):
        return self.job_code


class Machine(models.Model):
    machine_code = models.CharField(max_length=25, null=False)
    description = models.CharField(max_length=100, null=False)
    hourly_rent = models.IntegerField(default=0)
    max_hour_perday = models.IntegerField(null=False)

    def get_absolute_url(self):
        return reverse('machine_management', kwargs={'pk': self.pk})

    def __str__(self):
        return self.machine_code

class Timecard(models.Model):
    site_code = models.CharField(max_length=50, null=False)
    contractor_name = models.CharField(max_length=50, null=False)
    date = models.DateTimeField(null=False, default=datetime.now())
    status = models.CharField(choices=((0, 'open'), (1, 'review'), (2, 'Finallized')),default='',max_length=10)
    total_hours = models.IntegerField(default=0)
    total_amount = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('timecard_management', kwargs={'pk': self.pk})

    def __str__(self):
        return self.site_code


class JobEntry(models.Model):
    job_code = models.ForeignKey(Job, on_delete='casscade')
    hours_worked = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    site_code = models.CharField(max_length=50)

class MachineEntry(models.Model):
    machine_code = models.ForeignKey(Machine, on_delete='casscade')
    hours_used = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    site_code = models.CharField(max_length=50)




#
# class Timecard_Details(models.Model):
#     sitecode_id = models.CharField(max_length=50)
#     contractor_name = models.CharField(max_length=50, null=False, default='')
#     date = models.DateTimeField(null=False, default=datetime.now())
#     #status = models.CharField(choices=((0, 'open'), (1, 'review'), (2, 'Finallized')), default='', max_length=10)
#     # code = models.CharField(max_length=50, null=False)
#     # code_type = models.CharField(choices=(('J', 'job_code'), ('M', 'machine_code')), default='',max_length=10)
#     job_code = models.ForeignKey(Job,on_delete='casscade',default=None)
#     machine_code = models.ForeignKey(Machine,on_delete='casscade',default=None)
#     job_hours = models.IntegerField(default=0)
#     machine_hours = models.IntegerField(default=0)





