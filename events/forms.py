
from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'category', 'date', 'time', 'description'] # added category if you have it
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(
              
                format='%I:%M %p',
                attrs={'type': 'time', 'class': 'form-control'} 
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')
        
        user = getattr(self.instance, 'user', None)

        if date and time and user:
            
            conflicts = Event.objects.filter(
                user=user, 
                date=date, 
                time=time
            )
            
          
            if self.instance.pk:
                conflicts = conflicts.exclude(pk=self.instance.pk)

            if conflicts.exists():
                raise forms.ValidationError("Conflict! You already have an event scheduled for this exact time.")
        
        return cleaned_data