from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Event, Photo
from django.http import HttpResponseRedirect 
import uuid
import boto3

S3_BASE_URL = 'https://s3.us-east-2.amazonaws.com/'
BUCKET = 'charlotteapp'

def signup(request):
    error_messsage = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
        else:
            error_messsage = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_messsage}
    return render(request, 'registration/signup.html', context)

def home(request):
    return render(request, 'home.html')

def saved_events(request):
    events = Event.objects.all()
    return render(request, 'saved_events.html', { 'events': events })

def event_detail(request, event_id):
    event = Event.objects.get(id = event_id)
    return render(request, 'events/detail.html', { 'event': event })

class EventCreate(LoginRequiredMixin, CreateView):
    model = Event
    fields = '__all__'
    success_url = '/events/saved/'

class EventUpdate(UpdateView):
    model = Event
    fields = '__all__'
    success_url = '/events/saved/'

def add_photo(request, event_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            photo = Photo(url=url, event_id=event_id)
            photo.save()
        except:
            print('Error occurred uploading image to S3')
    return redirect('detail', event_id=event_id)
