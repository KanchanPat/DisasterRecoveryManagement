from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls.base import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from timecard.models import Timecard, Job, Machine
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views import View

from DRApp import settings
from timecard.forms import CreateTimeCardForm, LaborEntryForm
from timecard.models import Job, Machine, MachineEntry

@method_decorator(login_required, name='dispatch')
class TimeCardList(ListView):
    model = Timecard
    context_object_name = 'time_card_list'
    template_name = 'base.html'


@method_decorator(login_required, name='dispatch')
class JobList(ListView):
    model = Job
    context_object_name = 'job_list'
    template_name = 'job_code.html'

    def get_object(self):
        job_id = self.request.GET.get("pk", "")
        print(job_id)
        return get_object_or_404(Job, id=job_id)


@method_decorator(login_required, name='dispatch')
class JobUpdate(UpdateView):
    model = Job
    fields = ['job_code', 'description', 'hourly_rate', 'max_hour_perday']
    template_name = 'update_form.html'

# self.session = request.session
#     # GET timecarddetails FROM SESSION OBJECT
#     timecarddetails = self.session.get(settings.TIMECARDDETAILS_SESSION_ID)
#     #  IF timecarddetails DOES NOT EXIST IN SESSION , CREATE NEW
#     if not timecarddetails:
#         self.session[settings.TIMECARDDETAILS_SESSION_ID] = {}
#         timecarddetails = self.session[settings.TIMECARDDETAILS_SESSION_ID]
#         jobs = Job.objects.all()
#         for job in jobs:
#             self.timecarddetails['job'][str(job.id)]['job_code']=job
#     self.timecarddetails = timecarddetails



class JobEntryForm(object):
    pass


def create_timecard(request):
    # if not request.session.get(settings.TIMECARDDETAILS_SESSION_ID):
    #     timecarddetails={}
    #     jobs = Job.objects.all()
    #     for job in jobs:
    #         timecarddetails['job'][str(job.id)]['job_code']=job
    #     request.session[settings.TIMECARDDETAILS_SESSION_ID] = timecarddetails
    if request.method == "POST":
        print("got response")
        form= CreateTimeCardForm(request.POST)
        if form.is_valid():
            timecard = form.save(commit=False)
            timecard.save()
            job_list = request.POST.get("jobcode")
            hourwork = request.POST.get('hoursworked', '')
            print("hourwork:", hourwork)
            print("job_list:", job_list)

            machine_list = request.POST.get("machinecode")
            hoursused = request.POST.get("hoursused")

            #form.save()
            print("machine_list:",machine_list)
            print("hoursused:", hoursused)
            qs = Machine.objects.filter(id=machine_list)
            #machineentry = MachineEntry(machine_code=qs.machine_code,hours_useded=hoursused,total=int(qs.hourly_rent)*int(hoursused))
            #machineentry = MachineEntry(qs[0], hours_useded=hoursused, total=int(qs[2]) * int(hoursused))
            print("machineentry:", qs.machine_code, hoursused)
            #machineentry.save()

        return HttpResponseRedirect('timecard/created.html')
    else:
        form = CreateTimeCardForm()
        #jobform = JobEntryForm()
        # subform1 = LaborEntryForm()
        job_list = Job.objects.all()
        machine_list = Machine.objects.all()

        return render(request,'timecard/timecard.html',
                  context={'form':form,
                           'job_list':job_list,
                            'machine_list':machine_list})


class JobCreateView(View):
    def post(self, request):
        pass

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
        job_id = self.request.POST.get("pk", False)
        obj = get_object_or_404(Job, pk=int(job_id))
        return obj


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
