from django.contrib.auth.decorators import login_required
from django.db.models import Sum
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
from timecard.forms import CreateTimeCardForm#, LaborEntryForm
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
    success_url = reverse_lazy('job_management')


def create_timecard(request):

    if request.method == "POST":
        print("got response")
        form= CreateTimeCardForm(request.POST)
        if form.is_valid():
            timecard = form.save(commit=False)
            for i in range(3):
                var1 = 'jobcode'+str(i)
                var2 = 'hoursworked'+str(i)
                job_list = request.POST.get(var1)
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
                machine_list = request.POST.get(var1)
                hoursused = request.POST.get(var2)
                print("machine_list:",machine_list)
                print("hoursused:", hoursused)
                if int(machine_list) > 0:
                    qs = Machine.objects.filter(id=machine_list).values_list()
                    machineentry = MachineEntry(machine_code_id = qs[0][0], hours_used=hoursused, total=int(qs[0][3]) * int(hoursused),site_code=timecard.site_code)
                    print("machineentry:", machineentry)
                    machineentry.save(force_insert=True)
    # def get_object(self):
    #     job_id = self.request.GET.get("pk", "")
    #     print(job_id)
    #     return get_object_or_404(Job, id=16)

            timecard.save()
            qsjob = JobEntry.objects.filter(site_code=timecard.site_code).aggregate(Sum('hours_worked'),Sum('total'))
            qsMachine = MachineEntry.objects.filter(site_code=timecard.site_code).aggregate(Sum('hours_used'), Sum('total'))
            print("qsjob = ", qsjob)
            print("qsMachine=", qsMachine)
            total_hours=int(qsjob['hours_worked__sum'])+int(qsMachine['hours_used__sum'])
            total_amount=int(qsjob['total__sum'])+int(qsMachine['total__sum'])
            Timecard.objects.filter(site_code=timecard.site_code).update(total_hours=total_hours,total_amount=total_amount)
            print("total_hours = ",total_hours, total_amount)

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
    success_url = reverse_lazy('job_management')


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