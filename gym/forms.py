from django import forms
from .models import GymNow


class GymNowForm(forms.ModelForm):
	class Meta:
		model = GymNow
		fields = ('userId', 'entryTime')
			