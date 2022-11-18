from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date

CATEGORIES = (
    ('B', 'Business Meeting'),
    ('U', 'UXDI'),
    ('S', 'Software Engineer'),
    ('D', 'Designer'),
    ('F', 'Finance'),
    ('R', 'Real Estate'),
    ('I', 'Self-Improvement'),
    ('M', 'Marketing'),
)
# Create your models here.
class Comment(models.Model):
    text = models.CharField(max_length = 100)

class Event(models.Model):
    name = models.CharField(max_length=50)
    date = models.DateField('Event Date')
    location = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    category = models.CharField(max_length=1, choices=CATEGORIES, default=CATEGORIES[0][0])
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_category_display()} on {self.date}"

class Comment(models.Model):
    comment = models.CharField(max_length = 50)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    
class Photo(models.Model):
    url = models.CharField(max_length=200)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for event_id: {self.event_id} @{self.url}"
