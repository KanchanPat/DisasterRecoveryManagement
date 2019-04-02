from django import forms

from timecard.models import Timecard, Job, JobEntry, MachineEntry


class CreateTimeCardForm(forms.ModelForm):
    class Meta:
        model = Timecard
        fields = ['site_code','contractor_name','date', 'status']
        status = forms.ChoiceField(choices=(('open', 'open'), ('review', 'finalize'), ('finalize', 'finalize')))
        # exclude = []

class JobEntryFom(forms.ModelForm):
    class Meta:
        model = JobEntry
        exclude = []
        def cleaned_jobentry(self):
            data = self.cleaned_data['job_code','hours_worked','total']
#
# class MachineEntryForm(forms.ModelForm):
#     class Meta:
#         model = MachineEntry
#         exclude = []
#         def cleaned_jobentry(self):
#             data = self.cleaned_data['machinecode','hoursused','machinetotal']
#             return data
#
# class LaborEntryForm(forms.Form):
#     # # model = Timecard_Details
#     # class Meta:
#     #     model = Job
#     #     jobs = forms.ModelChoiceField(queryset=Job.objects.all())
#     #     fields = ('job_code',)
#     #     widgets = {
#     #         'job': jobs,
#     #
#     #     }
#choices = ['open','review','fi]
#     jobcode = forms.ChoiceField(choices=[(choice.pk,choice) for choice in Job.objects.all()])
#     hours = forms.IntegerField()
#     total = forms.IntegerField()
#
