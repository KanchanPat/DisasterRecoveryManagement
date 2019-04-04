from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils.decorators import method_decorator
from django.urls.base import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from timecard.models import Timecard
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import JobEntry, MachineEntry
from .forms import CreateTimeCardForm

from django.views import View

from DRApp import settings
from timecard.forms import CreateTimeCardForm
from timecard.models import Job, Machine, MachineEntry



@method_decorator(login_required, name='dispatch')
class TimeCardList(ListView):
    model = Timecard
    context_object_name = 'time_card_list'
    template_name = 'timecard_management.html'



@method_decorator(login_required, name='dispatch')
class StatusUpdateView(UpdateView):
    model = Timecard
    fields = ['status']
    template_name = 'update_form.html'
    success_url = reverse_lazy('timecard_management')


@method_decorator(login_required, name='dispatch')
class JobList(ListView):
    model = Job
    context_object_name = 'job_list'
    template_name = 'job_management.html'

    def get_object(self):
        job_id = self.request.GET.get("pk", "")
        #print(job_id)
        return get_object_or_404(Job, id=job_id)


@method_decorator(login_required, name='dispatch')
class JobUpdate(UpdateView):
    model = Job
    fields = ['job_code', 'description', 'hourly_rate', 'max_hour_perday']
    template_name = 'update_form.html'
    success_url = reverse_lazy('job_management')

@method_decorator(login_required, name='dispatch')
class JobCreate(CreateView):
    model = Job
    fields = ['job_code', 'description', 'hourly_rate', 'max_hour_perday']
    template_name = 'update_form.html'
    success_url = reverse_lazy('job_management')


@method_decorator(login_required, name='dispatch')
class JobDelete(DeleteView):
    model = Job
    template_name = 'delete.html'
    success_url = reverse_lazy('job_management.html')


@method_decorator(login_required, name='dispatch')
class MachineList(ListView):
    model = Machine
    context_object_name = 'machine_list'
    template_name = 'machine_management.html'


@method_decorator(login_required, name='dispatch')
class MachineUpdate(UpdateView):
    model = Machine
    fields = ['machine_code', 'description', 'hourly_rent', 'max_hour_perday']
    template_name = 'update_form.html'
    success_url = reverse_lazy('machine_management')



@method_decorator(login_required, name='dispatch')
class MachineCreate(CreateView):
    model = Machine
    fields = ['machine_code', 'description', 'hourly_rent', 'max_hour_perday']
    template_name = 'update_form.html'
    success_url = reverse_lazy('machine_management')


@method_decorator(login_required, name='dispatch')
class MachineDelete(DeleteView):
    model = Machine
    template_name = 'delete.html'
    success_url = reverse_lazy('machine_management.html')

@method_decorator(login_required, name='dispatch')
class TimecardList(ListView):
    model = Timecard
    context_object_name = 'timecard_list'
    template_name = 'timecard_management.html'

def create_timecard(request):

    if request.method == "POST":
        print("got response")
        form= CreateTimeCardForm(request.POST)
        #sitecode = form.cleaned_data['site_code']
        #print("sitecode" , sitecode)
        if form.is_valid():
            print("inside form valid")
            timecard = form.save(commit=False)
            for i in range(3):
                var1 = 'jobcode'+str(i)
                var2 = 'hoursworked'+str(i)
                job_list = request.POST.get(var1).split('|')[0]
                hoursworked = request.POST.get(var2)
                print("hoursworked:", hoursworked)
                print("job_list:", job_list)
                if int(job_list) >0:
                    qs = Job.objects.filter(id=job_list).values_list()
                    jobentry = JobEntry(job_code_id=qs[0][0], hours_worked=hoursworked,
                                                total=int(qs[0][3]) * int(hoursworked), site_code=timecard.site_code)
                    print("jobentry:", jobentry)
                    jobentry.save(force_insert=True)

            for i in range(3):
                var1 = 'machinecode'+str(i)
                var2 = 'hoursused'+str(i)
                machine_list = request.POST.get(var1).split('|')[0]
                hoursused = request.POST.get(var2)
                print("machine_list:",machine_list)
                print("hoursused:", hoursused)
                if int(machine_list) > 0:
                    qs = Machine.objects.filter(id=machine_list).values_list()
                    machineentry = MachineEntry(machine_code_id = qs[0][0], hours_used=hoursused, total=int(qs[0][3]) * int(hoursused),site_code=timecard.site_code)
                    print("machineentry:", machineentry)
                    machineentry.save(force_insert=True)
            timecard.save()
            qsjob = JobEntry.objects.filter(site_code=timecard.site_code).aggregate(Sum('hours_worked'),Sum('total'))
            qsMachine = MachineEntry.objects.filter(site_code=timecard.site_code).aggregate(Sum('hours_used'), Sum('total'))
            print("qsjob = ", qsjob)
            print("qsMachine=", qsMachine)
            if qsjob['hours_worked__sum'] == None:
                hour1 = 0
            else: hour1 = qsjob['hours_worked__sum']
            if qsMachine['hours_used__sum'] == None:
                hour2=0
            else: hour2=qsMachine['hours_used__sum']
            if qsjob['total__sum'] == None:
                amount1 = 0
            else : amount1=qsjob['total__sum']
            if qsMachine['total__sum'] == None:
                amount2 = 0
            else : amount2 = qsMachine['total__sum']

            total_hours=int(hour1)+int(hour2)
            total_amount=int(amount1)+int(amount2)
            Timecard.objects.filter(site_code=timecard.site_code).update(total_hours=total_hours,total_amount=total_amount)
            print("total_hours = ",total_hours, total_amount)

        return HttpResponseRedirect('/timecard_management')
    else:
        form = CreateTimeCardForm()
        #jobform = JobEntryForm()
        # subform1 = LaborEntryForm()
        job_list = Job.objects.all()
        machine_list = Machine.objects.all()

        return render(request,'timecard.html',
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
    success_url = reverse_lazy('job_management')


@method_decorator(login_required, name='dispatch')
class JobDelete(DeleteView):
    model = Job
    template_name = 'delete.html'
    success_url = reverse_lazy('job_management')



@method_decorator(login_required, name='dispatch')
class MachineList(ListView):
    model = Machine
    context_object_name = 'machine_list'
    template_name = 'machine_management.html'


@method_decorator(login_required, name='dispatch')
class MachineUpdate(UpdateView):
    model = Machine
    template_name = 'update_form.html'
    fields = ['machine_code', 'description', 'hourly_rent', 'max_hour_perday']
    success_url = reverse_lazy('machine_management')


@method_decorator(login_required, name='dispatch')
class MachineCreate(CreateView):
    model = Machine
    template_name = 'update_form.html'
    fields = ['machine_code', 'description', 'hourly_rent', 'max_hour_perday']
    success_url = reverse_lazy( 'machine_management' )


@method_decorator(login_required, name='dispatch')
class MachineDelete(DeleteView):
    model = Machine
    template_name = 'delete.html'
    success_url = reverse_lazy('machine_management')