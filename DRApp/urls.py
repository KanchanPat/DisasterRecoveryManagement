"""DRApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views]--[=]==]=-----==\
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from timecard import views
from timecard.views import JobList, JobUpdate, JobCreate, JobDelete, TimeCardList
from timecard.views import MachineList, MachineCreate, MachineUpdate, MachineDelete

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('job_management/', JobList.as_view(), name='job_management'),
    path('job_update/<int:pk>/', JobUpdate.as_view(), name='job_update'),
    path('job_create/', JobCreate.as_view(), name='job_create'),
    path('job_delete/<int:pk>/', JobDelete.as_view(), name='job_delete'),
    path('machine_management/', MachineList.as_view(), name='machine_management'),
    path('machine_update/<int:pk>/', MachineUpdate.as_view(), name='machine_update'),
    path('machine_create/', MachineCreate.as_view(), name='machine_create'),
    path('machine_delete/<int:pk>/', MachineDelete.as_view(), name='machine_delete'),
    path('timecard_approval/', TimeCardList.as_view(), name='timecard_approval' ),
    path('timecard/',views.create_timecard,name='timecard'),
    #path('timecarddetails/',views.create_timecarddetails,name='timecarddetails'),
]
