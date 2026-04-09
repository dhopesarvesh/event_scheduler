from django.urls import path
from . import views

urlpatterns = [
    path('', views.EventListView.as_view(), name='event_list'),
    path('create/', views.EventCreateView.as_view(), name='event_create'),
    # Add paths for update, delete, etc.
    path('signup/', views.signup, name='signup'),
    path('<int:pk>/edit/', views.EventUpdateView.as_view(), name='event_edit'),
    path('<int:pk>/delete/', views.EventDeleteView.as_view(), name='event_delete'),

]