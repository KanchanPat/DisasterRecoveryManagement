from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.

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
from timecard.forms import CreateTimeCardForm
from timecard.models import JobEntry, Timecard
from timecard_details.timecard_details import Timecard_details


def create_timecarddetails(request):
    # if not request.session.get(settings.TIMECARDDETAILS_SESSION_ID):
    #     timecarddetails={}
    #     jobs = Job.objects.all()
    #     for job in jobs:
    #         timecarddetails['job'][str(job.id)]['job_code']=job
    #     request.session[settings.TIMECARDDETAILS_SESSION_ID] = timecarddetails
    timecarddetails = Timecard_details(request)
    if request.method == 'POST':
        form = CreateTimeCardForm(request.POST)
        if form.is_valid():
            timecard = form.save(commit=False)
            for item in timecarddetails['job_list']:
                JobEntry.JobEntryFom.create(job_code=item['job_code'],
                                         hours_worked=item['hours_worked'],
                                         total=item['total'],
                                         site_code=timecarddetails['site_code'])

            # redirect to the payment
            return HttpResponseRedirect('timecard/created.html')
    else:
        form = CreateTimeCardForm()
        return render(request, 'timecard/timecard.html', {'timecarddetails': timecarddetails,
                                                        'form': form})

