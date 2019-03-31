from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls.base import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from timecard.models import Timecard, Job, Machine
from django.shortcuts import get_object_or_404


@method_decorator(login_required, name='dispatch')
class TimeCardList(ListView):
    model = Timecard
    context_object_name = 'time_card_list'
    template_name = 'test.html'


@method_decorator(login_required, name='dispatch')
class JobList(ListView):
    model = Job
    context_object_name = 'job_list'
    template_name = 'test.html'


@method_decorator(login_required, name='dispatch')
class JobUpdate(UpdateView):
    model = Job
    fields = ['job_code', 'description', 'hourly_rate', 'max_hour_perday']
    template_name = 'update_form.html'

    def get_object(self):
        return get_object_or_404(Job, job_code='plumber')


@method_decorator(login_required, name='dispatch')
class JobCreate(CreateView):
    model = Job
    fields = ['job_code', 'description', 'hourly_rate', 'max_hour_perday']
    template_name = 'update_form.html'


@method_decorator(login_required, name='dispatch')
class JobDelete(DeleteView):
    model = Job
    template_name = 'delete.html'
    success_url = reverse_lazy('job_management')

    def get_object(self):
        return get_object_or_404(Job, job_code='plumber')


@method_decorator(login_required, name='dispatch')
class MachineList(ListView):
    model = Machine
    context_object_name = 'machine_list'
    template_name = 'update_form.html'


@method_decorator(login_required, name='dispatch')
class MachineUpdate(UpdateView):
    model = Machine
    template_name = ''

    def get_object(self):
        return get_object_or_404(Machine, machine_code='plumber')


@method_decorator(login_required, name='dispatch')
class MachineCreate(CreateView):
    model = Machine
    template_name = ''


@method_decorator(login_required, name='dispatch')
class MachineDelete(DeleteView):
    model = Machine
    template_name = 'delete.html'
    success_url = reverse_lazy('machine_management')