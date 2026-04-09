from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm # For registration
from django.contrib.auth import login
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Event
from .forms import EventForm


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in immediately so they don't have to log in twice
            login(request, user) 
            # Redirect to the 'event_list' URL name
            return redirect('event_list') 
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

class EventListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'

    def get_queryset(self):
        
        return Event.objects.filter(user=self.request.user).order_by('date', 'time')

class EventCreateView(LoginRequiredMixin, CreateView):
    
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    success_url = reverse_lazy('event_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        
        if self.request.user.is_authenticated:
            instance = Event(user=self.request.user)
            kwargs.update({'instance': instance})
        return kwargs
    
    

    def form_valid(self, form):
        form.instance.user = self.request.user 
        return super().form_valid(form)



    
    
    
class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html' # Reuse the same form template!
    success_url = reverse_lazy('event_list')

    def get_queryset(self):
        # Prevent users from editing events they don't own via URL manipulation
        return Event.objects.filter(user=self.request.user)

class EventDeleteView(LoginRequiredMixin, DeleteView):
    model = Event
    template_name = 'events/event_confirm_delete.html'
    success_url = reverse_lazy('event_list')

    def get_queryset(self):
        return Event.objects.filter(user=self.request.user)
    
