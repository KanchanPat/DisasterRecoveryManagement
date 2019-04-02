from django.contrib import admin
from django.urls import path
from django.views.generic import ListView

from timecard import views
from timecard.models import Job

urlpatterns = [
    path('',views.create_timecard,name='timecard'),
    path('job/',ListView.as_view(queryset=Job.objects.all(),
                                context_object_name='jobListContext',
                                template_name='timecard/job_codes.html'),
                                name='job_codes'),


]
