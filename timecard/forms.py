from django import forms

from timecard.models import Timecard


class CreateTimeCardForm(forms.ModelForm):
    class Meta:
        model = Timecard
        fields = ['site_code','contractor_name','date']


#
# class JobEntryFom(forms.ModelForm):
#     class Meta:
#         model = JobEntry
#         exclude = []
#         def cleaned_jobentry(self):
#             data = self.cleaned_data['job_code','hours_worked','total']
