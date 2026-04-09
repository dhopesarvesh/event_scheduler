
from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'category', 'date', 'time', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        
            'time': forms.TimeInput(attrs={'type': 'time'}),
            
        }
def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')
        user = self.instance.user 

        if date and time and user:
            
            conflicts = Event.objects.filter(user=user, date=date, time=time)
            
            
            if self.instance.pk:
                conflicts = conflicts.exclude(pk=self.instance.pk)

            if conflicts.exists():
                raise forms.ValidationError("Conflict! You already have an event at this time.")
        
        return cleaned_data