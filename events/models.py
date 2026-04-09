from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):

    CATEGORY_CHOICES = [
        ('meeting', 'Meeting'),
        ('task', 'Task'),
        ('reminder', 'Reminder'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='reminder')
    date = models.DateField()
    time = models.TimeField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.date}"
