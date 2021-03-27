from django import forms
from .models import GymNow,GymWaiting


class GymNowForm(forms.ModelForm):
	class Meta:
		model = GymNow
		fields = ('userId', 'entryTime')
			
class GymWaitForm(forms.ModelForm):
	class Meta:
		model = GymWaiting
		fields = ('userId', 'waitTime')
			
class UploadFileForm(forms.Form):
    file = forms.FileField()